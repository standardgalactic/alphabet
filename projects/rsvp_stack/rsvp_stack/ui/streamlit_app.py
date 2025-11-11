import streamlit as st
from rsvp_stack.plugins import load_plugins, list_plugins, PLUGIN_REGISTRY
load_plugins()
st.title('RSVP Stack')
st.write('Detected plugins:', list_plugins())
sel = st.selectbox('plugin', list_plugins())
if st.button('run'):
    mod = PLUGIN_REGISTRY[sel]['module']
    if hasattr(mod,'run'):
        st.write(mod.run(None))
    else:
        st.write('no run()')
