#! /usr/bin/env python3
import warnings; warnings.filterwarnings("ignore")
from gevent import monkey; monkey.patch_all(thread=False)
import os, sys, traceback
from multiprocessing import Process
from Ingram import get_config, Core
from Ingram.data import SnapshotPipeline 
from Ingram.utils import common, get_parse, log, logo, color
from mod_loader import mgr

def get_cls(obj):
    if hasattr(obj, '__closure__') and obj.__closure__:
        for c in obj.__closure__:
            if isinstance(c.cell_contents, type): return c.cell_contents
    return None

pipe_cls = get_cls(SnapshotPipeline)
if pipe_cls:
    _orig = pipe_cls._snapshot
    def _hooked(self, func, res):
        mgr.fire('found', res=res, cfg=self.config)
        return _orig(self, func, res)
    pipe_cls._snapshot = _hooked

def run():
    try:
        mgr.load()
        mgr.fire('start')

        args = get_parse()
        cfg = get_config(args)
        
        if not os.path.exists(cfg.out_dir): os.makedirs(cfg.out_dir)
        s_path = os.path.join(cfg.out_dir, cfg.snapshots)
        if not os.path.exists(s_path): os.makedirs(s_path)
            
        log.config_logger(os.path.join(cfg.out_dir, cfg.log), cfg.debug)
        
        # На Windows Ingram запускается в том же процессе
        core_obj = Core(cfg)
        if common.os_check() == 'windows':
            core_obj.run()
        else:
            p = Process(target=core_obj.run)
            p.start()
            p.join()

    except KeyboardInterrupt:
        sys.exit()
    except Exception:
        # Если упадет - мы увидим почему
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    run()