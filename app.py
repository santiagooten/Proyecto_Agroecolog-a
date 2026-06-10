import streamlit as st
import pandas as pd

st.set_page_config(page_title="Policultivos Uruguay", page_icon="🌱", layout="wide")

# --- CSS PERSONALIZADO ---
st.markdown("""
<style>
    .stApp {
        background-color: #f9f6f0;
    }
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
    [data-testid="stMetric"] {
        background-color: #e8f0e4;
        border-radius: 10px;
        padding: 12px 16px;
        border-left: 4px solid #4a7c59;
    }
    .stSelectbox > div > div {
        border-color: #4a7c59;
        border-radius: 8px;
    }
    hr {
        border-color: #c5d9be;
    }
    .stInfo {
        background-color: #e8f0e4;
        border-left-color: #4a7c59;
    }
</style>
""", unsafe_allow_html=True)

# --- BANNER ---
st.markdown("""
<div style="
    background: linear-gradient(135deg, #2d5a27 0%, #4a7c59 60%, #7fb069 100%);
    border-radius: 16px;
    padding: 40px 48px;
    margin-bottom: 28px;
    color: white;
">
    <div style="font-size: 2.4rem; font-weight: 700; letter-spacing: -0.5px;">
        🌱 Planificador de Policultivos
    </div>
    <div style="font-size: 1.1rem; opacity: 0.9; font-weight: 400; margin-top: 8px;">
        Herramienta agroecológica para Uruguay · Asociaciones de cultivos basadas en evidencia científica
    </div>
    <div style="display: flex; gap: 20px; margin-top: 12px; font-size: 0.9rem; opacity: 0.8;">
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
    xl = pd.read_excel("Base_Datos_Agroecologica_Uruguay_V3.xlsx", sheet_name=None)
    return xl

datos = cargar_datos()
cultivos = datos["Cultivos_Horticolas"]
funcionales = datos["Plantas_Funcionales"]
agroforestales = datos["Agroforestales"]
silvopastoril = datos["Silvopastoril"]
compatibilidades = datos["Compatibilidades"]

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌿 Por planta",
    "📅 Por estación",
    "🌾 Por sistema",
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
        st.caption(f"{len(resultado)} cultivos encontrados")
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


# --- TAB 3: POR SISTEMA ---
with tab3:
    sub1, sub2, sub3 = st.tabs([
        "🥬 Hortícola",
        "🌳 Agroforestal",
        "🐄 Silvopastoril"
    ])

    with sub1:
        sistema_sel = st.radio(
            "Tipo de sistema hortícola",
            ["Todos", "Hortícola intensivo", "Hortícola", "Hortícola;Policultivo"],
            horizontal=True
        )

        if sistema_sel == "Todos":
            df_sist = cultivos.copy()
        else:
            df_sist = cultivos[cultivos["Tipo_sistema"].str.contains(sistema_sel, na=False)]

        st.caption(f"{len(df_sist)} cultivos encontrados")

        for _, row in df_sist.iterrows():
            with st.expander(f"🌾 {row['Nombre_comun']} — *{row['Nombre_cientifico']}*"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Tipo:** {row['Tipo']}")
                    st.write(f"**Función ecológica:** {row['Funcion_ecologica']}")
                    st.write(f"**Familia:** {row['Familia']}")
                with col2:
                    st.write(f"**Req. hídrico:** {row['Req_hidrico']}")
                    st.write(f"**Req. nutricional:** {row['Req_nutricional']}")
                    st.write(f"**Estación:** {row['Estacion_siembra']}")
                with col3:
                    st.write(f"**Región:** {row['Region_Uruguay']}")
                    st.metric("Temp. óptima", f"{row['Temp_optima_C']}°C")
                if pd.notna(row["Compatible"]):
                    st.write(f"**Compañeras:** {row['Compatible'].replace(';', ', ')}")
                if pd.notna(row["Incompatible"]):
                    st.write(f"**Incompatibles:** {row['Incompatible'].replace(';', ', ')}")
                if pd.notna(row["Observaciones"]):
                    st.caption(f"📝 {row['Observaciones']}")

    with sub2:
        funcion_agro = st.multiselect(
            "Filtrar por función",
            agroforestales["Funcion_principal"].unique().tolist(),
            default=[]
        )
        region_agro = st.multiselect(
            "Filtrar por región",
            ["Sur", "Litoral", "Norte", "Este", "Todo Uruguay"],
            default=[]
        )

        df_agro = agroforestales.copy()
        if funcion_agro:
            df_agro = df_agro[df_agro["Funcion_principal"].isin(funcion_agro)]
        if region_agro:
            df_agro = df_agro[df_agro["Region_Uruguay"].apply(
                lambda x: any(r in str(x) for r in region_agro)
            )]

        st.caption(f"{len(df_agro)} especies encontradas")

        for _, row in df_agro.iterrows():
            nativo = "🇺🇾 Nativo" if row["Nativo"] == "Sí" else "🌍 Introducido"
            with st.expander(f"🌳 {row['Nombre']} — *{row['Nombre_cientifico']}* · {nativo}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Función principal:** {row['Funcion_principal']}")
                    st.write(f"**Funciones secundarias:** {row['Funciones_secundarias']}")
                    st.write(f"**Sistema productivo:** {row['Sistema_productivo']}")
                with col2:
                    st.write(f"**Altura adulto:** {row['Altura_adulto_m']} m")
                    st.write(f"**Velocidad de crecimiento:** {row['Velocidad_crecimiento']}")
                    st.write(f"**Distancia mín. al cultivo:** {row['Distancia_min_cultivo_m']} m")
                with col3:
                    st.write(f"**Sombra (1-3):** {row['Sombra_1_3']}")
                    st.write(f"**Fauna asociada:** {row['Fauna_asociada']}")
                    st.write(f"**Región:** {row['Region_Uruguay']}")
                if pd.notna(row["Observaciones"]):
                    st.caption(f"📝 {row['Observaciones']}")

    with sub3:
        animal_sel = st.multiselect(
            "Filtrar por animal",
            silvopastoril["Animal"].unique().tolist(),
            default=[]
        )

        df_silvo = silvopastoril.copy()
        if animal_sel:
            df_silvo = df_silvo[df_silvo["Animal"].isin(animal_sel)]

        st.caption(f"{len(df_silvo)} sistemas encontrados")

        for _, row in df_silvo.iterrows():
            with st.expander(f"🐄 {row['Arbol']} + {row['Animal']} — {row['Tipo_produccion']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Árbol:** {row['Arbol']} (*{row['Nombre_cientifico']}*)")
                    st.write(f"**Animal:** {row['Animal']}")
                    st.write(f"**Producción:** {row['Tipo_produccion']}")
                with col2:
                    st.write(f"**Sombra verano:** {row['Sombra_verano']}")
                    st.write(f"**Resistencia sequía:** {row['Resistencia_sequia']}")
                    st.write(f"**Árboles/ha:** {row['Arboles_por_ha']}")
                with col3:
                    st.write(f"**Región:** {row['Region_Uruguay']}")
                    st.write(f"**Época implantación:** {row['Epoca_implantacion']}")
                    st.write(f"**Función ecológica:** {row['Funcion_ecologica']}")
                st.info(f"💡 {row['Beneficio_productivo']}")
                if pd.notna(row["Observaciones"]):
                    st.caption(f"📝 {row['Observaciones']}")


# --- TAB 4: PLANTAS FUNCIONALES ---
with tab4:
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


# --- TAB 5: COMPATIBILIDADES ---
with tab5:
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
