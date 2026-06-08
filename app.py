import streamlit as st
import pandas as pd

st.set_page_config(page_title="Policultivos Uruguay", page_icon="🌱", layout="wide")

@st.cache_data
def cargar_datos():
    xl = pd.read_excel("Base_Datos_Agroecologica_Uruguay.xlsx", sheet_name=None)
    return xl

datos = cargar_datos()
cultivos = datos["Cultivos_Horticolas"]
funcionales = datos["Plantas_Funcionales"]
agroforestales = datos["Agroforestales"]
silvopastoril = datos["Silvopastoril"]
compatibilidades = datos["Compatibilidades"]

st.title("🌱 Planificador de Policultivos - Uruguay")
st.caption("Basado en datos agroecológicos para condiciones de Uruguay")

tab1, tab2, tab3, tab4 = st.tabs([
    "🌿 Por planta",
    "📅 Por estación",
    "🌸 Plantas funcionales",
    "🔍 Compatibilidades"
])

# --- TAB 1: POR PLANTA ---
with tab1:
    col1, col2 = st.columns([1, 2])

    with col1:
        planta_sel = st.selectbox(
            "Elegí un cultivo",
            cultivos["Nombre_comun"].tolist()
        )

    fila = cultivos[cultivos["Nombre_comun"] == planta_sel].iloc[0]

    with col2:
        region = fila["Region_Uruguay"] if pd.notna(fila["Region_Uruguay"]) else "—"
        estacion = fila["Estacion_siembra"] if pd.notna(fila["Estacion_siembra"]) else "—"
        st.markdown(f"**{fila['Nombre_cientifico']}** · {fila['Familia']}")
        st.caption(f"📍 {region} · 🗓️ Siembra: {estacion}")

    st.divider()

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Temp. mínima", f"{fila['Temp_min_C']}°C")
    with col_b:
        st.metric("Temp. óptima", f"{fila['Temp_optima_C']}°C")
    with col_c:
        st.metric("Temp. máxima", f"{fila['Temp_max_C']}°C")

    st.divider()

    col_comp, col_incomp = st.columns(2)

    with col_comp:
        st.subheader("✅ Compañeras ideales")
        if pd.notna(fila["Compatible"]):
            for planta in fila["Compatible"].split(";"):
                planta = planta.strip()
                rel = compatibilidades[
                    ((compatibilidades["Especie_A"] == planta_sel) & (compatibilidades["Especie_B"] == planta)) |
                    ((compatibilidades["Especie_B"] == planta_sel) & (compatibilidades["Especie_A"] == planta))
                ]
                with st.expander(f"🌿 {planta}"):
                    if not rel.empty:
                        r = rel.iloc[0]
                        st.write(f"**Mecanismo:** {r['Mecanismo']}")
                        st.write(f"**Intensidad:** {r['Intensidad']}")
                        if pd.notna(r["Fuente"]):
                            st.caption(f"Fuente: {r['Fuente']}")
                    else:
                        st.write("Combinación beneficiosa registrada en la base de datos.")
        else:
            st.info("No hay compañeras registradas para este cultivo.")

    with col_incomp:
        st.subheader("❌ Incompatibles")
        if pd.notna(fila["Incompatible"]):
            for planta in fila["Incompatible"].split(";"):
                planta = planta.strip()
                rel = compatibilidades[
                    ((compatibilidades["Especie_A"] == planta_sel) & (compatibilidades["Especie_B"] == planta)) |
                    ((compatibilidades["Especie_B"] == planta_sel) & (compatibilidades["Especie_A"] == planta))
                ]
                with st.expander(f"⚠️ {planta}"):
                    if not rel.empty:
                        r = rel.iloc[0]
                        st.write(f"**Motivo:** {r['Mecanismo']}")
                        if pd.notna(r["Fuente"]):
                            st.caption(f"Fuente: {r['Fuente']}")
                    else:
                        st.write("Combinación negativa registrada en la base de datos.")
        else:
            st.info("No hay incompatibilidades registradas.")

    if pd.notna(fila["Observaciones"]):
        st.divider()
        st.info(f"📝 {fila['Observaciones']}")


