import streamlit as st
import pandas as pd

st.set_page_config(page_title="Policultivos Uruguay", page_icon="🌱", layout="wide")

# --- CSS PERSONALIZADO ---
st.markdown("""
<style>
    /* Paleta verde/tierra */
    :root {
        --verde-oscuro: #2d5a27;
        --verde-medio: #4a7c59;
        --verde-claro: #7fb069;
        --tierra: #8b6914;
        --crema: #f5f0e8;
        --marron: #5c4033;
    }

    /* Fondo general */
    .stApp {
        background-color: #f9f6f0;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #e8f0e4;
        padding: 6px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 16px;
        color: #2d5a27;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2d5a27 !important;
        color: white !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #e8f0e4;
        border-radius: 8px;
        color: #2d5a27;
        font-weight: 500;
    }
    .streamlit-expanderContent {
        border-left: 3px solid #7fb069;
        padding-left: 12px;
    }

    /* Métricas */
    [data-testid="stMetric"] {
        background-color: #e8f0e4;
        border-radius: 10px;
        padding: 12px 16px;
        border-left: 4px solid #4a7c59;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        border-color: #4a7c59;
        border-radius: 8px;
    }

    /* Divider */
    hr {
        border-color: #c5d9be;
    }

    /* Info boxes */
    .stInfo {
        background-color: #e8f0e4;
        border-left-color: #4a7c59;
    }
</style>
""", unsafe_allow_html=True)


# --- BANNER DE CABECERA ---
st.markdown("""
<div style="
    background: linear-gradient(135deg, #2d5a27 0%, #4a7c59 60%, #7fb069 100%);
    border-radius: 16px;
    padding: 40px 48px;
    margin-bottom: 28px;
    color: white;
    display: flex;
    flex-direction: column;
    gap: 10px;
">
    <div style="font-size: 2.4rem; font-weight: 700; letter-spacing: -0.5px;">
        🌱 Planificador de Policultivos
    </div>
    <div style="font-size: 1.1rem; opacity: 0.9; font-weight: 400;">
        Herramienta agroecológica para Uruguay · Asociaciones de cultivos basadas en evidencia científica
    </div>
    <div style="display: flex; gap: 20px; margin-top: 8px; font-size: 0.9rem; opacity: 0.8;">
        <span>🌿 Cultivos hortícolas</span>
        <span>🌸 Plantas funcionales</span>
        <span>🌳 Sistemas agroforestales</span>
        <span>🔍 Compatibilidades</span>
    </div>
</div>
""", unsafe_allow_html=True)


# --- DATOS ---
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
        planta_sel = st.selectbox("Elegí un cultivo", cultivos["Nombre_comun"].tolist())

    fila = cultivos[cultivos["Nombre_comun"] == planta_sel].iloc[0]

    with col2:
        region = fila["Region_Uruguay"] if pd.notna(fila["Region_Uruguay"]) else "—"
        estacion = fila["Estacion_siembra"] if pd.notna(fila["Estacion_siembra"]) else "—"
        st.markdown(f"### {planta_sel}")
        st.markdown(f"*{fila['Nombre_cientifico']}* · {fila['Familia']}")
        st.caption(f"📍 {region} · 🗓️ Siembra: {estacion}")

    st.divider()

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("🌡️ Temp. mínima", f"{fila['Temp_min_C']}°C")
    with col_b:
        st.metric("✅ Temp. óptima", f"{fila['Temp_optima_C']}°C")
    with col_c:
        st.metric("🔥 Temp. máxima", f"{fila['Temp_max_C']}°C")

    st.divider()

    col_comp, col_incomp = st.columns(2)

    with col_comp:
        st.markdown("#### ✅ Compañeras ideales")
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
        st.markdown("#### ❌ Incompatibles")
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

    st.markdown(f"#### Cultivos para sembrar en {estacion_sel}")
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
    st.markdown("#### 🌸 Plantas funcionales y aromáticas")
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
    st.markdown("#### 🔍 Tabla de compatibilidades")

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
