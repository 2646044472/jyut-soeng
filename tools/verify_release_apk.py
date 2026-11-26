"""Check the actual signed candidate against a downloaded published APK, not a local key."""
import argparse, hashlib, json, os, re, subprocess, zipfile
from pathlib import Path
from story_proofread import approved_story_ids

ROOT = Path(__file__).resolve().parents[1]


def run(exe, *args):
    return subprocess.check_output([str(exe), *map(str, args)], text=True)


def manifest(path, build_tools):
    text=run(build_tools / "aapt", "dump", "badging", path)
    m=re.search(r"^package: name='([^']+)' versionCode='(\d+)' versionName='([^']+)'",text,re.M)
    if not m: raise RuntimeError(f"Cannot read manifest for {path}")
    return m[1],int(m[2]),m[3]


def certs(path, build_tools):
    report=run(build_tools / "apksigner","verify","--verbose","--print-certs",path)
    digests=set(re.findall(r"^Signer #\d+ certificate SHA-256 digest: ([a-f0-9]{64})$",report,re.M|re.I))
    if not digests:raise RuntimeError("Missing APK signer")
    return digests


def main():
    p=argparse.ArgumentParser();p.add_argument("old",type=Path);p.add_argument("new",type=Path);p.add_argument("pack",type=Path);a=p.parse_args()
    sdk=os.environ.get("ANDROID_HOME") or os.environ["ANDROID_SDK_ROOT"];bt=Path(sdk)/"build-tools/35.0.0"
    old,new=manifest(a.old,bt),manifest(a.new,bt)
    assert old[0]==new[0]=="dev.local.yuecal" and new[1]>old[1],(old,new)
    assert tuple(map(int,new[2].split(".")))>tuple(map(int,old[2].split("."))),(old,new)
    assert certs(a.old,bt)==certs(a.new,bt),"Candidate certificate does not match the published APK"
    with zipfile.ZipFile(a.new) as z:builtin=z.read("assets/builtin/content.json")
    with zipfile.ZipFile(a.pack) as z:updated=z.read("jyut-soeng/content.json")
    assert builtin==updated==(ROOT/"app/src/main/assets/builtin/content.json").read_bytes(),"Pack mismatch"
    with zipfile.ZipFile(a.old) as z:baseline=json.loads(z.read("assets/builtin/content.json"))["entries"]
    rows=json.loads(builtin)["entries"]
    assert {x["id"] for x in baseline}=={x["id"] for x in rows} and len(rows)==len(baseline)==5000
    accepted=approved_story_ids(ROOT)
    assert {x["id"] for x in rows if x.get("qualityPriority",0)}==accepted
    assert len([x for x in rows if x["entryType"]=="sentence"])==2000
    print("Published -> candidate:",old,"->",new)
    print("Matching APK signing certificate(s):",sorted(certs(a.new,bt)))
    print(f"Identical built-in/update pack; {len(accepted)}/2000 priority. SHA-256 APK:",hashlib.file_digest(a.new.open("rb"),"sha256").hexdigest())

if __name__=="__main__":main()