# --- TAB 2: POR ESTACIÓN ---
with tab2:
    estacion_sel = st.selectbox(
        "¿Qué estación querés planificar?",
        ["Verano", "Otoño", "Invierno", "Primavera"]
    )

    st.subheader(f"Cultivos para sembrar en {estacion_sel}")

    resultado = cultivos[cultivos["Estacion_siembra"].str.contains(estacion_sel, na=False)]

    if resultado.empty:
        st.info("No hay cultivos registrados para esta estación.")
    else:
        for _, row in resultado.iterrows():
            with st.expander(f"🌾 {row['Nombre_comun']} — {row['Nombre_cientifico']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Tipo:** {row['Tipo']}")
                    st.write(f"**Familia:** {row['Familia']}")
                with col2:
                    st.write(f"**Req. hídrico:** {row['Req_hidrico']}")
                    st.write(f"**Req. nutricional:** {row['Req_nutricional']}")
                with col3:
                    st.write(f"**Región:** {row['Region_Uruguay']}")
                    st.write(f"**Sistema:** {row['Tipo_sistema']}")

                if pd.notna(row["Compatible"]):
                    st.write(f"**Compañeras:** {row['Compatible'].replace(';', ', ')}")
                if pd.notna(row["Observaciones"]):
                    st.caption(f"📝 {row['Observaciones']}")


# --- TAB 3: PLANTAS FUNCIONALES ---
with tab3:
    st.subheader("🌸 Plantas funcionales y aromáticas")
    st.caption("Plantas que cumplen roles específicos en el sistema: repelentes, atractoras de polinizadores, nematicidas, etc.")

    funcion_sel = st.multiselect(
        "Filtrar por función",
        funcionales["Funcion_principal"].unique().tolist(),
        default=[]
    )

    df_func = funcionales if not funcion_sel else funcionales[funcionales["Funcion_principal"].isin(funcion_sel)]

    for _, row in df_func.iterrows():
        with st.expander(f"🌼 {row['Nombre']} — {row['Nombre_cientifico']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Función principal:** {row['Funcion_principal']}")
                st.write(f"**Función secundaria:** {row['Funcion_secundaria']}")
                st.write(f"**Mecanismo:** {row['Mecanismo']}")
            with col2:
                st.write(f"**Atrae polinizadores:** {row['Atrae_polinizadores']}")
                if pd.notna(row["Polinizadores_especificos"]):
                    st.write(f"**Polinizadores:** {row['Polinizadores_especificos']}")
                if pd.notna(row["Control_plagas"]):
                    st.write(f"**Controla:** {row['Control_plagas']}")
            if pd.notna(row["Observaciones"]):
                st.caption(f"📝 {row['Observaciones']}")


# --- TAB 4: COMPATIBILIDADES ---
with tab4:
    st.subheader("🔍 Tabla de compatibilidades")

    relacion_sel = st.radio(
        "Mostrar",
        ["Todas", "Solo positivas", "Solo negativas"],
        horizontal=True
    )

    df_compat = compatibilidades.copy()
    if relacion_sel == "Solo positivas":
        df_compat = df_compat[df_compat["Relacion"] == "Positiva"]
    elif relacion_sel == "Solo negativas":
        df_compat = df_compat[df_compat["Relacion"] == "Negativa"]

    for _, row in df_compat.iterrows():
        icono = "✅" if row["Relacion"] == "Positiva" else "❌"
        with st.expander(f"{icono} {row['Especie_A']} + {row['Especie_B']} ({row['Intensidad']})"):
            st.write(f"**Mecanismo:** {row['Mecanismo']}")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Beneficio para {row['Especie_A']}:** {row['Beneficio_A']}")
            with col2:
                st.write(f"**Beneficio para {row['Especie_B']}:** {row['Beneficio_B']}")
            st.caption(f"Sistema: {row['Sistema']} · Fuente: {row['Fuente']}")
