
# Ingram Mod Manager v1 (beta)

![Banner](./banner.jpg)

Custom mod loader for the [Ingram](https://github.com/jorhelp/Ingram) camera scanner. It uses monkey patching to hook into the core engine at runtime without touching original source files

## Preincluded mods

**fixer.py**
* Patches `SnapshotPipeline` to stop `gevent.exceptions.LoopExit` errors when the queue is empty.
* Redirects `stderr` to `devnull` to keep the console clean from junk tracebacks.

**SmartSort.py (Smart Downloader, Sorter)**
* Handles Dahua "Invalid Authority" errors by cycling through auth types (Basic/Digest) and channel IDs
* Automatically detects PTZ (Pan-Tilt-Zoom) support via ISAPI.
* Sorts snapshots into folders: `/Basic` or `/PTZ_Cam`.
* Tries multiple snapshot paths (CVE-bypass, ISAPI, CGI) to ensure capture

**Styler.py (Interface)**
* Replaces the default logo with a custom pretty gradient ASCII-art and status banner.

## Installation

1. Copy `run_with_mods.py`, `mod_loader.py`, and the `mods/` folder into your Ingram root directory.
2. Install dependencies:
```bash
pip install requests pycryptodome colorama loguru gevent
```

## Usage

Run the scanner via `run_with_mods.py`. It's all original Ingram arguments:

```bash
python run_with_mods.py -i targets.txt -o out_folder -t 1000
```

## Modding API

Add your own mods to the `mods/` directory. A template:
You can also use pre-installed mods as template to make your own mod. Explore the mod engine script to understand how to write mods easily!
It's basically just python scripts.
```python
def reg(mgr):
    # Events: 'start' (launcher init) or 'found' (camera found)
    mgr.sub('found', my_mod_logic)

def my_mod_logic(res, cfg):
    # res = (ip, port, product, user, password, vul_name)
    # cfg = Ingram config object
    print(f"Mod triggered for: {res[0]}")
```

---
**Author:** @notos0  
**Disclaimer:** For authorized security testing only. Use at your own risk
