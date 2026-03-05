import streamlit as st
from PIL import Image, ImageDraw, ImageFont
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
    
    .config-section {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .preview-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        margin: 2rem 0;
        text-align: center;
    }
    
    /* Estilos de hoja de presentación */
    .sheet-class {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem;
        border-radius: 15px;
        position: relative;
        overflow: hidden;
    }
    
    .sheet-class::before {
        content: "✏️";
        position: absolute;
        top: 20px;
        right: 20px;
        font-size: 4rem;
        opacity: 0.2;
    }
    
    .sheet-gift {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #ffecd2 100%);
        color: #d63031;
        padding: 3rem;
        border-radius: 15px;
        position: relative;
        overflow: hidden;
        border: 3px solid #ff6b6b;
    }
    
    .sheet-gift::before {
        content: "🎁";
        position: absolute;
        top: 20px;
        right: 20px;
        font-size: 4rem;
        opacity: 0.3;
    }
    
    .sheet-work {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 3rem;
        border-radius: 15px;
        position: relative;
        overflow: hidden;
    }
    
    .sheet-work::before {
        content: "💼";
        position: absolute;
        top: 20px;
        right: 20px;
        font-size: 4rem;
        opacity: 0.2;
    }
    
    .watermark-preview {
        position: absolute;
        bottom: 20px;
        right: 20px;
        font-size: 1.5rem;
        opacity: 0.6;
        font-weight: bold;
        color: rgba(255,255,255,0.8);
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Inicializar session state
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
    <p style="font-size: 1.3rem; color: #666;">Conversión profesional de imágenes con marca de agua Yan</p>
</div>
""", unsafe_allow_html=True)

# Área de upload PRIMERO
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

# CONFIGURACIÓN FUERA (después del upload)
st.markdown("### ⚙️ Configuración de Conversión")

with st.container():
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    
    # Fila 1: Configuración básica
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        max_files = st.number_input("Máximo archivos", 1, 50, 20)
        quality = st.slider("Calidad PDF (DPI)", 50, 300, 150)
    
    with col2:
        max_file_size = st.number_input("Tamaño máx. (MB)", 1, 100, 50)
        margin = st.slider("Margen (mm)", 0, 50, 0)
    
    with col3:
        # Selector de formato de hoja
        sheet_format = st.selectbox(
            "📄 Formato de Hoja",
            ["Clase/Escolar", "Regalo", "Trabajo/Profesional"]
        )
        
        page_size = st.selectbox(
            "Tamaño de página",
            ["Original", "A4", "Carta", "Personalizado"]
        )
    
    with col4:
        # Orientación con visualización clara
        orientation = st.radio(
            "📐 Orientación",
            ["Automática", "Vertical", "Horizontal"],
            horizontal=True
        )
        
        output_format = st.radio(
            "📦 Salida",
            ["PDF único", "PDFs separados", "Ambos"],
            horizontal=True
        )
    
    # Fila 2: Tamaño personalizado y nombre
    col5, col6 = st.columns(2)
    
    custom_width, custom_height = 210, 297
    with col5:
        if page_size == "Personalizado":
            st.markdown("**Dimensiones personalizadas:**")
            c1, c2 = st.columns(2)
            with c1:
                custom_width = st.number_input("Ancho (mm)", 50, 500, 210)
            with c2:
                custom_height = st.number_input("Alto (mm)", 50, 500, 297)
    
    with col6:
        project_name = st.text_input(
            "📝 Nombre del proyecto",
            value=f"Proyecto_Yan_{datetime.now().strftime('%Y%m%d')}",
            help="Nombre para guardar tu PDF"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Función para obtener estilo de hoja
def get_sheet_style():
    styles = {
        "Clase/Escolar": "sheet-class",
        "Regalo": "sheet-gift",
        "Trabajo/Profesional": "sheet-work"
    }
    return styles.get(sheet_format, "sheet-class")

def get_sheet_emoji():
    emojis = {
        "Clase/Escolar": "✏️",
        "Regalo": "🎁",
        "Trabajo/Profesional": "💼"
    }
    return emojis.get(sheet_format, "📄")

def apply_orientation(img):
    """Aplica orientación seleccionada a la imagen"""
    if orientation == "Automática":
        return img
    
    width, height = img.size
    
    if orientation == "Horizontal":
        # Forzar horizontal (landscape)
        if height > width:
            img = img.rotate(90, expand=True)
    elif orientation == "Vertical":
        # Forzar vertical (portrait)
        if width > height:
            img = img.rotate(-90, expand=True)
    
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
    scale = min(scale_w, scale_h, 1.0)  # No ampliar, solo reducir
    
    new_w = max(int(img_w * scale), 1)
    new_h = max(int(img_h * scale), 1)
    
    return img.resize((new_w, new_h), Image.Resampling.LANCZOS)

def add_watermark(img, text="Yan"):
    """Añade marca de agua 'Yan' a la imagen"""
    # Crear copia para no modificar original
    watermarked = img.copy()
    draw = ImageDraw.Draw(watermarked)
    
    # Intentar usar fuente por defecto o crear una básica
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    # Calcular posición (esquina inferior derecha)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = img.width - text_width - 30
    y = img.height - text_height - 30
    
    # Dibujar sombra
    draw.text((x+2, y+2), text, font=font, fill=(0, 0, 0, 128))
    # Dibujar texto principal
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 200))
    
    return watermarked

def create_presentation_sheet(img, format_type):
    """Crea una hoja de presentación según el formato seleccionado"""
    # Tamaño base A4 en pixels (150 DPI)
    sheet_width, sheet_height = 1240, 1754
    
    # Crear fondo según formato
    if format_type == "Clase/Escolar":
        # Fondo azul-morado para clase
        sheet = Image.new('RGB', (sheet_width, sheet_height), (102, 126, 234))
        accent_color = (255, 255, 255)
        emoji = "✏️"
        title = "Material de Clase"
    elif format_type == "Regalo":
        # Fondo rosa para regalo
        sheet = Image.new('RGB', (sheet_width, sheet_height), (255, 154, 158))
        accent_color = (255, 255, 255)
        emoji = "🎁"
        title = "¡Con Amor!"
    else:  # Trabajo
        # Fondo verde para trabajo
        sheet = Image.new('RGB', (sheet_width, sheet_height), (17, 153, 142))
        accent_color = (255, 255, 255)
        emoji = "💼"
        title = "Documento Profesional"
    
    draw = ImageDraw.Draw(sheet)
    
    # Intentar cargar fuentes
    try:
        font_title = ImageFont.truetype("arial.ttf", 60)
        font_emoji = ImageFont.truetype("arial.ttf", 120)
        font_watermark = ImageFont.truetype("arial.ttf", 40)
    except:
        font_title = ImageFont.load_default()
        font_emoji = ImageFont.load_default()
        font_watermark = ImageFont.load_default()
    
    # Dibujar emoji grande en esquina
    draw.text((sheet_width - 150, 50), emoji, font=font_emoji, fill=(255, 255, 255, 100))
    
    # Dibujar título
    bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = bbox[2] - bbox[0]
    draw.text(((sheet_width - title_width) // 2, 100), title, font=font_title, fill=accent_color)
    
    # Calcular espacio para imagen
    margin = 100
    available_width = sheet_width - (2 * margin)
    available_height = sheet_height - 300  # Espacio para título y marca de agua
    
    # Redimensionar imagen para caber en la hoja
    img_ratio = img.width / img.height
    sheet_ratio = available_width / available_height
    
    if img_ratio > sheet_ratio:
        new_width = available_width
        new_height = int(available_width / img_ratio)
    else:
        new_height = available_height
        new_width = int(available_height * img_ratio)
    
    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Pegar imagen centrada
    x_offset = (sheet_width - new_width) // 2
    y_offset = 250 + (available_height - new_height) // 2
    
    # Convertir imagen a RGB si es necesario
    if resized_img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', resized_img.size, (255, 255, 255))
        if resized_img.mode == 'P':
            resized_img = resized_img.convert('RGBA')
        if resized_img.mode in ('RGBA', 'LA'):
            background.paste(resized_img, mask=resized_img.split()[-1])
        else:
            background.paste(resized_img)
        resized_img = background
    
    sheet.paste(resized_img, (x_offset, y_offset))
    
    # Añadir marca de agua Yan
    draw.text((sheet_width - 150, sheet_height - 80), "Yan", font=font_watermark, 
              fill=(255, 255, 255, 150))
    
    return sheet

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
                emoji = get_sheet_emoji()
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                    <h3>{emoji}</h3>
                    <p>{sheet_format}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with progress_cols[3]:
                orient_icon = "📱" if orientation == "Vertical" else "💻" if orientation == "Horizontal" else "🔄"
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
                    <h3>{orient_icon}</h3>
                    <p>{orientation}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Procesar imágenes
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            images_data = []
            
            for idx, file in enumerate(valid_files):
                try:
                    image = Image.open(file)
                    original_size = image.size
                    
                    # Aplicar orientación primero
                    image = apply_orientation(image)
                    
                    # Luego redimensionar
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
                    status_text.text(f"Procesando {idx + 1} de {len(valid_files)}...")
                    
                except Exception as e:
                    st.error(f"Error con {file.name}: {str(e)}")
            
            progress_bar.empty()
            status_text.success(f"✅ ¡{len(images_data)} imágenes listas!")
            
            # PREVISUALIZACIÓN SOLO DE LA PRIMERA FOTO
            if images_data:
                st.markdown("### 👁️ Previsualización (Primera imagen)")
                
                preview_col1, preview_col2 = st.columns([2, 1])
                
                with preview_col1:
                    # Mostrar hoja de presentación con la primera imagen
                    sheet_style = get_sheet_style()
                    first_img = images_data[0]['image']
                    
                    # Crear hoja de presentación
                    presentation_sheet = create_presentation_sheet(first_img, sheet_format)
                    
                    st.markdown(f'<div class="preview-container">', unsafe_allow_html=True)
                    st.image(presentation_sheet, use_container_width=True, 
                            caption=f"Vista previa: Formato {sheet_format} con marca de agua Yan")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with preview_col2:
                    # Información de la previsualización
                    st.markdown("### 📋 Detalles")
                    st.info(f"""
                    **Formato seleccionado:** {sheet_format} {get_sheet_emoji()}
                    
                    **Orientación aplicada:** {orientation}
                    
                    **Tamaño original:** {images_data[0]['original_size'][0]}×{images_data[0]['original_size'][1]} px
                    
                    **Tamaño final:** {first_img.width}×{first_img.height} px
                    
                    **Marca de agua:** Yan™
                    
                    **Total archivos:** {len(images_data)}
                    """)
                    
                    # Miniaturas de las demás imágenes (solo nombres)
                    if len(images_data) > 1:
                        st.markdown("### 🖼️ Otras imágenes")
                        for i, data in enumerate(images_data[1:], 1):
                            st.caption(f"{i}. {data['name']}")
            
            # Botón de generación
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🚀 GENERAR PDF(S) CON MARCA YAN", key="convert", use_container_width=True):
                with st.spinner("Creando documentos profesionales..."):
                    
                    # Crear hojas de presentación para todas las imágenes
                    final_images = []
                    for data in images_data:
                        sheet = create_presentation_sheet(data['image'], sheet_format)
                        final_images.append(sheet)
                    
                    if output_format in ["PDF único", "Ambos"] and len(final_images) > 0:
                        pdf_buffer = io.BytesIO()
                        
                        first_img = final_images[0]
                        other_imgs = final_images[1:]
                        
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
                        
                        # Mensaje según formato
                        style_colors = {
                            "Clase/Escolar": ("#667eea", "#764ba2", "✏️"),
                            "Regalo": ("#ff9a9e", "#fecfef", "🎁"),
                            "Trabajo/Profesional": ("#11998e", "#38ef7d", "💼")
                        }
                        
                        c1, c2 = style_colors.get(sheet_format, ("#667eea", "#764ba2", "📄"))
                        
                        st.markdown(f"""
                        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, {c1} 0%, {c2} 100%); border-radius: 15px; color: white; margin: 1rem 0;">
                            <h2>{style_colors.get(sheet_format, ("", "", "📄"))[2]} ¡PDF Creado Exitosamente!</h2>
                            <p>Documento estilo {sheet_format} con marca de agua Yan</p>
                            <p style="font-size: 0.9rem; opacity: 0.9;">{len(final_images)} páginas • Calidad {quality} DPI</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.download_button(
                            label=f"📥 Descargar {project_name}.pdf",
                            data=pdf_buffer,
                            file_name=f"{project_name}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    
                    # PDFs individuales
                    if output_format in ["PDFs separados", "Ambos"]:
                        st.markdown("### 📄 Archivos Individuales")
                        
                        individual_cols = st.columns(3)
                        for idx, (data, sheet) in enumerate(zip(images_data, final_images)):
                            with individual_cols[idx % 3]:
                                pdf_individual = io.BytesIO()
                                sheet.save(pdf_individual, 'PDF', resolution=quality)
                                pdf_individual.seek(0)
                                
                                st.download_button(
                                    label=f"📄 {data['name']}_Yan.pdf",
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
    st.info("💡 **Consejo:** Usa el formato 'Regalo' para crear tarjetas especiales con la marca Yan.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🚀 PDF Converter De Yan | Documentos con estilo y marca personalizada</p>
    <p style="font-size: 0.8rem;">Todos los PDFs incluyen marca de agua Yan™ | Hasta 50 archivos simultáneos</p>
</div>
""", unsafe_allow_html=True)