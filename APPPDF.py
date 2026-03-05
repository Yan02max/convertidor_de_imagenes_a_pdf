import streamlit as st
from PIL import Image
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

# CSS personalizado para animaciones y diseño moderno
st.markdown("""
<style>
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
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
        animation: float 3s ease-in-out infinite;
    }
    
    .upload-zone:hover {
        border-color: #2196F3;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transform: translateY(-5px);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin: 0.5rem;
        animation: slideIn 0.5s ease-out;
    }
    
    /* Grid de previsualización tipo carpeta */
    .preview-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        gap: 15px;
        padding: 20px;
        background: #f8f9fa;
        border-radius: 15px;
        max-height: 600px;
        overflow-y: auto;
    }
    
    .preview-item {
        background: white;
        border-radius: 12px;
        padding: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .preview-item:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .preview-item.selected {
        border: 3px solid #4CAF50;
        box-shadow: 0 0 0 4px rgba(76, 175, 80, 0.2);
    }
    
    .gift-card-style {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
        border: 2px solid #ff6b6b;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .gift-card-style::before {
        content: "🎁";
        position: absolute;
        top: -10px;
        right: -10px;
        font-size: 3rem;
        opacity: 0.3;
        transform: rotate(15deg);
    }
    
    .gift-ribbon {
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 30px;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    }
    
    .a4-style {
        background: white;
        border: 1px solid #ddd;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .letter-style {
        background: #fefefe;
        border: 2px solid #4CAF50;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .custom-size-inputs {
        background: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar session state para previsualización
if 'preview_images' not in st.session_state:
    st.session_state.preview_images = []
    st.session_state.processed_files = 0
    st.session_state.total_size = 0

# Header animado
st.markdown("""
<div class="main-header">
    <h1 style="font-size: 3.5rem; background: linear-gradient(45deg, #2196F3, #4CAF50); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        🚀 PDF Converter Yan
    </h1>
    <p style="font-size: 1.3rem; color: #666;">Conversión profesional de imágenes con previsualización en tiempo real</p>
</div>
""", unsafe_allow_html=True)

# Sidebar con configuración mejorada
with st.sidebar:
    st.markdown("### ⚙️ Configuración Avanzada")
    
    max_file_size = st.number_input("Tamaño máx. por archivo (MB)", 1, 100, 50)
    max_files = st.number_input("Máximo de archivos", 1, 50, 20)
    
    quality = st.slider("Calidad PDF (DPI)", 50, 300, 150)
    
    st.markdown("---")
    st.markdown("### 📐 Configuración de Página")
    
    # Selector de tamaño de página con estilos visuales
    page_size = st.selectbox(
        "Tamaño de página",
        ["Original", "A4", "Carta (Carta de Regalo)", "Personalizado"]
    )
    
    # Inputs para tamaño personalizado
    custom_width, custom_height = 210, 297  # Default A4 mm
    if page_size == "Personalizado":
        with st.container():
            st.markdown('<div class="custom-size-inputs">', unsafe_allow_html=True)
            col_w, col_h = st.columns(2)
            with col_w:
                custom_width = st.number_input("Ancho (mm)", 50, 500, 210)
            with col_h:
                custom_height = st.number_input("Alto (mm)", 50, 500, 297)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Orientación con efectos visuales
    orientation = st.radio(
        "Orientación",
        ["Automática", "Vertical", "Horizontal"],
        help="Cambia la orientación de las páginas del PDF"
    )
    
    margin = st.slider("Margen (mm)", 0, 50, 0)
    
    st.markdown("---")
    
    # Nombre del proyecto
    project_name = st.text_input(
        "📝 Nombre del proyecto",
        value=f"Proyecto_{datetime.now().strftime('%Y%m%d')}",
        help="Este nombre se usará para guardar tu PDF"
    )
    
    output_format = st.radio("Formato de salida", ["PDF único", "PDFs separados", "Ambos"])
    
    st.markdown("---")
    
    # Estadísticas
    st.markdown("### 📊 Estadísticas")
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric("Archivos procesados", st.session_state.processed_files)
    with col_stat2:
        st.metric("MB procesados", f"{st.session_state.total_size:.1f}")

# Área de upload
st.markdown("""
<div class="upload-zone">
    <h2>📁 Arrastra tus imágenes aquí</h2>
    <p style="color: #666;">o haz clic para seleccionar archivos</p>
    <p style="font-size: 0.9rem; color: #999;">Máximo {} archivos • Hasta {} MB cada uno</p>
</div>
""".format(max_files, max_file_size), unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "", 
    type=['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'webp', 'gif', 'ico'],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

# Función para aplicar estilos según configuración
def get_page_style():
    if page_size == "Carta (Carta de Regalo)":
        return "gift-card-style"
    elif page_size == "A4":
        return "a4-style"
    elif page_size == "Carta":
        return "letter-style"
    return ""

def apply_orientation(img):
    """Aplica orientación seleccionada a la imagen"""
    if orientation == "Automática":
        return img
    
    width, height = img.size
    is_landscape = width > height
    
    if orientation == "Horizontal" and not is_landscape:
        # Rotar a horizontal
        img = img.rotate(90, expand=True)
    elif orientation == "Vertical" and is_landscape:
        # Rotar a vertical
        img = img.rotate(-90, expand=True)
    
    return img

def resize_to_page_size(img):
    """Redimensiona imagen según tamaño de página seleccionado"""
    if page_size == "Original":
        return img
    
    # Conversiones aproximadas de mm a pixels (a 96 DPI)
    mm_to_px = 3.7795275591
    
    if page_size == "A4":
        target_w, target_h = int(210 * mm_to_px), int(297 * mm_to_px)
    elif page_size == "Carta (Carta de Regalo)" or page_size == "Carta":
        target_w, target_h = int(216 * mm_to_px), int(279 * mm_to_px)
    elif page_size == "Personalizado":
        target_w, target_h = int(custom_width * mm_to_px), int(custom_height * mm_to_px)
    else:
        return img
    
    # Aplicar márgenes
    margin_px = int(margin * mm_to_px)
    target_w -= 2 * margin_px
    target_h -= 2 * margin_px
    
    # Calcular escala manteniendo aspect ratio
    img_w, img_h = img.size
    scale_w = target_w / img_w
    scale_h = target_h / img_h
    scale = min(scale_w, scale_h)
    
    new_w = int(img_w * scale)
    new_h = int(img_h * scale)
    
    return img.resize((new_w, new_h), Image.Resampling.LANCZOS)

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
            st.markdown("### 📈 Progreso de Conversión")
            
            progress_cols = st.columns(4)
            with progress_cols[0]:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>{len(valid_files)}</h3>
                    <p>Archivos válidos</p>
                </div>
                """, unsafe_allow_html=True)
            
            with progress_cols[1]:
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                    <h3>{total_size:.1f} MB</h3>
                    <p>Tamaño total</p>
                </div>
                """, unsafe_allow_html=True)
            
            with progress_cols[2]:
                page_type = "🎁" if "Regalo" in page_size else "📄"
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                    <h3>{page_type}</h3>
                    <p>{page_size}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with progress_cols[3]:
                orient_emoji = "📱" if orientation == "Vertical" else "💻" if orientation == "Horizontal" else "🔄"
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
                    <h3>{orient_emoji}</h3>
                    <p>{orientation}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Procesar imágenes con barra de progreso
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            images_data = []
            
            for idx, file in enumerate(valid_files):
                try:
                    image = Image.open(file)
                    original_size = image.size
                    
                    # Aplicar orientación
                    image = apply_orientation(image)
                    
                    # Redimensionar según página seleccionada
                    image = resize_to_page_size(image)
                    
                    # Convertir a RGB
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
                    
                    images_data.append({
                        'image': image,
                        'name': os.path.splitext(file.name)[0],
                        'original': file,
                        'original_size': original_size
                    })
                    
                    progress = (idx + 1) / len(valid_files)
                    progress_bar.progress(int(progress * 100))
                    status_text.text(f"Procesando {idx + 1} de {len(valid_files)}: {file.name}")
                    
                except Exception as e:
                    st.error(f"Error con {file.name}: {str(e)}")
            
            progress_bar.empty()
            status_text.success(f"✅ ¡{len(images_data)} imágenes procesadas!")
            
            # Grid de previsualización tipo carpeta
            st.markdown("### 👁️ Previsualización (Vista de Carpeta)")
            
            # Mostrar en grid responsive
            cols_per_row = 5
            rows = (len(images_data) + cols_per_row - 1) // cols_per_row
            
            for row in range(rows):
                cols = st.columns(cols_per_row)
                for col_idx in range(cols_per_row):
                    idx = row * cols_per_row + col_idx
                    if idx < len(images_data):
                        with cols[col_idx]:
                            data = images_data[idx]
                            
                            # Aplicar clase de estilo según configuración
                            style_class = get_page_style()
                            
                            st.markdown(f'<div class="preview-item {style_class}">', unsafe_allow_html=True)
                            
                            # Mostrar imagen procesada
                            st.image(data['image'], use_container_width=True)
                            
                            # Información
                            st.caption(f"📄 {data['name'][:15]}...")
                            new_size = data['image'].size
                            st.caption(f"📐 {new_size[0]}×{new_size[1]}")
                            
                            # Indicador de cambio de orientación
                            orig = data['original_size']
                            if (orig[0] > orig[1]) != (new_size[0] > new_size[1]):
                                st.caption("🔄 Rotado")
                            
                            st.markdown('</div>', unsafe_allow_html=True)
            
            # Botón de generación
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🚀 GENERAR PDF(S)", key="convert", use_container_width=True):
                with st.spinner("Generando documentos de alta calidad..."):
                    
                    if output_format in ["PDF único", "Ambos"] and len(images_data) > 0:
                        pdf_buffer = io.BytesIO()
                        
                        first_img = images_data[0]['image']
                        other_imgs = [d['image'] for d in images_data[1:]]
                        
                        quality_map = {
                            "Mínima": 30, "Baja": 50, "Media": 75, "Alta": 90, "Máxima": 95
                        }
                        
                        save_kwargs = {
                            'resolution': quality,
                            'save_all': True,
                            'append_images': other_imgs,
                        }
                        
                        first_img.save(pdf_buffer, 'PDF', **save_kwargs)
                        pdf_buffer.seek(0)
                        
                        st.session_state.processed_files += len(images_data)
                        st.session_state.total_size += total_size
                        
                        st.balloons()
                        
                        # Mensaje de éxito con estilo según tipo de página
                        if "Regalo" in page_size:
                            st.markdown("""
                            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); border-radius: 15px; color: #d63031; margin: 1rem 0; border: 3px solid #ff6b6b;">
                                <h2>🎁 ¡PDF de Regalo Creado!</h2>
                                <p>Tu carta especial está lista para descargar</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white; margin: 1rem 0;">
                                <h2>🎉 ¡Conversión Exitosa!</h2>
                                <p>Tu PDF está listo para descargar</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.download_button(
                            label=f"📥 Descargar {project_name}.pdf ({len(images_data)} páginas)",
                            data=pdf_buffer,
                            file_name=f"{project_name}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    
                    # PDFs individuales
                    if output_format in ["PDFs separados", "Ambos"]:
                        st.markdown("### 📄 Archivos Individuales")
                        
                        individual_cols = st.columns(3)
                        for idx, data in enumerate(images_data):
                            with individual_cols[idx % 3]:
                                pdf_individual = io.BytesIO()
                                data['image'].save(pdf_individual, 'PDF', resolution=quality)
                                pdf_individual.seek(0)
                                
                                st.download_button(
                                    label=f"📄 {data['name']}.pdf",
                                    data=pdf_individual,
                                    file_name=f"{data['name']}.pdf",
                                    mime="application/pdf",
                                    key=f"indiv_{idx}"
                                )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🚀 PDF Converter De Yan | Procesamiento profesional de imágenes</p>
    <p style="font-size: 0.8rem;">Soporta hasta 50 archivos • Múltiples formatos de página • Previsualización en tiempo real</p>
</div>
""", unsafe_allow_html=True)