import streamlit as st
import pandas as pd
import os

# =========================
# CONFIGURACIÓN
# =========================
st.set_page_config(page_title="Observatorio CRC", layout="wide")

st.title("📊 Observatorio CRC")

# =========================
# CARGA DE DATOS
# =========================
ruta = "observatorio.csv"

if not os.path.exists(ruta):
    st.error("❌ No se encontró el archivo observatorio.csv. Verifica que esté en el repositorio.")
    st.stop()

df = pd.read_csv(ruta)

# =========================
# RESUMEN POR CANAL
# =========================
st.subheader("📊 Resumen por canal")

resumen = df.groupby("canal").agg({
    "indice": "mean",
    "video": "count"
}).reset_index()

def nivel(x):
    if x > 0.7:
        return "ALTO"
    elif x > 0.4:
        return "MEDIO"
    else:
        return "BAJO"

resumen["nivel"] = resumen["indice"].apply(nivel)

def color(n):
    if n == "ALTO":
        return "🟢"
    elif n == "MEDIO":
        return "🟡"
    return "🔴"

resumen["estado"] = resumen["nivel"].apply(color)

st.dataframe(resumen, use_container_width=True)

# =========================
# GRÁFICO
# =========================
st.subheader("📈 Comparación de pluralismo")

st.bar_chart(resumen.set_index("canal")["indice"])

# =========================
# INTERPRETACIÓN AUTOMÁTICA
# =========================
st.subheader("🧠 Interpretación automática")

for _, row in resumen.iterrows():

    canal = row["canal"]
    indice = round(row["indice"], 3)
    nivel_val = row["nivel"]

    if nivel_val == "BAJO":
        st.error(f"""
🔴 {canal.upper()} presenta pluralismo BAJO ({indice})

Existe concentración de la información en pocos actores,
lo que reduce la diversidad de voces y puede afectar el equilibrio informativo.
""")

    elif nivel_val == "MEDIO":
        st.warning(f"""
🟡 {canal.upper()} presenta pluralismo MEDIO ({indice})

Se observa diversidad de actores, pero con predominio de algunos.
""")

    else:
        st.success(f"""
🟢 {canal.upper()} presenta pluralismo ALTO ({indice})

Existe equilibrio en la distribución de actores y mayor pluralidad informativa.
""")

# =========================
# ALERTAS CRC
# =========================
st.subheader("🚨 Alertas regulatorias")

for _, row in resumen.iterrows():

    if row["indice"] < 0.4:
        st.error(f"⚠️ Riesgo: {row['canal']} presenta posible déficit de pluralismo")

    elif row["indice"] < 0.6:
        st.warning(f"🔍 Seguimiento: {row['canal']} requiere monitoreo")

    else:
        st.success(f"✅ {row['canal']} sin alertas")

# =========================
# DETALLE POR VIDEO
# =========================
st.subheader("📁 Detalle por video")

st.dataframe(df, use_container_width=True)
