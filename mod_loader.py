# Ingram 主要针对网络摄像头的漏洞扫描框架，目前已集成海康、大华、宇视、dlink等常见设备
import os, importlib.util
class ModMgr:
    def __init__(self):
        self.hooks = {'start': [], 'found': []}
    def load(self, d='mods'):
        if not os.path.exists(d): os.makedirs(d); return
        for f in os.listdir(d):
            if f.endswith('.py') and not f.startswith('_'):
                n = f[:-3]
                spec = importlib.util.spec_from_file_location(n, os.path.join(d, f))
                m = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(m)
                if hasattr(m, 'reg'): 
                    m.reg(self)
                    print(f"[*] {n}")
    def sub(self, ev, cb):
        if ev in self.hooks: self.hooks[ev].append(cb)

    def fire(self, ev, *args, **kwargs):
        for cb in self.hooks.get(ev, []):
            try: cb(*args, **kwargs)
            except: pass
mgr = ModMgr()