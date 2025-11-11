from rsvp_stack.plugins import load_plugins, PLUGIN_REGISTRY, list_plugins
import inspect

load_plugins()

class RSVPStack:
    def __init__(self, cfg):
        self.cfg = cfg
        self.modules = {}
        backend = cfg.backend

        def grab(name): return PLUGIN_REGISTRY.get(name)
        def grab_backend(base): return PLUGIN_REGISTRY.get(f"{base}_{backend}")

        if cfg.rsvp.enabled: self.modules["rsvp"] = grab_backend("rsvp")
        if cfg.ebssc.enabled: self.modules["ebssc"] = grab_backend("ebssc")
        if cfg.spherepop.enabled: self.modules["spherepop"] = grab("spherepop")
        if cfg.tartan.enabled: self.modules["tartan"] = grab_backend("tartan")
        if cfg.clio.enabled: self.modules["clio"] = grab_backend("clio")

    def run(self):
        print("Plugins:", list(list_plugins().keys()))
        results = {}
        for k, plug in self.modules.items():
            if not plug: continue
            mod = plug["module"]
            if hasattr(mod, "run"): results[k] = mod.run()
            elif hasattr(mod, "train"): results[k] = mod.train()
            else: results[k] = "loaded"
        return results