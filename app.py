import streamlit as st
import pandas as pd
import joblib
import numpy as np
import base64

# Configuración de página al inicio
st.set_page_config(page_title="¿Cuánto Vale Dormir Aquí?", layout="wide")

# --- DISEÑO UI/UX AVANZADO ---
st.markdown(
    """
    <style>
    /* Fondo general y fuentes */
    .stApp {
        background-color: #f8fafd;
    }
    
    /* Estilo para los Headers de sección */
    h1, h2, h3 {
        color: #1e3a8a !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Contenedores de inputs (Cards) */
    [data-testid="stVerticalBlock"] > div:has(div.stNumberInput, div.stSelectbox) {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    
    /* Ajuste del botón primario */
    .stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        border: none;
        padding: 15px 0px;
        font-weight: 600;
        border-radius: 12px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4);
        transform: translateY(-2px);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# HEADER PRINCIPAL
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>🏨 ¿Cuánto Vale Dormir Aquí? </h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 1.1rem;'>Optimización de tarifas para hoteles</p>", unsafe_allow_html=True)

# CARGAR MODELOS
@st.cache_resource
def load_models():
    # Asegúrate de que los archivos estén en la misma carpeta
    modelo = joblib.load('modelo_hotel.pkl')
    preprocessor = joblib.load('preprocessor_hotel.pkl')
    return modelo, preprocessor

try:
    modelo, preprocessor = load_models()
    st.toast("✅ Modelos cargados correctamente", icon="🚀")
except:
    st.error("⚠️ Error al cargar los modelos. Verifica que 'modelo_hotel.pkl' y 'preprocessor_hotel.pkl' existan.")

# === ÁREA DE CONFIGURACIÓN ===
st.markdown("### ⚙️ Parámetros de Reserva")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("#### 🏢 Hotel y Fechas")
    hotel = st.selectbox("Tipo de Hotel", ['City Hotel', 'Resort Hotel'], key="hotel")
    lead_time = st.number_input("Días de adelanto", 0, 365, 30, key="lead")
    month = st.selectbox("Mes llegada", ['January','February','March','April','May','June',
                                        'July','August','September','October','November','December'], key="month")

    st.markdown("#### 👥 Ocupación")
    c1, c2, c3 = st.columns(3)
    adults = c1.number_input("Adultos", 1, 4, 2, key="adults")
    children = c2.number_input("Niños", 0, 4, 0, key="children")
    babies = c3.number_input("Bebés", 0, 2, 0, key="babies")

with col_right:
    st.markdown("#### 🏠 Detalles de Estancia")
    c1, c2 = st.columns(2)
    weekend = c1.number_input("Noches finde", 0, 8, 1, key="weekend")
    week = c2.number_input("Noches laboral", 0, 15, 2, key="week")
    
    st.markdown("#### 🛏️ Tipo de habitaciones")
    nombres_habitaciones = {
        'A': 'Básica', 'B': 'Básica mejorada', 'C': 'Estándar', 'D': 'Superior', 'E': 'Deluxe',
        'F': 'Deluxe', 'G': 'Premium', 'H': 'Premium+', 'L': 'Suite', 'P': 'Presidential'
    }
    room = st.selectbox(
        "Categoría de Habitación", 
        options=list(nombres_habitaciones.keys()),
        format_func=lambda x: nombres_habitaciones[x],
        key="room"
    )

    st.markdown("#### 💼 Estrategia Comercial")
    nombres_segmentos = {
        'Online TA': 'Agencias via Online', 'Offline TA/TO': 'Agencias de viajes',
        'Groups': 'Viajes por volumen (grupos)', 'Direct': 'Atencion directa', 'Corporate': 'Viajeros de negocios'
    }
    segment = st.selectbox(
        "Perfil de cliente", 
        options=list(nombres_segmentos.keys()),
        format_func=lambda x: nombres_segmentos[x],
        key="segment"
    )
    
    nombres_canales = {
        'GDS': 'Empresas de viajes por aplicativos', 'Direct': 'Canal directo al hotel', 'TA/TO': 'Canal de terceros'
    }
    channel = st.selectbox(
        "Canal de Marketing", 
        options=list(nombres_canales.keys()),
        format_func=lambda x: nombres_canales[x],
        key="channel"
    )

# BOTÓN DE ACCIÓN
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔮 CALCULAR PRECIO ÓPTIMO", type="primary", use_container_width=True):
    # Lógica de procesamiento
    input_data = {
        'hotel': hotel, 'lead_time': lead_time, 'arrival_date_month': month,
        'stays_in_weekend_nights': weekend, 'stays_in_week_nights': week,
        'reserved_room_type': room, 'market_segment': segment,
        'distribution_channel': channel, 'adults': adults,
        'children': children, 'babies': babies
    }
    
    input_df = pd.DataFrame([input_data])
    input_processed = preprocessor.transform(input_df)
    precio = modelo.predict(input_processed)[0]
    
    # RESULTADO CON UI PREMIUM
    st.markdown("---")
    
    # Animación estética
    # st.balloons()
    
    # Tarjeta de Precio mejorada
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #ffffff 0%, #f0f7ff 100%); padding: 40px; border-radius: 20px; border: 2px solid #3b82f6; box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.1); text-align: center;">
        <h2 style="color: #1e40af; margin-bottom: 10px; font-size: 1.5rem; text-transform: uppercase; letter-spacing: 2px;">
            Tarifa Sugerida
        </h2>
        <div style="font-size: 5rem; font-weight: 800; color: #1d4ed8; margin: 10px 0;">
            €{precio:.2f} <span style="font-size: 1.5rem; color: #64748b; font-weight: 400;">/ noche</span>
        </div>
        <div style="background-color: #dcfce7; display: inline-block; padding: 8px 20px; border-radius: 50px; color: #15803d; font-weight: 700; font-size: 1rem; border: 1px solid #bbf7d0;">
            ✓ Confianza del Modelo: ±13€ de precisión
        </div>
        <p style="margin-top: 20px; color: #64748b;">Esta tarifa maximiza la probabilidad de reserva según la demanda prevista para <b>{month}</b>.</p>
    </div>
    """, unsafe_allow_html=True)