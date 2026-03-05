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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin: 0.5rem;
    }
    
    .config-section {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Estilo móvil para vista previa */
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
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .instruction-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left: 4px solid #2196F3;
        padding: 1rem;
        border-radius: 0 10px 10px 0;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        color: #1565c0;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'preview_images' not in st.session_state:
    st.session_state.preview_images = []
    st.session_state.processed_files = 0
    st.session_state.total_size = 0
    st.session_state.current_preview = 0  # Para controlar qué imagen se muestra

# Header
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
        quality = st.slider("Calidad PDF (DPI)", 50, 300, 150, 
                          help="Valores más bajos = PDF más ligero")
        
        # Optimización de compresión
        compression_level = st.select_slider(
            "📦 Compresión PDF",
            options=["Mínima", "Baja", "Media", "Alta", "Máxima"],
            value="Media",
            help="Alta/Máxima = archivos más pequeños, calidad ligeramente reducida"
        )
    
    with col2:
        max_file_size = st.number_input("Tamaño máx. (MB)", 1, 100, 50)
        margin = st.slider("Margen (mm)", 0, 50, 0)
        
        # Optimización de imagen
        optimize_images = st.checkbox("⚡ Optimizar imágenes", value=True,
                                    help="Reduce tamaño manteniendo calidad aceptable")
        
        if optimize_images:
            max_dimension = st.number_input("Máx dimensión (px)", 800, 4000, 1920,
                                          help="Redimensiona imágenes grandes")
    
    with col3:
        sheet_format = st.selectbox(
            "🎨 Estilo de Color",
            ["Natural", "Clase/Escolar (Azul)", "Regalo (Rosa)", "Trabajo (Verde)", "Fiesta (Dorado)"]
        )
        
        page_size = st.selectbox(
            "Tamaño de página",
            ["Original", "A4", "Carta", "Personalizado"]
        )
    
    # Fila 2: Rotación manual con instrucciones debajo del título
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
        
        # Título de rotación
        st.markdown("**🎚️ Rotación Manual**")
        
        # INSTRUCCIONES DEBAJO DEL TÍTULO
        st.markdown("""
        <div class="instruction-box">
            💡 <b>Instrucciones:</b><br>
            • <b>0°</b> = Sin rotación<br>
            • <b>Positivo (+)</b> = Sentido horario ↻<br>
            • <b>Negativo (-)</b> = Sentido antihorario ↺<br>
            • Usa valores como 90, 180, 270 para giros exactos
        </div>
        """, unsafe_allow_html=True)
        
        rotation_degrees = st.slider("Grados", -360, 360, 0, 90)
        if rotation_degrees != 0:
            direction = "horario ↻" if rotation_degrees > 0 else "antihorario ↺"
            st.info(f"🔄 Rotación: {abs(rotation_degrees)}° {direction}")
    
    with col5:
        project_name = st.text_input(
            "📝 Nombre del proyecto",
            value=f"Proyecto_Yan_{datetime.now().strftime('%Y%m%d')}"
        )
    
    with col6:
        output_format = st.radio(
            "📦 Formato de salida",
            ["PDF único", "PDFs separados", "Ambos"],
            horizontal=False
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

def get_color_profile():
    """Retorna el perfil de color según el formato seleccionado"""
    profiles = {
        "Natural": {
            "saturation": 1.0,
            "contrast": 1.0,
            "brightness": 1.0,
            "tint": None,
            "emoji": "🖼️"
        },
        "Clase/Escolar (Azul)": {
            "saturation": 1.2,
            "contrast": 1.1,
            "brightness": 1.05,
            "tint": (180, 200, 255),
            "emoji": "✏️"
        },
        "Regalo (Rosa)": {
            "saturation": 1.3,
            "contrast": 1.0,
            "brightness": 1.1,
            "tint": (255, 200, 220),
            "emoji": "🎁"
        },
        "Trabajo (Verde)": {
            "saturation": 1.1,
            "contrast": 1.15,
            "brightness": 1.0,
            "tint": (200, 255, 220),
            "emoji": "💼"
        },
        "Fiesta (Dorado)": {
            "saturation": 1.4,
            "contrast": 1.2,
            "brightness": 1.15,
            "tint": (255, 235, 180),
            "emoji": "🎉"
        }
    }
    return profiles.get(sheet_format, profiles["Natural"])

def apply_color_profile(img, profile):
    """Aplica el perfil de color a la imagen"""
    if profile["saturation"] != 1.0:
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(profile["saturation"])
    
    if profile["contrast"] != 1.0:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(profile["contrast"])
    
    if profile["brightness"] != 1.0:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(profile["brightness"])
    
    if profile["tint"]:
        tint_overlay = Image.new('RGB', img.size, profile["tint"])
        img = Image.blend(img, tint_overlay, 0.15)
    
    return img

def get_sheet_emoji():
    profile = get_color_profile()
    return profile["emoji"]

def apply_rotation(img):
    """Aplica solo la rotación manual del usuario"""
    if rotation_degrees != 0:
        img = img.rotate(-rotation_degrees, expand=True)
    return img

def optimize_image_size(img, max_dim=1920):
    """Optimiza el tamaño de la imagen para PDF más ligero"""
    width, height = img.size
    max_current = max(width, height)
    
    if max_current > max_dim:
        scale = max_dim / max_current
        new_width = int(width * scale)
        new_height = int(height * scale)
        return img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    return img

def resize_to_page_size(img):
    """Redimensiona imagen según tamaño de página seleccionado"""
    if page_size == "Original":
        return img
    
    mm_to_px = 3.7795275591
    
    if page_size == "A4":
        target_w, target_h = int(210 * mm_to_px), int(297 * mm_to_px)
    elif page_size == "Carta":
        target_w, target_h = int(216 * mm_to_px), int(279 * mm_to_px)
    elif page_size == "Personalizado":
        target_w, target_h = int(custom_width * mm_to_px), int(custom_height * mm_to_px)
    else:
        return img
    
    margin_px = int(margin * mm_to_px)
    target_w -= 2 * margin_px
    target_h -= 2 * margin_px
    
    img_w, img_h = img.size
    scale_w = target_w / img_w if img_w > 0 else 1
    scale_h = target_h / img_h if img_h > 0 else 1
    scale = min(scale_w, scale_h, 1.0)
    
    new_w = max(int(img_w * scale), 1)
    new_h = max(int(img_h * scale), 1)
    
    return img.resize((new_w, new_h), Image.Resampling.LANCZOS)

def get_compression_quality():
    """Retorna calidad de compresión según nivel seleccionado"""
    compression_map = {
        "Mínima": 95,
        "Baja": 85,
        "Media": 75,
        "Alta": 60,
        "Máxima": 45
    }
    return compression_map.get(compression_level, 75)

def add_watermark_to_image(img, text="Yan"):
    """Añade marca de agua 'Yan' a la imagen"""
    watermarked = img.copy()
    draw = ImageDraw.Draw(watermarked)
    
    # Tamaño de fuente adaptativo según tamaño de imagen
    img_size = min(img.width, img.height)
    font_size = max(30, min(60, img_size // 20))
    
    try:
        font = ImageFont.truetype("arialbd.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = img.width - text_width - 30
    y = img.height - text_height - 30
    
    # Sombra más sutil
    for offset in range(2):
        draw.text((x+offset, y+offset), text, font=font, fill=(0, 0, 0, 80))
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 220))
    
    return watermarked

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
                <div class="metric-card">
                    <h3>{len(valid_files)}</h3>
                    <p>Archivos</p>
                </div>
                """, unsafe_allow_html=True)
            
            with progress_cols[1]:
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                    <h3>{total_size:.1f} MB</h3>
                    <p>Total</p>
                </div>
                """, unsafe_allow_html=True)
            
            with progress_cols[2]:
                profile = get_color_profile()
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                    <h3>{profile['emoji']}</h3>
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
                <div class="metric-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
                    <h3>{rot_emoji}</h3>
                    <p>{rot_text}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Procesar imágenes
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            images_data = []
            color_profile = get_color_profile()
            compression_quality = get_compression_quality()
            
            for idx, file in enumerate(valid_files):
                try:
                    image = Image.open(file)
                    original_size = image.size
                    
                    # PASO 1: Optimizar tamaño si está activado
                    if optimize_images:
                        image = optimize_image_size(image, max_dimension)
                    
                    # PASO 2: Aplicar rotación manual
                    image = apply_rotation(image)
                    
                    # PASO 3: Redimensionar
                    image = resize_to_page_size(image)
                    
                    # PASO 4: Aplicar perfil de color
                    image = apply_color_profile(image, color_profile)
                    
                    # PASO 5: Convertir a RGB
                    if image.mode in ('RGBA', 'LA', 'P'):
                        background = Image.new('RGB', image.size, (255, 255, 255))
                        if image.mode == 'P':
                            image = image.convert('RGBA')
                        if image.mode in ('RGBA', 'LA'):
                            background.paste(image, mask=image.split()[-1])
                        else:
                            background.paste(image)
                        image = background
                    elif image.mode != 'RGB':
                        image = image.convert('RGB')
                    
                    # PASO 6: Añadir marca de agua
                    image = add_watermark_to_image(image, "Yan")
                    
                    was_rotated = rotation_degrees != 0
                    
                    images_data.append({
                        'image': image,
                        'name': os.path.splitext(file.name)[0],
                        'original': file,
                        'original_size': original_size,
                        'was_rotated': was_rotated,
                        'rotation_applied': rotation_degrees,
                        'final_size': image.size
                    })
                    
                    progress = (idx + 1) / len(valid_files)
                    progress_bar.progress(int(progress * 100))
                    status_text.text(f"Procesando {idx + 1} de {len(valid_files)}... 🎨 {sheet_format} 🔄 {rotation_degrees}° ⚡ Compresión: {compression_level}")
                    
                except Exception as e:
                    st.error(f"Error con {file.name}: {str(e)}")
            
            progress_bar.empty()
            
            # Calcular ahorro de espacio
            original_pixels = sum(d['original_size'][0] * d['original_size'][1] for d in images_data)
            final_pixels = sum(d['final_size'][0] * d['final_size'][1] for d in images_data)
            savings = (1 - final_pixels/original_pixels) * 100 if original_pixels > 0 else 0
            
            status_text.success(f"✅ ¡{len(images_data)} imágenes procesadas! ⚡ Optimización: {savings:.0f}% más ligero")
            
            # VISTA PREVIA MÓVIL - TODAS LAS IMÁGENES EN FORMATO CARRUSEL
            if images_data:
                st.markdown("### 👁️ Vista Previa (Formato Móvil)")
                
                # Selector de imagen para vista previa tipo carrusel
                total_images = len(images_data)
                
                # Controles de navegación
                nav_col1, nav_col2, nav_col3 = st.columns([1, 3, 1])
                
                with nav_col1:
                    if st.button("⬅️ Anterior", disabled=total_images <= 1):
                        st.session_state.current_preview = max(0, st.session_state.current_preview - 1)
                
                with nav_col2:
                    st.markdown(f"""
                    <div class="preview-counter">
                        📷 Imagen {st.session_state.current_preview + 1} de {total_images} 
                        (Desliza o usa botones para navegar)
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Mostrar imagen actual en contenedor móvil
                    current_idx = st.session_state.current_preview % total_images
                    current_data = images_data[current_idx]
                    
                    st.markdown('<div class="mobile-preview-container">', unsafe_allow_html=True)
                    st.image(current_data['image'], 
                            caption=f"{current_data['name']} • {current_data['final_size'][0]}×{current_data['final_size'][1]}px", 
                            use_container_width=True)
                    
                    # Indicador de rotación si aplica
                    if current_data['was_rotated']:
                        direction = "horario ↻" if current_data['rotation_applied'] > 0 else "antihorario ↺"
                        st.info(f"🔄 Rotada {abs(current_data['rotation_applied'])}° {direction}")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with nav_col3:
                    if st.button("Siguiente ➡️", disabled=total_images <= 1):
                        st.session_state.current_preview = min(total_images - 1, st.session_state.current_preview + 1)
                
                # Slider adicional para navegación rápida
                if total_images > 1:
                    selected_preview = st.slider("Navegar imágenes", 1, total_images, st.session_state.current_preview + 1)
                    st.session_state.current_preview = selected_preview - 1
                
                # Detalles al lado de la vista previa
                st.markdown("### 📋 Resumen del Proceso")
                
                summary_col1, summary_col2 = st.columns(2)
                
                with summary_col1:
                    st.markdown("#### 🎨 Ajustes aplicados")
                    changes = []
                    if "Natural" not in sheet_format:
                        changes.append(f"✅ Color: {sheet_format}")
                    if rotation_degrees != 0:
                        direction = "horario ↻" if rotation_degrees > 0 else "antihorario ↺"
                        changes.append(f"✅ Rotación: {abs(rotation_degrees)}° {direction}")
                    if optimize_images:
                        changes.append(f"✅ Optimización: {max_dimension}px máx")
                    changes.append(f"✅ Compresión: {compression_level}")
                    changes.append("✅ Marca de agua Yan")
                    
                    for change in changes:
                        st.success(change)
                
                with summary_col2:
                    st.markdown("#### 📊 Estadísticas")
                    st.code(f"""
Total imágenes:     {len(images_data)}
Tamaño original:    {original_pixels/1000000:.1f} MPix
Tamaño final:       {final_pixels/1000000:.1f} MPix
Ahorro:             {savings:.0f}%
Calidad PDF:        {quality} DPI
Compresión:         {compression_level} ({compression_quality}%)
                    """)
                    
                    if len(images_data) > 1:
                        st.markdown("#### 🗂️ Lista de archivos")
                        for i, data in enumerate(images_data, 1):
                            rotated = " 🔄" if data['was_rotated'] else ""
                            st.caption(f"{i}. {data['name']}{rotated} ({data['final_size'][0]}×{data['final_size'][1]})")
            
            # Botón de generación
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🚀 GENERAR PDF(S) OPTIMIZADO", key="convert", use_container_width=True):
                with st.spinner(f"Creando PDF con compresión {compression_level}..."):
                    
                    final_images = []
                    
                    for data in images_data:
                        final_images.append(data['image'])
                    
                    if output_format in ["PDF único", "Ambos"] and len(final_images) > 0:
                        pdf_buffer = io.BytesIO()
                        
                        first_img = final_images[0]
                        other_imgs = final_images[1:]
                        
                        # Guardar con compresión optimizada
                        save_kwargs = {
                            'resolution': quality,
                            'save_all': True,
                            'append_images': other_imgs,
                            'quality': compression_quality,
                        }
                        
                        first_img.save(pdf_buffer, 'PDF', **save_kwargs)
                        pdf_buffer.seek(0)
                        
                        # Calcular tamaño del PDF
                        pdf_size_mb = len(pdf_buffer.getvalue()) / (1024 * 1024)
                        
                        st.session_state.processed_files += len(images_data)
                        st.session_state.total_size += total_size
                        
                        st.balloons()
                        
                        rot_info = f"Rotación: {rotation_degrees}°" if rotation_degrees != 0 else "Sin rotación"
                        
                        st.markdown(f"""
                        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white; margin: 1rem 0;">
                            <h2>✨ ¡PDF Optimizado Creado! ✨</h2>
                            <p>Estilo: <b>{sheet_format}</b> • {len(final_images)} páginas</p>
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
                                # Guardar con compresión
                                data['image'].save(pdf_individual, 'PDF', 
                                                 resolution=quality, 
                                                 quality=compression_quality)
                                pdf_individual.seek(0)
                                
                                ind_size = len(pdf_individual.getvalue()) / 1024
                                
                                st.download_button(
                                    label=f"📄 {data['name']}_Yan.pdf ({ind_size:.0f} KB)",
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