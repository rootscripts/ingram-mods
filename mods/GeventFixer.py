# This mod is for patching gevent loop errors and silencing console noise
import time, os, sys
from Ingram.data import SnapshotPipeline

def reg(mgr):
    sys.stderr = open(os.devnull, 'w')
    def get_real(obj):
        if hasattr(obj, '__closure__') and obj.__closure__:
            for c in obj.__closure__:
                if isinstance(c.cell_contents, type): return c.cell_contents
        return None

    cls = get_real(SnapshotPipeline)
    if not cls: return
    
    def quiet_process(self, core):
        while not core.finish():
            try:
                if self.pipeline.empty():
                    time.sleep(1)
                    continue
                task = self.pipeline.get(timeout=2)
                self.workers.submit(self._snapshot, *task)
                with self.task_count_lock: self.task_count += 1
            except:
                time.sleep(0.5)

    cls.process = quiet_process
    print("[*] Engine patches applied.")