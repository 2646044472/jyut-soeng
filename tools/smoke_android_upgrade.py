"""UI + progress smoke test on an explicitly disposable CI emulator (never a user's phone)."""
import json, os, re, sqlite3, subprocess, sys, tempfile, time, xml.etree.ElementTree as ET, zipfile
from pathlib import Path
PKG="dev.local.yuecal"
DB=f"/data/user/0/{PKG}/databases/canto_calibrator.db"
SERIAL=os.environ.get("ANDROID_SERIAL","emulator-5554")
def adb(*args,timeout=40): return subprocess.check_output(["adb","-s",SERIAL,*map(str,args)],timeout=timeout,text=True).strip()
def shell(*args): return adb("shell",*args)
def launch(): shell("am","start","-W","-n",PKG+"/.MainActivity")
def stop(): shell("am","force-stop",PKG)
def tree():
    shell("uiautomator","dump","--compressed","/data/local/tmp/jyut-smoke.xml")
    return ET.fromstring(adb("exec-out","cat","/data/local/tmp/jyut-smoke.xml"))
def labels(n):
    return [v.strip() for k in ("text","content-desc") if (v:=n.get(k,"")).strip()]

def bounds(n):
    coords=re.fullmatch(r"\[(-?\d+),(-?\d+)\]\[(-?\d+),(-?\d+)\]",n.get("bounds",""))
    if coords:
        x1,y1,x2,y2=map(int,coords.groups())
        if 0<=x1<x2 and 0<=y1<y2:return (x1,y1,x2,y2)

def exact_control(ui,label):
    # The reader header itself contains the words “上一句或下一句”: never tap a substring.
    parents={child:n for n in ui.iter() for child in n}
    for n in ui.iter("node"):
        if n.get("package")!=PKG or label not in labels(n) or bounds(n) is None:continue
        while n is not None and n.get("package")==PKG:
            if n.get("enabled")=="false":break
            if n.get("clickable")=="true" and n.get("enabled")=="true" and (rect:=bounds(n)):
                return rect
            n=parents.get(n)
    return None

def diagnostic_labels(ui):
    if ui is None:return []
    found=[]
    for n in ui.iter("node"):
        if n.get("package")!=PKG:continue
        for value in labels(n):
            if (len(value)>=3 or value in ("下一句","上一句","完成")) and not re.fullmatch("[a-z]+[1-6]",value):
                line=value.replace("\n"," ")[:130]
                if line not in found:found.append(line)
    return found[:18]

def counter(index):
    # Full header starts with this index, not just a number in the story.
    return re.compile(rf"^第\s*{index}\s*/\s*\d+\s*句(?:\s|$)")

