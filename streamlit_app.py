import os
import json
import streamlit as st
from datetime import datetime

# 📂 Carpeta base donde se almacenan los proyectos
CARPETA_PROYECTOS = "proyectos"
os.makedirs(CARPETA_PROYECTOS, exist_ok=True)

# 🚀 Paso 1: Seleccionar o crear proyecto
st.sidebar.subheader("📁 Proyecto")
proyectos = sorted([f for f in os.listdir(CARPETA_PROYECTOS) if os.path.isdir(os.path.join(CARPETA_PROYECTOS, f))])
proyecto_seleccionado = st.sidebar.selectbox("Selecciona un proyecto", ["Nuevo proyecto..."] + proyectos)

if proyecto_seleccionado == "Nuevo proyecto...":
    nuevo_nombre = st.sidebar.text_input("Introduce el nombre del nuevo proyecto")
    if st.sidebar.button("Crear proyecto") and nuevo_nombre:
        ruta_nuevo = os.path.join(CARPETA_PROYECTOS, nuevo_nombre)
        os.makedirs(ruta_nuevo, exist_ok=True)
        st.experimental_rerun()
else:
    ruta_proyecto = os.path.join(CARPETA_PROYECTOS, proyecto_seleccionado)

    # 🚀 Paso 2: Seleccionar o crear versión
    st.sidebar.subheader("🧾 Versión")
    versiones = sorted([v.replace(".json", "") for v in os.listdir(ruta_proyecto) if v.endswith(".json")])
    version_seleccionada = st.sidebar.selectbox("Selecciona una versión", ["Nueva versión..."] + versiones)

    if version_seleccionada == "Nueva versión...":
        nueva_version = st.sidebar.text_input("Nombre de la nueva versión")
        if st.sidebar.button("Crear versión") and nueva_version:
            nombre_archivo = nueva_version + ".json"
            ruta_version = os.path.join(ruta_proyecto, nombre_archivo)
            datos_base = {}  # aquí puedes poner un estado base si lo deseas
            with open(ruta_version, "w", encoding="utf-8") as f:
                json.dump(datos_base, f, indent=2)
            st.session_state["ruta_version_actual"] = ruta_version
            st.experimental_rerun()
    else:
        ruta_version = os.path.join(ruta_proyecto, version_seleccionada + ".json")
        st.session_state["ruta_version_actual"] = ruta_version

        # ✅ Cargar la versión seleccionada
        with open(ruta_version, "r", encoding="utf-8") as f:
            st.session_state["datos_proyecto"] = json.load(f)
