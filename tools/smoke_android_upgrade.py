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
def find(label,scroll=False,tap=False,timeout=100):
    until=time.monotonic()+timeout; tries=0
    while time.monotonic()<until:
        try:
            ui=tree()
        except (ET.ParseError,subprocess.CalledProcessError):
            time.sleep(1);continue
        for n in ui.iter("node"):
            if label in n.get("text","") or label in n.get("content-desc",""):
                x1,y1,x2,y2=map(int,re.findall(r"\d+",n.get("bounds")))
                if (x2>x1 and y2>y1):
                    if tap:shell("input","tap",(x1+x2)//2,(y1+y2)//2)
                    return
        tries+=1
        if scroll and tries>1:shell("input","swipe",360,1350,360,350,220)
        time.sleep(.3)
    raise RuntimeError("Could not find expected UI: "+label)
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
def learn_one():find("下一句",scroll=True,tap=True,timeout=140);find("第 2 /");stop();return snapshot()
def main(old,new):
    assert SERIAL.startswith("emulator-") and "1" in (shell("getprop","ro.kernel.qemu"), shell("getprop","ro.boot.qemu")) and os.environ.get("JYUT_DISPOSABLE_EMULATOR")=="1","Disposable emulator required"
    assert not shell("pm","list","packages",PKG),"Refusing to touch a preexisting installation"
    adb("root");adb("wait-for-device");assert shell("id","-u")=="0"
    shell("svc","wifi","disable");shell("svc","data","disable")
    shell("wm","size","720x1600");shell("wm","density","220");shell("input","keyevent","82")
    with zipfile.ZipFile(new) as z:
        rows=json.loads(z.read("assets/builtin/content.json"))["entries"]
    priority={r["id"] for r in rows if r.get("qualityPriority",0)}
    adb("install",new,timeout=120);launch();open_study(mark=True)
    fresh,attempts=learn_one();assert len(fresh)==len(attempts)==1 and set(fresh)<=priority
    print("Offline fresh-install home -> sentence study -> next: ",list(fresh),flush=True)
    adb("uninstall",PKG);adb("install",old,timeout=120);launch()
    # Old release seeded via WorkManager; wait for real counts before learning one legacy card.
    find("开始学句子",scroll=True,tap=True);find("2000 句",scroll=True);shell("input","keyevent","4")
    open_study();prior,prior_attempts=learn_one();assert len(prior)==len(prior_attempts)==1
    adb("install","-r",new,timeout=120);launch();open_study(mark=True);post,post_attempts=learn_one()
    assert len(post)==2 and all(post.get(k)==v for k,v in prior.items()),"Lost or altered learned SRS record"
    assert len(post_attempts)==2 and post_attempts[0]==prior_attempts[0],"Lost original learning attempt"
    assert set(post).difference(prior)<=priority,"Upgrade picked a non-proofread new card"
    print("Offline cover install preserved exact old SRS + attempt and selected an unseen proofread card:",set(post)-set(prior),flush=True)
if __name__=="__main__":main(*sys.argv[1:])
