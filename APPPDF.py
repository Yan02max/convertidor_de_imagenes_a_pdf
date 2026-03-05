import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import io
import os
from datetime import datetime

st.set_page_config(
    page_title="PDF Yan - Simple", 
    page_icon="🚀",
    layout="centered"
)

# CSS mínimo
st.markdown("""
<style>
    .main-title { text-align: center; color: #2196F3; margin-bottom: 0; }
    .subtitle { text-align: center; color: #666; font-size: 1rem; margin-top: 0; }
    .stButton>button { width: 100%; background: linear-gradient(45deg, #2196F3, #4CAF50); color: white; font-size: 1.2rem; padding: 1rem; border-radius: 10px; }
    .preview-box { background: white; border-radius: 15px; padding: 1rem; box-shadow: 0 4px 10px rgba(0,0,0,0.1); max-width: 350px; margin: 0 auto; }
    #MainMenu, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Header simple
st.markdown("<h1 class='main-title'>🚀 PDF Yan</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Imágenes → PDF con estilo</p>", unsafe_allow_html=True)

# Upload
st.markdown("### 📁 Selecciona imágenes")
uploaded_files = st.file_uploader(
    "Arrastra o haz clic", 
    type=['png', 'jpg', 'jpeg'],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

if uploaded_files:
    # Solo 3 controles esenciales
    st.markdown("### ⚙️ Ajustes rápidos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Rotación simplificada: solo 4 opciones comunes
        rotation = st.selectbox(
            "🔄 Girar",
            ["No girar", "90° derecha", "180°", "90° izquierda"],
            index=0
        )
        
        # Color simplificado: 3 opciones
        color_style = st.selectbox(
            "🎨 Color",
            ["Normal", "Más vivo", "Blanco y negro"],
            index=0
        )
    
    with col2:
        # Calidad simplificada: 2 opciones
        calidad = st.radio(
            "📦 Calidad",
            ["Buena (rápido)", "Alta (pesado)"],
            index=0
        )
        
        # Nombre simple
        nombre = st.text_input("📝 Nombre", f"PDF_Yan_{datetime.now().strftime('%d%m%Y')}")
    
    # Procesar solo la primera imagen para preview
    archivo = uploaded_files[0]
    imagen = Image.open(archivo)
    
    # Aplicar rotación
    rot_map = {
        "No girar": 0,
        "90° derecha": -90,
        "180°": 180,
        "90° izquierda": 90
    }
    if rot_map[rotation] != 0:
        imagen = imagen.rotate(rot_map[rotation], expand=True)
    
    # Aplicar color
    if color_style == "Más vivo":
        imagen = ImageEnhance.Color(imagen).enhance(1.3)
        imagen = ImageEnhance.Contrast(imagen).enhance(1.1)
    elif color_style == "Blanco y negro":
        imagen = imagen.convert('L').convert('RGB')
    
    # Redimensionar si es muy grande (optimización automática)
    max_size = 1500 if calidad == "Buena (rápido)" else 2500
    if max(imagen.size) > max_size:
        imagen.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
    
    # Marca de agua
    draw = ImageDraw.Draw(imagen)
    try:
        font = ImageFont.truetype("arialbd.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    # Esquina inferior derecha
    bbox = draw.textbbox((0,0), "Yan", font=font)
    w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
    draw.text((imagen.width-w-20, imagen.height-h-20), "Yan", font=font, fill=(255,255,255,200))
    
    # Vista previa móvil (una sola imagen representativa)
    st.markdown("### 👁️ Vista previa")
    st.markdown('<div class="preview-box">', unsafe_allow_html=True)
    st.image(imagen, use_container_width=True)
    st.caption(f"{archivo.name} • {len(uploaded_files)} archivo(s) total")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Botón único de acción
    if st.button("🚀 CREAR PDF"):
        with st.spinner("Creando..."):
            
            # Procesar todas las imágenes
            imagenes_finales = []
            dpi = 100 if calidad == "Buena (rápido)" else 200
            
            for file in uploaded_files:
                img = Image.open(file)
                
                # Misma rotación
                if rot_map[rotation] != 0:
                    img = img.rotate(rot_map[rotation], expand=True)
                
                # Mismo color
                if color_style == "Más vivo":
                    img = ImageEnhance.Color(img).enhance(1.3)
                    img = ImageEnhance.Contrast(img).enhance(1.1)
                elif color_style == "Blanco y negro":
                    img = img.convert('L').convert('RGB')
                
                # Mismo resize
                if max(img.size) > max_size:
                    img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                
                # Convertir y marca
                if img.mode in ('RGBA', 'P'):
                    fondo = Image.new('RGB', img.size, (255,255,255))
                    fondo.paste(img, mask=img.split()[-1] if img.mode=='RGBA' else None)
                    img = fondo
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Marca
                d = ImageDraw.Draw(img)
                try:
                    f = ImageFont.truetype("arialbd.ttf", max(30, min(img.width, img.height)//25))
                except:
                    f = ImageFont.load_default()
                bb = d.textbbox((0,0), "Yan", font=f)
                ww, hh = bb[2]-bb[0], bb[3]-bb[1]
                d.text((img.width-ww-15, img.height-hh-15), "Yan", font=f, fill=(255,255,255))
                
                imagenes_finales.append(img)
            
            # Crear PDF
            buffer = io.BytesIO()
            calidad_jpg = 75 if calidad == "Buena (rápido)" else 90
            
            imagenes_finales[0].save(
                buffer, 
                'PDF', 
                resolution=dpi,
                save_all=True,
                append_images=imagenes_finales[1:],
                quality=calidad_jpg
            )
            buffer.seek(0)
            
            st.success(f"✅ ¡PDF creado! {len(imagenes_finales)} páginas")
            st.download_button(
                label=f"📥 Descargar {nombre}.pdf",
                data=buffer,
                file_name=f"{nombre}.pdf",
                mime="application/pdf"
            )

# Footer mínimo
st.markdown("---")
st.markdown("<p style='text-align:center; color:#999; font-size:0.8rem;'>PDF Yan - Simple y rápido</p>", unsafe_allow_html=True)