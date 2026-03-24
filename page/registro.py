import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from controller.registro_controller import FactoryRegistros

DB_FILE = 'data.json'

# --- Funciones de Soporte ---
CATEGORIAS = ["Productos (CPE/Sanitario)", "Contratos (Arrendamiento/Franquicia)", "Permisología Cali (Bomberos/RIF/Sanidad)", "Compras (Importación)", "Producción (Calderas/Químicos)", "Marcas SAPI"]
def cargar_datos():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def guardar_todos(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def eliminar_registro(idx):
    data = cargar_datos()
    if 0 <= idx < len(data):
        eliminado = data.pop(idx)
        guardar_todos(data)
        return True, eliminado['nombre']
    return False, ""

def actualizar_registro(idx, nuevos_datos):
    data = cargar_datos()
    if 0 <= idx < len(data):
        data[idx] = nuevos_datos
        guardar_todos(data)
        return True
    return False

# ==========================================
# 2. MODALES (DIALOGS)
# ==========================================

@st.dialog("Editar Registro")
def modal_editar(idx, registro_actual):
    st.write(f"Modificando: **{registro_actual['nombre']}**")
    
    with st.form("form_modal_edit"):
        nombre = st.text_input("Nombre", value=registro_actual['nombre'])
        c1, c2 = st.columns(2)
        with c1:
            try:
                indice_cat = CATEGORIAS.index(registro_actual['categoria'])
            except ValueError:
                indice_cat = 0

            cat = st.selectbox("Categoría", options=CATEGORIAS, index=indice_cat)
            resp = st.text_input("Responsable", value=registro_actual.get('responsable', ''))
        with c2:
            fecha_actual = datetime.strptime(registro_actual['fecha_vencimiento'], '%Y-%m-%d')
            fecha = st.date_input("Vencimiento", value=fecha_actual)
            alerta = st.number_input("Días Alerta", value=registro_actual.get('dias_alerta_previa', 30))

        entidad = st.text_input("Entidad", value=registro_actual.get('entidad', ''))
        prioridad = st.select_slider("Prioridad", options=["Baja", "Media", "Alta", "Crítica"], 
                                     value=registro_actual.get('prioridad', 'Media'))

        if st.form_submit_button("Guardar Cambios", use_container_width=True):
            datos_nuevos = {
                "nombre": nombre, "categoria": cat, "entidad": entidad,
                "fecha_vencimiento": str(fecha), "dias_alerta_previa": alerta,
                "responsable": resp, "prioridad": prioridad
            }
            if FactoryRegistros.update_one_collection(idx, datos_nuevos):
                st.success("Registro actualizado")
                st.rerun()

@st.dialog("Confirmar Eliminación")
def modal_confirmar_eliminar(idx, nombre_registro):
    st.warning(f"⚠️ ¿Estás seguro de que deseas eliminar el registro: **{nombre_registro}**?")
    st.write("Esta acción no se puede deshacer.")
    
    # Usamos columnas para los botones de confirmación
    c1, c2 = st.columns(2)
    
    with c1:
        if st.button("Sí, Eliminar", use_container_width=True, type="primary"):
            exito = FactoryRegistros.delete_one_collection(idx)
            if exito:
                st.toast(f"✅ {idx} eliminado correctamente")
                st.rerun()
    
    with c2:
        if st.button("Cancelar", use_container_width=True):
            st.rerun() # Simplemente cierra el modal al recargar

# ==========================================
# 3. VISTA DE REGISTRO
# ==========================================
def vista_registro():
    st.title("⚙️ Gestión de Base de Datos")
    

    # --- Sección de Nuevo Registro ---
    with st.expander("➕ Agregar Nuevo Registro"):
        with st.form("form_nuevo", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                nombre = st.text_input("Nombre del Documento/Permiso")
                cat = st.selectbox("Categoría", CATEGORIAS)
                entidad = st.text_input("Entidad")
            with c2:
                fecha = st.date_input("Fecha de Vencimiento")
                # Lógica automática según tu descripción de audio
                dias_sugeridos = 180 if cat == "Marcas SAPI" else 30
                alerta = st.number_input("Días de Alerta Previa", value=dias_sugeridos)
                resp = st.text_input("Responsable")
            
            if st.form_submit_button("Registrar en Sistema", use_container_width=True):
                if nombre:
                    nueva_entrada = {
                        "nombre": nombre, "categoria": cat, "entidad": entidad,
                        "fecha_vencimiento": str(fecha), "dias_alerta_previa": alerta,
                        "responsable": resp, "prioridad": "Media"
                    }
                    FactoryRegistros.insert_one_collection(nueva_entrada)
                    st.success("¡Registro exitoso!")
                    st.rerun()
                else:
                    st.error("El nombre es obligatorio")

    # --- Sección de Tabla con Checkbox ---
    st.subheader("📋 Registros Actuales")
    [data, df] = FactoryRegistros.get_all_collection(1)

    if data:
        df_gest = pd.DataFrame(data)
        
        # Selección moderna de filas
        evento = st.dataframe(
            df_gest[['nombre', 'categoria', 'fecha_vencimiento', 'responsable']],
            width='stretch',
            selection_mode="single-row",
            on_select="rerun"
        )

        indices = evento.get("selection", {}).get("rows", [])
        
        if indices:
            idx = indices[0]
            registro_sel = data[idx] # Obtenemos el registro seleccionado
            col1, col2, _ = st.columns([1, 1, 3])
            with col1:
                if st.button("✏️ Editar", use_container_width=True):
                    modal_editar(registro_sel["id"], data[idx])
            with col2:
                # CAMBIO AQUÍ: Ahora llama al modal de confirmación
                if st.button("🗑️ Eliminar", use_container_width=True):
                    modal_confirmar_eliminar(registro_sel["id"], registro_sel['nombre'])

    else:
        st.write("No hay registros en el sistema.")



    


