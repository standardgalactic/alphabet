import json, os
REG_PATH = os.path.expanduser('~/.rsvp_model_registry.json')
def _load():
    if os.path.exists(REG_PATH):
        return json.load(open(REG_PATH))
    return {}
def register(name, meta):
    r = _load()
    r[name] = meta
    json.dump(r, open(REG_PATH,'w'))
def list_models():
    return _load()
