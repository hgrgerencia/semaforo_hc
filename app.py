import streamlit as st
from page.registro import  vista_registro
from page.semaforo import vista_semaforo
from page.login import show_login
from streamlit_option_menu import option_menu

# Configuración global
st.set_page_config(page_title="🚦Semáforo H.C", layout="wide")

if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.menu = ["🗝️ Login"]

NOMBRE_EMPRESA = st.secrets["NOMBRE_EMPRESA"]
def main():
    
    with st.sidebar: 
        selected = option_menu( 
            menu_title=F"🚦 Semaforo {NOMBRE_EMPRESA}", 
            options=st.session_state.menu, 
            menu_icon="cast", 
            default_index=0, 
        )
    
    # Lógica de enrutamiento
    if selected == "🗝️ Login":
        show_login() 
    if selected  == "📊 Panel de Semáforo":
        vista_semaforo()
    if selected  == "📝 Registrar Obligación":
        vista_registro()
        
    if selected  == "🔐 Cerrar Sesión":
        st.session_state.login = False
        st.session_state.menu = ["🗝️ Login"]
        st.rerun(scope="app")

if __name__ == "__main__":
    main()