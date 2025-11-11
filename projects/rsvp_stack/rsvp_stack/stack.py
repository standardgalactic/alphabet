from rsvp_stack.plugins import load_plugins, PLUGIN_REGISTRY, list_plugins
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
        print("Detected plugins:", list_plugins())
        results = {}
        for k, plug in self.modules.items():
            if not plug:
                print(f"[skip] {k}")
                continue
            mod = plug["module"]
            print(f"[run] {k}")
            if hasattr(mod, "train"):
                results[k] = mod.train(self.cfg)
            elif hasattr(mod, "run"):
                results[k] = mod.run(self.cfg)
            else:
                results[k] = "loaded"
        return results
