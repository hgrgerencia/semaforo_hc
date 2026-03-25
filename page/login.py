import streamlit as st 

IMG= "img/logo.png"
def show_login():
    LISTA_MENU_ADMIN= [ "📊 Panel de Semáforo","📝 Registrar Obligación","🔐 Cerrar Sesión"]
    LISTA_MENU_OBSERVADOR= [ "📊 Panel de Semáforo","🔐 Cerrar Sesión"]

    st.image(IMG,width="content")
    
    st.title("Iniciar Sesión")
    with st.form(key="login_form",clear_on_submit=True):
        username = st.text_input("Nombre de Usuario")
        password = st.text_input("Contraseña", type="password")
        button = st.form_submit_button("Iniciar Sesión")
        

        if button:
            if username == st.secrets["USERNAME_ADMIN"] and password == st.secrets["PASSWORD"]:   
                st.session_state.username = 'admin'         
                st.session_state.menu = LISTA_MENU_ADMIN
                st.session_state["login"] = True
                st.rerun(scope="app")
            if username == st.secrets["USERNAME_OBSERVADOR"] and password == st.secrets["PASSWORD_OBSERVADOR"]:    
                st.session_state.username = 'semaforo_hc'        
                st.session_state.menu = LISTA_MENU_OBSERVADOR
                st.session_state["login"] = True
                st.rerun(scope="app")
            else:
                st.error("Credenciales incorrectas")