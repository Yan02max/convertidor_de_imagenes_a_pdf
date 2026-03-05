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
    
    .info-sheet {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
    }
    
    .info-sheet-class {
        border-left: 5px solid #667eea;
    }
    
    .info-sheet-gift {
        border-left: 5px solid #ff6b6b;
        background: linear-gradient(to right, #fff5f5, white);
    }
    
    .info-sheet-work {
        border-left: 5px solid #11998e;
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
        # Selector de tipo de hoja de información
        sheet_format = st.selectbox(
            "📄 Tipo de Documento",
            ["Solo Imágenes", "Clase/Escolar", "Regalo", "Trabajo/Profesional"]
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

# HOJA DE INFORMACIÓN OPCIONAL (aparece solo si no es "Solo Imágenes")
show_info_sheet = sheet_format != "Solo Imágenes"

if show_info_sheet:
    st.markdown("### 📝 Hoja de Información (Opcional)")
    
    with st.container():
        if sheet_format == "Clase/Escolar":
            st.markdown('<div class="info-sheet info-sheet-class">', unsafe_allow_html=True)
            st.markdown("#### ✏️ Información del Estudiante")
            
            col_a, col_b = st.columns(2)
            with col_a:
                student_name = st.text_input("Nombre del estudiante", "")
                subject = st.text_input("Materia/Asignatura", "")
                teacher = st.text_input("Profesor(a)", "")
            with col_b:
                grade = st.text_input("Grado/Grupo", "")
                date_class = st.date_input("Fecha", datetime.now())
                school = st.text_input("Escuela/Institución", "")
            
            topic = st.text_area("Tema o descripción", "", height=100)
            st.markdown('</div>', unsafe_allow_html=True)
            
        elif sheet_format == "Regalo":
            st.markdown('<div class="info-sheet info-sheet-gift">', unsafe_allow_html=True)
            st.markdown("#### 🎁 Información del Regalo")
            
            col_a, col_b = st.columns(2)
            with col_a:
                recipient = st.text_input("Para:", "")
                occasion = st.selectbox("Ocasión", ["Cumpleaños", "Aniversario", "Navidad", "San Valentín", "Otro"])
            with col_b:
                sender = st.text_input("De parte de:", "")
                date_gift = st.date_input("Fecha del regalo", datetime.now())
            
            message = st.text_area("Mensaje personal", "¡Con mucho cariño!", height=100)
            st.markdown('</div>', unsafe_allow_html=True)
            
        elif sheet_format == "Trabajo/Profesional":
            st.markdown('<div class="info-sheet info-sheet-work">', unsafe_allow_html=True)
            st.markdown("#### 💼 Información del Documento")
            
            col_a, col_b = st.columns(2)
            with col_a:
                company = st.text_input("Empresa/Organización", "")
                department = st.text_input("Departamento", "")
                prepared_by = st.text_input("Preparado por", "")
            with col_b:
                doc_title = st.text_input("Título del documento", "")
                doc_code = st.text_input("Código/Referencia", "")
                date_work = st.date_input("Fecha", datetime.now())
            
            confidentiality = st.select_slider(
                "Nivel de confidencialidad",
                options=["Público", "Interno", "Confidencial", "Restringido"],
                value="Interno"
            )
            st.markdown('</div>', unsafe_allow_html=True)

def get_sheet_emoji():
    emojis = {
        "Clase/Escolar": "✏️",
        "Regalo": "🎁",
        "Trabajo/Profesional": "💼",
        "Solo Imágenes": "🖼️"
    }
    return emojis.get(sheet_format, "📄")

def apply_orientation(img):
    """Aplica orientación seleccionada a la imagen"""
    if orientation == "Automática":
        return img
    
    width, height = img.size
    
    if orientation == "Horizontal":
        if height > width:
            img = img.rotate(90, expand=True)
    elif orientation == "Vertical":
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
    scale = min(scale_w, scale_h, 1.0)
    
    new_w = max(int(img_w * scale), 1)
    new_h = max(int(img_h * scale), 1)
    
    return img.resize((new_w, new_h), Image.Resampling.LANCZOS)

def create_info_sheet_image(format_type):
    """Crea una imagen de la hoja de información según el tipo"""
    if format_type == "Solo Imágenes":
        return None
    
    # Tamaño A4 en pixels (150 DPI)
    sheet_width, sheet_height = 1240, 1754
    
    if format_type == "Clase/Escolar":
        # Fondo blanco con borde azul
        sheet = Image.new('RGB', (sheet_width, sheet_height), (255, 255, 255))
        draw = ImageDraw.Draw(sheet)
        
        # Borde decorativo
        draw.rectangle([20, 20, sheet_width-20, sheet_height-20], outline=(102, 126, 234), width=5)
        
        # Header
        try:
            font_header = ImageFont.truetype("arial.ttf", 50)
            font_text = ImageFont.truetype("arial.ttf", 30)
            font_small = ImageFont.truetype("arial.ttf", 25)
        except:
            font_header = ImageFont.load_default()
            font_text = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Título
        draw.text((sheet_width//2, 80), "✏️ INFORMACIÓN DEL ESTUDIANTE", 
                 fill=(102, 126, 234), font=font_header, anchor="mm")
        
        # Línea decorativa
        draw.line([(100, 120), (sheet_width-100, 120)], fill=(102, 126, 234), width=3)
        
        # Información del formulario
        y_pos = 180
        line_height = 60
        
        info_lines = [
            f"👤 Estudiante: {student_name if student_name else '_____________________'}",
            f"📚 Materia: {subject if subject else '_____________________'}",
            f"👨‍🏫 Profesor(a): {teacher if teacher else '_____________________'}",
            f"🎓 Grado/Grupo: {grade if grade else '_____________________'}",
            f"📅 Fecha: {date_class.strftime('%d/%m/%Y') if 'date_class' in locals() else '_____________________'}",
            f"🏫 Escuela: {school if school else '_____________________'}",
            "",
            "📝 Tema/Descripción:",
            topic if 'topic' in locals() and topic else "______________________________________________",
        ]
        
        for line in info_lines:
            draw.text((80, y_pos), line, fill=(50, 50, 50), font=font_text)
            y_pos += line_height
        
        # Marca de agua Yan
        draw.text((sheet_width-150, sheet_height-80), "Yan", 
                 fill=(200, 200, 200), font=font_header)
        
        return sheet
        
    elif format_type == "Regalo":
        # Fondo blanco con detalles rosas
        sheet = Image.new('RGB', (sheet_width, sheet_height), (255, 255, 255))
        draw = ImageDraw.Draw(sheet)
        
        # Decoración de regalo
        draw.rectangle([20, 20, sheet_width-20, sheet_height-20], outline=(255, 107, 107), width=5)
        
        # Moño decorativo en esquinas
        for x in [50, sheet_width-100]:
            for y in [50, sheet_height-150]:
                draw.ellipse([x, y, x+50, y+50], fill=(255, 154, 158))
        
        try:
            font_header = ImageFont.truetype("arial.ttf", 50)
            font_text = ImageFont.truetype("arial.ttf", 35)
            font_message = ImageFont.truetype("arial.ttf", 30)
        except:
            font_header = ImageFont.load_default()
            font_text = ImageFont.load_default()
            font_message = ImageFont.load_default()
        
        # Título
        draw.text((sheet_width//2, 100), "🎁 REGALO ESPECIAL", 
                 fill=(255, 107, 107), font=font_header, anchor="mm")
        
        y_pos = 200
        
        # Información
        draw.text((100, y_pos), f"Para: {recipient if recipient else '_____________________'}", 
                 fill=(50, 50, 50), font=font_text)
        y_pos += 80
        
        draw.text((100, y_pos), f"Ocasión: {occasion if 'occasion' in locals() else '_____________________'}", 
                 fill=(50, 50, 50), font=font_text)
        y_pos += 80
        
        draw.text((100, y_pos), f"De: {sender if sender else '_____________________'}", 
                 fill=(50, 50, 50), font=font_text)
        y_pos += 80
        
        draw.text((100, y_pos), f"Fecha: {date_gift.strftime('%d/%m/%Y') if 'date_gift' in locals() else '_____________________'}", 
                 fill=(50, 50, 50), font=font_text)
        y_pos += 120
        
        # Caja de mensaje
        draw.rectangle([80, y_pos, sheet_width-80, y_pos+300], outline=(255, 154, 158), width=2)
        draw.text((100, y_pos+20), "Mensaje:", fill=(255, 107, 107), font=font_text)
        
        msg = message if 'message' in locals() and message else "¡Con mucho cariño!"
        draw.text((100, y_pos+80), msg, fill=(80, 80, 80), font=font_message)
        
        # Marca de agua
        draw.text((sheet_width-150, sheet_height-80), "Yan", 
                 fill=(255, 200, 200), font=font_header)
        
        return sheet
        
    elif format_type == "Trabajo/Profesional":
        # Fondo blanco con detalles verdes profesionales
        sheet = Image.new('RGB', (sheet_width, sheet_height), (255, 255, 255))
        draw = ImageDraw.Draw(sheet)
        
        # Borde profesional
        draw.rectangle([20, 20, sheet_width-20, sheet_height-20], outline=(17, 153, 142), width=5)
        
        # Línea de encabezado
        draw.rectangle([0, 0, sheet_width, 150], fill=(17, 153, 142))
        
        try:
            font_header = ImageFont.truetype("arial.ttf", 40)
            font_title = ImageFont.truetype("arial.ttf", 50)
            font_text = ImageFont.truetype("arial.ttf", 30)
        except:
            font_header = ImageFont.load_default()
            font_title = ImageFont.load_default()
            font_text = ImageFont.load_default()
        
        # Header
        draw.text((sheet_width//2, 75), "DOCUMENTO PROFESIONAL", 
                 fill=(255, 255, 255), font=font_title, anchor="mm")
        
        y_pos = 200
        
        # Información estructurada
        info_data = [
            ("Empresa:", company if 'company' in locals() else ""),
            ("Departamento:", department if 'department' in locals() else ""),
            ("Preparado por:", prepared_by if 'prepared_by' in locals() else ""),
            ("Título:", doc_title if 'doc_title' in locals() else ""),
            ("Referencia:", doc_code if 'doc_code' in locals() else ""),
            ("Fecha:", date_work.strftime('%d/%m/%Y') if 'date_work' in locals() else ""),
        ]
        
        for label, value in info_data:
            draw.text((100, y_pos), f"{label}", fill=(17, 153, 142), font=font_header)
            draw.text((400, y_pos), value if value else "_____________________", 
                     fill=(50, 50, 50), font=font_text)
            y_pos += 70
        
        # Nivel de confidencialidad
        y_pos += 30
        conf_level = confidentiality if 'confidentiality' in locals() else "Interno"
        
        # Caja de confidencialidad
        conf_colors = {
            "Público": (76, 175, 80),
            "Interno": (33, 150, 243),
            "Confidencial": (255, 152, 0),
            "Restringido": (244, 67, 54)
        }
        conf_color = conf_colors.get(conf_level, (128, 128, 128))
        
        draw.rectangle([100, y_pos, sheet_width-100, y_pos+80], fill=conf_color)
        draw.text((sheet_width//2, y_pos+40), f"NIVEL: {conf_level.upper()}", 
                 fill=(255, 255, 255), font=font_header, anchor="mm")
        
        # Marca de agua
        draw.text((sheet_width-150, sheet_height-80), "Yan", 
                 fill=(200, 220, 215), font=font_header)
        
        return sheet
    
    return None

def add_watermark_to_image(img, text="Yan"):
    """Añade marca de agua 'Yan' a la imagen"""
    watermarked = img.copy()
    draw = ImageDraw.Draw(watermarked)
    
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = img.width - text_width - 30
    y = img.height - text_height - 30
    
    # Sombra
    draw.text((x+2, y+2), text, font=font, fill=(0, 0, 0, 100))
    # Texto
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 180))
    
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
                    
                    # Añadir marca de agua
                    image = add_watermark_to_image(image, "Yan")
                    
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
            
            # PREVISUALIZACIÓN
            if images_data:
                st.markdown("### 👁️ Vista Previa")
                
                preview_col1, preview_col2 = st.columns([2, 1])
                
                with preview_col1:
                    # Crear vista previa: Hoja de info + primera imagen
                    info_img = create_info_sheet_image(sheet_format)
                    
                    if info_img:
                        # Mostrar hoja de información primero
                        st.image(info_img, caption=f"Hoja de información: {sheet_format}", 
                                use_container_width=True)
                    
                    # Mostrar primera imagen procesada
                    st.image(images_data[0]['image'], 
                            caption=f"Primera imagen: {images_data[0]['name']} (con marca Yan)", 
                            use_container_width=True)
                
                with preview_col2:
                    # Información de la previsualización
                    st.markdown("### 📋 Detalles")
                    st.info(f"""
                    **Formato:** {sheet_format} {get_sheet_emoji()}
                    
                    **Hoja de info:** {'Sí' if show_info_sheet else 'No'}
                    
                    **Orientación:** {orientation}
                    
                    **Tamaño original:** {images_data[0]['original_size'][0]}×{images_data[0]['original_size'][1]} px
                    
                    **Tamaño final:** {images_data[0]['image'].width}×{images_data[0]['image'].height} px
                    
                    **Marca de agua:** Yan™
                    
                    **Total imágenes:** {len(images_data)}
                    """)
                    
                    # Lista de archivos
                    if len(images_data) > 1:
                        st.markdown("### 🖼️ Archivos incluidos")
                        for i, data in enumerate(images_data, 1):
                            st.caption(f"{i}. {data['name']}")
            
            # Botón de generación
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🚀 GENERAR PDF(S) CON MARCA YAN", key="convert", use_container_width=True):
                with st.spinner("Creando documentos profesionales..."):
                    
                    # Preparar imágenes finales
                    final_images = []
                    
                    # 1. Agregar hoja de información primero (si aplica)
                    if show_info_sheet:
                        info_sheet_img = create_info_sheet_image(sheet_format)
                        if info_sheet_img:
                            final_images.append(info_sheet_img)
                    
                    # 2. Agregar todas las imágenes procesadas
                    for data in images_data:
                        final_images.append(data['image'])
                    
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
                            "Regalo": ("#ff6b6b", "#ff9a9e", "🎁"),
                            "Trabajo/Profesional": ("#11998e", "#38ef7d", "💼"),
                            "Solo Imágenes": ("#667eea", "#764ba2", "🖼️")
                        }
                        
                        c1, c2, emoji = style_colors.get(sheet_format, ("#667eea", "#764ba2", "📄"))
                        
                        pages_count = len(final_images)
                        has_info = "incluye hoja de información" if show_info_sheet else "solo imágenes"
                        
                        st.markdown(f"""
                        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, {c1} 0%, {c2} 100%); border-radius: 15px; color: white; margin: 1rem 0;">
                            <h2>{emoji} ¡PDF Creado Exitosamente!</h2>
                            <p>Documento tipo {sheet_format} con marca de agua Yan</p>
                            <p style="font-size: 0.9rem; opacity: 0.9;">{pages_count} páginas • {has_info} • {quality} DPI</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.download_button(
                            label=f"📥 Descargar {project_name}.pdf",
                            data=pdf_buffer,
                            file_name=f"{project_name}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    
                    # PDFs individuales (solo imágenes, sin hoja de info para no repetir)
                    if output_format in ["PDFs separados", "Ambos"]:
                        st.markdown("### 📄 Archivos Individuales")
                        
                        individual_cols = st.columns(3)
                        for idx, data in enumerate(images_data):
                            with individual_cols[idx % 3]:
                                pdf_individual = io.BytesIO()
                                data['image'].save(pdf_individual, 'PDF', resolution=quality)
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
    st.info("💡 **Tip:** Selecciona un tipo de documento para agregar una hoja de información personalizada al inicio de tu PDF.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🚀 PDF Converter De Yan | Documentos profesionales con información personalizada</p>
    <p style="font-size: 0.8rem;">Hoja de información opcional • Marca de agua Yan™ • Hasta 50 archivos</p>
</div>
""", unsafe_allow_html=True)