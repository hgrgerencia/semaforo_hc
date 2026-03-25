import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from controller.registro_controller import FactoryRegistros

# --- Funciones de Soporte ---
def cargar_datos():
    [data, df] = FactoryRegistros.get_all_collection(1)
    return data

def calcular_estado(row):
    hoy = datetime.now()
    vencimiento = datetime.strptime(row['fecha_vencimiento'], '%Y-%m-%d')
    dias_restantes = (vencimiento - hoy).days
    alerta = row.get('dias_alerta_previa', 30)

    if dias_restantes < 0: return "🔴 VENCIDO"
    elif dias_restantes <= alerta: return "🟡 POR VENCER"
    return "🟢 VIGENTE"

# --- VISTA: SEMÁFORO ---
def vista_semaforo():
    st.title("🚦 Monitor de Vencimientos Operativos")
    
    data = cargar_datos()
    if not data:
        st.info("No hay datos registrados.")
        return

    df = pd.DataFrame(data)
    
    # Filtros para que sea interactivo
    cats = df['categoria'].unique().tolist()
    sel = st.multiselect("Filtrar por Área:", cats, default=cats)
    df_f = df[df['categoria'].isin(sel)].copy()


    if df_f.empty:
        st.warning("No hay registros que coincidan con el filtro.")
        return
    
    # --- Resumen de Métricas (Opcional, para dar más valor visual) ---

    c1, c2, c3 = st.columns(3)
    vencidos = len(df_f[df_f.apply(lambda r: "🔴" in calcular_estado(r), axis=1)])
    alertas = len(df_f[df_f.apply(lambda r: "🟡" in calcular_estado(r), axis=1)])
    vigentes = len(df_f[df_f.apply(lambda r: "🟢" in calcular_estado(r), axis=1)])

    c1.metric("Vencidos", vencidos, delta_color="inverse")
    c2.metric("En Alerta", alertas)
    c3.metric("Vigentes", vigentes)

    # --- Construcción de la Tabla en Markdown ---
    # Encabezado de la tabla Markdown
    tabla_md = "| Documento / Trámite | Categoría | Vencimiento | Responsable | Estado |\n"
    tabla_md += "| :--- | :--- | :--- | :--- | :--- |\n"

    for _, row in df_f.iterrows():
        # Calculamos el estado usando tu función existente
        estado_raw = calcular_estado(row)
        
        # Limpiamos el texto del nombre para que no rompa la tabla (evitar pipes '|')
        nombre = str(row['nombre']).replace("|", "-")
        entidad = str(row.get('entidad', 'N/A')).replace("|", "-")
        categoria = row['categoria']
        fecha = row['fecha_vencimiento']
        resp = row.get('responsable', 'N/A')

        # Construimos la fila
        # Combinamos Nombre + Entidad en la primera columna para ahorrar espacio
        tabla_md += f"| **{nombre}** / _{entidad}_ | {categoria} | `{fecha}` | {resp} | {estado_raw} |\n"

    # Renderizamos la tabla directamente
    st.markdown(tabla_md)

    