def find(label,scroll=False,tap=False,timeout=100,pattern=None,exact_button=False,up=False):
    until=time.monotonic()+timeout; tries=0; ui=None; last_error=None
    while time.monotonic()<until:
        try:
            ui=tree()
        except (ET.ParseError,subprocess.SubprocessError) as e:
            last_error=type(e).__name__;time.sleep(1);continue
        if exact_button:
            rect=exact_control(ui,label)
            if rect:
                x1,y1,x2,y2=rect
                print(f"Tap exact enabled control {label!r} at {rect}",flush=True)
                shell("input","tap",(x1+x2)//2,(y1+y2)//2)
                return
        else:
            for n in ui.iter("node"):
                if any((pattern.search(v) if pattern else label in v) for v in labels(n)) and (rect:=bounds(n)):
                    x1,y1,x2,y2=rect
                    if tap:shell("input","tap",(x1+x2)//2,(y1+y2)//2)
                    return
        tries+=1
        if (scroll or up) and tries>1:
            shell("input","swipe",360,400 if up else 1350,360,1350 if up else 350,220)
        time.sleep(.3)
    raise RuntimeError(f"Missing {label!r}; last dump error={last_error}; visible reader labels={diagnostic_labels(ui)!r}")

def open_study(mark=False):
    find("开始学句子",scroll=True,tap=True)
    find("开始今日句子学习",tap=True)
    find("粤拼 · 粤语原句")
    if mark:find("已逐字精校")
def snapshot():
    # Only after force-stop, from a disposable, offline, rooted emulator with synthetic records.
    with tempfile.TemporaryDirectory() as t:
        dest=Path(t)/"canto.db"
        for suff in ("","-wal"):
            if shell("sh","-c",f"'test -s {DB}{suff} && echo present || true'")=="present":
                adb("pull",DB+suff,str(dest)+suff)
        with sqlite3.connect(dest) as db:
            return dict((r[0],r[1:]) for r in db.execute("SELECT entryId,repetitions,intervalDays,easeFactor,nextReviewEpochDay,lastReviewedAt,totalCorrect,totalAttempts,streak FROM review_progress")),list(db.execute("SELECT * FROM study_attempts ORDER BY id"))
def learn_one(stage):
    try:
        find("reader 1",pattern=counter(1))
        find("下一句",scroll=True,exact_button=True,timeout=140)
        find("reader 2",pattern=counter(2),up=True,timeout=75)
    except Exception:
        # Only synthetic data from the explicitly disposable, offline CI emulator.
        try:
            print(f"{stage} UI failure; app pid={shell('pidof',PKG)}",flush=True)
        except Exception:pass
        try:
            stop();progress,attempts=snapshot()
            print(f"{stage}: persisted progress IDs={list(progress)[:3]} attempts={len(attempts)}",flush=True)
        except Exception as e:
            print(f"{stage}: diagnostic DB unavailable ({type(e).__name__})",flush=True)
        raise
    stop();return snapshot()
def main(old,new):
    assert SERIAL.startswith("emulator-") and "1" in (shell("getprop","ro.kernel.qemu"), shell("getprop","ro.boot.qemu")) and os.environ.get("JYUT_DISPOSABLE_EMULATOR")=="1","Disposable emulator required"
    assert not shell("pm","list","packages",PKG),"Refusing to touch a preexisting installation"
    adb("root");adb("wait-for-device");assert shell("id","-u")=="0"
    shell("svc","wifi","disable");shell("svc","data","disable")
    shell("wm","size","720x1600");shell("wm","density","220");shell("input","keyevent","82")
    with zipfile.ZipFile(new) as z:
        rows=json.loads(z.read("assets/builtin/content.json"))["entries"]
    priority=[r["id"] for r in sorted(rows,key=lambda r:(r["sortOrder"],r["id"])) if r["entryType"]=="sentence" and r.get("qualityPriority")==1]
    adb("install",new,timeout=120);launch();open_study(mark=True)
    fresh,attempts=learn_one("fresh");assert len(attempts)==1 and set(fresh)=={priority[0]},(list(fresh),len(attempts),priority[0])
    print("Offline fresh-install home -> sentence study -> next: ",list(fresh),flush=True)
    adb("uninstall",PKG);adb("install",old,timeout=120);launch()
    # Old release seeded via WorkManager; wait for real counts before learning one legacy card.
    find("开始学句子",scroll=True,tap=True);find("2000 句",scroll=True);shell("input","keyevent","4")
    open_study();prior,prior_attempts=learn_one("legacy");assert len(prior)==len(prior_attempts)==1
    adb("install","-r",new,timeout=120);launch();open_study(mark=True);post,post_attempts=learn_one("cover")
    assert len(post)==2 and all(post.get(k)==v for k,v in prior.items()),"Lost or altered learned SRS record"
    assert len(post_attempts)==2 and post_attempts[0]==prior_attempts[0],"Lost original learning attempt"
    expected=next(k for k in priority if k not in prior)
    assert set(post).difference(prior)=={expected},("Wrong first unseen proofread card",list(post),expected)
    print("Offline cover install preserved exact old SRS + attempt and selected an unseen proofread card:",set(post)-set(prior),flush=True)
if __name__=="__main__":main(*sys.argv[1:])
