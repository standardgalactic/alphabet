import gradio as gr
from rsvp_stack.plugins import load_plugins, PLUGIN_REGISTRY
load_plugins()
def list_plugins():
    return '\\n'.join(PLUGIN_REGISTRY.keys())
def run_plugin(name):
    p = PLUGIN_REGISTRY.get(name)
    if not p: return f'plugin {name} not found'
    mod = p['module']
    if hasattr(mod,'run'):
        return str(mod.run(None))
    return 'no run()'
with gr.Blocks() as demo:
    gr.Markdown('# RSVP Stack Plugins')
    pl = gr.Textbox(value=list_plugins(), label='discovered plugins')
    inp = gr.Textbox(label='plugin name')
    btn = gr.Button('Run')
    out = gr.Textbox(label='output')
    btn.click(lambda n: run_plugin(n), inputs=inp, outputs=out)
if __name__=='__main__':
    demo.launch()
