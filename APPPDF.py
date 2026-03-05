import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import io
import os
from datetime import datetime

# Configuración de página optimizada
st.set_page_config(
    page_title="Converter - Imagen a PDF De Yan", 
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .main-header {
        animation: slideIn 0.8s ease-out;
        text-align: center;
        padding: 2rem 0;
    }
    
    .upload-zone {
        border: 3px dashed #4CAF50;
        border-radius: 20px;
        padding: 3rem;
        text-align: center;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        transition: all 0.3s ease;
    }
    
    .upload-zone:hover {
        border-color: #2196F3;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .metric-card {
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin: 0.5rem;
    }
    
    .metric-blue { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .metric-pink { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
    .metric-cyan { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
    .metric-gold { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); }
    
    .config-section {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .mobile-preview-container {
        max-width: 400px;
        margin: 0 auto;
        background: white;
        border-radius: 20px;
        padding: 1rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .preview-counter {
        text-align: center;
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    .instruction-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left: 4px solid #2196F3;
        padding: 1rem;
        border-radius: 0 10px 10px 0;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        color: #1565c0;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'processed_files' not in st.session_state:
    st.session_state.processed_files = 0
    st.session_state.total_size = 0
    st.session_state.current_preview = 0

# Header animado
st.markdown("""
<div class="main-header">
    <h1 style="font-size: 3.5rem; background: linear-gradient(45deg, #2196F3, #4CAF50); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        🚀 PDF Converter Yan
    </h1>
    <p style="font-size: 1.3rem; color: #666;">Imágenes coloridas con rotación manual y marca Yan</p>
</div>
""", unsafe_allow_html=True)

# Área de upload
st.markdown("""
<div class="upload-zone">
    <h2>📁 Arrastra tus imágenes aquí</h2>
    <p style="color: #666;">o haz clic para seleccionar archivos</p>
    <p style="font-size: 0.9rem; color: #999;">Máximo 50 archivos • Hasta 50 MB cada uno</p>
</div>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "", 
    type=['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'webp', 'gif', 'ico'],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

# CONFIGURACIÓN
st.markdown("### ⚙️ Configuración de Conversión")

with st.container():
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        max_files = st.number_input("Máximo archivos", 1, 50, 20)
        quality = st.slider("Calidad PDF (DPI)", 50, 300, 150)
        
        # UNIFICADO: Compresión y optimización en un solo control
        compression_level = st.select_slider(
            "📦 Nivel de optimización",
            options=["Rápido", "Equilibrado", "Calidad máxima"],
            value="Equilibrado",
            help="Rápido = archivos más pequeños, Calidad = archivos más grandes"
        )
    
    with col2:
        max_file_size = st.number_input("Tamaño máx. (MB)", 1, 100, 50)
        margin = st.slider("Margen (mm)", 0, 50, 0)
        
        # UNIFICADO: Tamaño máximo según nivel de optimización
        max_dimension_map = {"Rápido": 1500, "Equilibrado": 2000, "Calidad máxima": 3000}
        max_dimension = max_dimension_map[compression_level]
    
    with col3:
        # UNIFICADO: Estilo de color con emoji incluido
        style_options = {
            "Natural 🖼️": {"saturation": 1.0, "contrast": 1.0, "brightness": 1.0, "tint": None},
            "Clase/Escolar (Azul) ✏️": {"saturation": 1.2, "contrast": 1.1, "brightness": 1.05, "tint": (180, 200, 255)},
            "Regalo (Rosa) 🎁": {"saturation": 1.3, "contrast": 1.0, "brightness": 1.1, "tint": (255, 200, 220)},
            "Trabajo (Verde) 💼": {"saturation": 1.1, "contrast": 1.15, "brightness": 1.0, "tint": (200, 255, 220)},
            "Fiesta (Dorado) 🎉": {"saturation": 1.4, "contrast": 1.2, "brightness": 1.15, "tint": (255, 235, 180)}
        }
        
        sheet_format = st.selectbox("🎨 Estilo de Color", list(style_options.keys()))
        color_profile = style_options[sheet_format]
        
        page_size = st.selectbox(
            "Tamaño de página",
            ["Original", "A4", "Carta", "Personalizado"]
        )
    
    # Fila 2: Rotación manual, nombre y salida
    col4, col5, col6 = st.columns(3)
    
    custom_width, custom_height = 210, 297
    with col4:
        if page_size == "Personalizado":
            st.markdown("**Dimensiones personalizadas:**")
            c1, c2 = st.columns(2)
            with c1:
                custom_width = st.number_input("Ancho (mm)", 50, 500, 210)
            with c2:
                custom_height = st.number_input("Alto (mm)", 50, 500, 297)
        
        st.markdown("**🎚️ Rotación Manual**")
        
        # INSTRUCCIONES debajo del título
        st.markdown("""
        <div class="instruction-box">
            💡 <b>Instrucciones:</b><br>
            • <b>0°</b> = Sin rotación<br>
            • <b>Positivo (+)</b> = Sentido horario ↻<br>
            • <b>Negativo (-)</b> = Sentido antihorario ↺<br>
            • Usa valores como 90, 180, 270 para giros exactos
        </div>
        """, unsafe_allow_html=True)
        
        rotation_degrees = st.slider("Grados", -360, 360, 0, 90,
                                   help="Valores positivos = sentido horario, negativos = antihorario")
        if rotation_degrees != 0:
            direction = "horario ↻" if rotation_degrees > 0 else "antihorario ↺"
            st.info(f"🔄 Rotación: {abs(rotation_degrees)}° {direction}")
    
    with col5:
        project_name = st.text_input(
            "📝 Nombre del proyecto",
            value=f"Proyecto_Yan_{datetime.now().strftime('%Y%m%d')}",
            help="Nombre para guardar tu PDF"
        )
    
    with col6:
        output_format = st.radio(
            "📦 Formato de salida",
            ["PDF único", "PDFs separados", "Ambos"],
            horizontal=False
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

# UNIFICADA: Función única para aplicar color
def apply_color_style(img, profile):
    """Aplica el perfil de color a la imagen"""
    if profile["saturation"] != 1.0:
        img = ImageEnhance.Color(img).enhance(profile["saturation"])
    if profile["contrast"] != 1.0:
        img = ImageEnhance.Contrast(img).enhance(profile["contrast"])
    if profile["brightness"] != 1.0:
        img = ImageEnhance.Brightness(img).enhance(profile["brightness"])
    if profile["tint"]:
        tint_overlay = Image.new('RGB', img.size, profile["tint"])
        img = Image.blend(img, tint_overlay, 0.15)
    return img

# UNIFICADA: Función única para redimensionar (combina optimización y página)
def resize_image(img, page_mode, custom_w=None, custom_h=None, margin_mm=0):
    """Redimensiona imagen según configuración"""
    # Primero: optimización automática de tamaño
    max_dim = max(img.size)
    limit = max_dimension_map[compression_level]
    if max_dim > limit:
        scale = limit / max_dim
        new_size = (int(img.width * scale), int(img.height * scale))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
    
    # Segundo: ajuste a tamaño de página si aplica
    if page_mode != "Original":
        mm_to_px = 3.7795275591
        if page_mode == "A4":
            target_w, target_h = int(210 * mm_to_px), int(297 * mm_to_px)
        elif page_mode == "Carta":
            target_w, target_h = int(216 * mm_to_px), int(279 * mm_to_px)
        else:  # Personalizado
            target_w, target_h = int(custom_w * mm_to_px), int(custom_h * mm_to_px)
        
        margin_px = int(margin_mm * mm_to_px)
        target_w -= 2 * margin_px
        target_h -= 2 * margin_px
        
        scale_w = target_w / img.width if img.width > 0 else 1
        scale_h = target_h / img.height if img.height > 0 else 1
        scale = min(scale_w, scale_h, 1.0)
        
        if scale < 1.0:
            new_size = (max(int(img.width * scale), 1), max(int(img.height * scale), 1))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
    
    return img

# UNIFICADA: Función única para convertir a RGB
def convert_to_rgb(img):
    """Convierte cualquier modo de imagen a RGB"""
    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        if img.mode in ('RGBA', 'LA'):
            background.paste(img, mask=img.split()[-1])
        else:
            background.paste(img)
        return background
    elif img.mode != 'RGB':
        return img.convert('RGB')
    return img

# UNIFICADA: Función única para marca de agua
def add_watermark(img, text="Yan"):
    """Añade marca de agua adaptativa"""
    watermarked = img.copy()
    draw = ImageDraw.Draw(watermarked)
    
    # Tamaño de fuente adaptativo
    font_size = max(30, min(img.width, img.height) // 20)
    try:
        font = ImageFont.truetype("arialbd.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    x = img.width - text_width - 20
    y = img.height - text_height - 20
    
    # Sombra sutil
    for offset in range(2):
        draw.text((x+offset, y+offset), text, font=font, fill=(0, 0, 0, 80))
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 220))
    
    return watermarked

# UNIFICADA: Obtener calidad de compresión
def get_quality_settings():
    """Retorna calidad JPEG y DPI según nivel seleccionado"""
    settings = {
        "Rápido": {"jpeg": 70, "dpi": 100},
        "Equilibrado": {"jpeg": 85, "dpi": 150},
        "Calidad máxima": {"jpeg": 95, "dpi": 300}
    }
    return settings[compression_level]

# Procesamiento
if uploaded_files:
    if len(uploaded_files) > max_files:
        st.error(f"❌ Demasiados archivos. Máximo permitido: {max_files}")
    else:
        valid_files = []
        total_size = 0
        
        for file in uploaded_files:
            size_mb = len(file.getvalue()) / (1024 * 1024)
            if size_mb > max_file_size:
                st.warning(f"⚠️ {file.name} excede el límite de {max_file_size}MB")
            else:
                valid_files.append(file)
                total_size += size_mb
        
        if valid_files:
            # Dashboard de métricas
            st.markdown("### 📈 Estado de Conversión")
            
            progress_cols = st.columns(4)
            with progress_cols[0]:
                st.markdown(f"""
                <div class="metric-card metric-blue">
                    <h3>{len(valid_files)}</h3>
                    <p>Archivos</p>
                </div>
                """, unsafe_allow_html=True)
            
            with progress_cols[1]:
                st.markdown(f"""
                <div class="metric-card metric-pink">
                    <h3>{total_size:.1f} MB</h3>
                    <p>Tamaño total</p>
                </div>
                """, unsafe_allow_html=True)
            
            with progress_cols[2]:
                emoji = sheet_format.split()[-1]
                st.markdown(f"""
                <div class="metric-card metric-cyan">
                    <h3>{emoji}</h3>
                    <p>{sheet_format.split('(')[0].strip()}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with progress_cols[3]:
                if rotation_degrees != 0:
                    rot_emoji = "🔄"
                    rot_text = f"{rotation_degrees}°"
                else:
                    rot_emoji = "⬆️"
                    rot_text = "Sin rotar"
                
                st.markdown(f"""
                <div class="metric-card metric-gold">
                    <h3>{rot_emoji}</h3>
                    <p>{rot_text}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Procesar imágenes
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            images_data = []
            quality_settings = get_quality_settings()
            
            for idx, file in enumerate(valid_files):
                try:
                    image = Image.open(file)
                    original_size = image.size
                    
                    # PIPELINE UNIFICADO: Rotar → Redimensionar → Color → RGB → Marca
                    if rotation_degrees != 0:
                        image = image.rotate(-rotation_degrees, expand=True)
                    
                    image = resize_image(image, page_size, custom_width, custom_height, margin)
                    image = apply_color_style(image, color_profile)
                    image = convert_to_rgb(image)
                    image = add_watermark(image, "Yan")
                    
                    images_data.append({
                        'image': image,
                        'name': os.path.splitext(file.name)[0],
                        'original_size': original_size,
                        'rotation': rotation_degrees
                    })
                    
                    progress = (idx + 1) / len(valid_files)
                    progress_bar.progress(int(progress * 100))
                    status_text.text(f"Procesando {idx + 1} de {len(valid_files)}... {sheet_format.split('(')[0]}")
                    
                except Exception as e:
                    st.error(f"Error con {file.name}: {str(e)}")
            
            progress_bar.empty()
            
            # Calcular ahorro
            original_pixels = sum(d['original_size'][0] * d['original_size'][1] for d in images_data)
            final_pixels = sum(d['image'].size[0] * d['image'].size[1] for d in images_data)
            savings = (1 - final_pixels/original_pixels) * 100 if original_pixels > 0 else 0
            
            status_text.success(f"✅ {len(images_data)} imágenes procesadas • Optimización: {savings:.0f}% más ligero")
            
            # VISTA PREVIA MÓVIL
            if images_data:
                st.markdown("### 👁️ Vista Previa (Formato Móvil)")
                
                total_images = len(images_data)
                
                # Controles de navegación
                nav_col1, nav_col2, nav_col3 = st.columns([1, 3, 1])
                
                with nav_col1:
                    if st.button("⬅️ Anterior", disabled=total_images <= 1):
                        st.session_state.current_preview = max(0, st.session_state.current_preview - 1)
                
                with nav_col2:
                    current_idx = st.session_state.current_preview % total_images
                    current_data = images_data[current_idx]
                    
                    st.markdown(f'<div class="mobile-preview-container">', unsafe_allow_html=True)
                    st.markdown(f'<div class="preview-counter">📷 Imagen {current_idx + 1} de {total_images} (Desliza o usa botones)</div>', unsafe_allow_html=True)
                    
                    st.image(current_data['image'], use_container_width=True)
                    
                    if current_data['rotation'] != 0:
                        direction = "horario ↻" if current_data['rotation'] > 0 else "antihorario ↺"
                        st.info(f"🔄 Imagen rotada {abs(current_data['rotation'])}° {direction}")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Slider de navegación
                    if total_images > 1:
                        selected = st.slider("Navegar imágenes", 1, total_images, current_idx + 1)
                        st.session_state.current_preview = selected - 1
                
                with nav_col3:
                    if st.button("Siguiente ➡️", disabled=total_images <= 1):
                        st.session_state.current_preview = min(total_images - 1, st.session_state.current_preview + 1)
                
                # Resumen del proceso
                st.markdown("### 📋 Resumen del Proceso")
                
                sum_col1, sum_col2 = st.columns(2)
                
                with sum_col1:
                    st.markdown("#### 🎨 Ajustes aplicados")
                    changes = []
                    if "Natural" not in sheet_format:
                        changes.append(f"✅ Color: {sheet_format.split('(')[0]}")
                    if rotation_degrees != 0:
                        direction = "horario ↻" if rotation_degrees > 0 else "antihorario ↺"
                        changes.append(f"✅ Rotación: {abs(rotation_degrees)}° {direction}")
                    changes.append("✅ Marca de agua Yan")
                    
                    for change in changes:
                        st.success(change)
                
                with sum_col2:
                    st.markdown("#### 📊 Estadísticas")
                    st.code(f"""
Total imágenes:     {len(images_data)}
Tamaño original:    {original_pixels/1000000:.1f} MPix
Tamaño final:       {final_pixels/1000000:.1f} MPix
Ahorro:             {savings:.0f}%
Calidad PDF:        {quality_settings['dpi']} DPI
Compresión:         {compression_level}
                    """)
                    
                    if len(images_data) > 1:
                        st.markdown("#### 🗂️ Archivos incluidos")
                        for i, data in enumerate(images_data, 1):
                            rotated = " 🔄" if data['rotation'] != 0 else ""
                            st.caption(f"{i}. {data['name']}{rotated} ({data['image'].size[0]}×{data['image'].size[1]})")
            
            # Botón de generación
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🚀 GENERAR PDF(S) OPTIMIZADO", key="convert", use_container_width=True):
                with st.spinner(f"Creando PDF con compresión {compression_level}..."):
                    
                    final_images = [d['image'] for d in images_data]
                    
                    if output_format in ["PDF único", "Ambos"] and final_images:
                        pdf_buffer = io.BytesIO()
                        
                        final_images[0].save(
                            pdf_buffer, 
                            'PDF', 
                            resolution=quality_settings['dpi'],
                            save_all=True,
                            append_images=final_images[1:],
                            quality=quality_settings['jpeg']
                        )
                        pdf_buffer.seek(0)
                        
                        pdf_size_mb = len(pdf_buffer.getvalue()) / (1024 * 1024)
                        
                        st.session_state.processed_files += len(images_data)
                        st.session_state.total_size += total_size
                        
                        st.balloons()
                        
                        rot_info = f"Rotación: {rotation_degrees}°" if rotation_degrees != 0 else "Sin rotación"
                        
                        st.markdown(f"""
                        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white; margin: 1rem 0;">
                            <h2>✨ ¡PDF Optimizado Creado! ✨</h2>
                            <p>Estilo: <b>{sheet_format.split('(')[0]}</b> • {len(final_images)} páginas</p>
                            <p style="font-size: 0.9rem; opacity: 0.9;">
                                {rot_info} • 
                                Tamaño PDF: {pdf_size_mb:.1f} MB •
                                Compresión: {compression_level} •
                                Marca Yan™
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.download_button(
                            label=f"📥 Descargar {project_name}.pdf ({pdf_size_mb:.1f} MB)",
                            data=pdf_buffer,
                            file_name=f"{project_name}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    
                    if output_format in ["PDFs separados", "Ambos"]:
                        st.markdown("### 📄 Archivos Individuales Optimizados")
                        
                        individual_cols = st.columns(3)
                        for idx, data in enumerate(images_data):
                            with individual_cols[idx % 3]:
                                pdf_individual = io.BytesIO()
                                data['image'].save(pdf_individual, 'PDF', 
                                                 resolution=quality_settings['dpi'],
                                                 quality=quality_settings['jpeg'])
                                pdf_individual.seek(0)
                                
                                ind_size_kb = len(pdf_individual.getvalue()) / 1024
                                
                                st.download_button(
                                    label=f"📄 {data['name'][:15]}..._Yan.pdf ({ind_size_kb:.0f} KB)",
                                    data=pdf_individual,
                                    file_name=f"{data['name']}_Yan.pdf",
                                    mime="application/pdf",
                                    key=f"indiv_{idx}"
                                )

# Estadísticas en sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📊 Estadísticas de Uso")
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric("Procesados", st.session_state.processed_files)
    with col_stat2:
        st.metric("MB totales", f"{st.session_state.total_size:.1f}")
    
    st.markdown("---")
    st.info("💡 **Tip:** Activa 'Optimizar imágenes' y usa compresión 'Alta' o 'Máxima' para PDFs más ligeros. La rotación manual permite ajustes precisos de -360° a 360°.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🚀 PDF Converter De Yan | Vista previa móvil, rotación manual y optimización inteligente</p>
    <p style="font-size: 0.8rem;">5 estilos de color • Rotación -360° a 360° • Compresión ajustable • Vista previa tipo carrusel • Marca Yan™</p>
</div>
""", unsafe_allow_html=True)