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
    
    .info-sheet-party {
        border-left: 5px solid #FFD700;
        background: linear-gradient(to right, #fffbeb, white);
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
    <p style="font-size: 1.3rem; color: #666;">Imágenes coloridas con rotación personalizada y marca Yan</p>
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
        # Selector de tipo de documento con colores
        sheet_format = st.selectbox(
            "🎨 Estilo de Color",
            ["Natural", "Clase/Escolar (Azul)", "Regalo (Rosa)", "Trabajo (Verde)", "Fiesta (Dorado)"]
        )
        
        page_size = st.selectbox(
            "Tamaño de página",
            ["Original", "A4", "Carta", "Personalizado"]
        )
    
    with col4:
        # Orientación con visualización clara
        orientation = st.radio(
            "🔄 Orientación",
            ["Automática", "Vertical (↕️)", "Horizontal (↔️)"],
            horizontal=True
        )
        
        output_format = st.radio(
            "📦 Salida",
            ["PDF único", "PDFs separados", "Ambos"],
            horizontal=True
        )
    
    # Fila 2: Tamaño personalizado, nombre y ROTACIÓN MANUAL
    col5, col6, col7 = st.columns(3)
    
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
    
    with col7:
        st.markdown("**🎚️ Rotación Manual (grados)**")
        rotation_degrees = st.slider("Rotar imagen", 0, 360, 0, 90, 
                                   help="0 = sin rotación, 90 = derecha, 180 = invertida, 270 = izquierda")
        if rotation_degrees > 0:
            st.info(f"🔄 Se aplicará rotación de {rotation_degrees}°")
    
    st.markdown('</div>', unsafe_allow_html=True)

# HOJA DE INFORMACIÓN OPCIONAL
show_info_sheet = "Natural" not in sheet_format

if show_info_sheet:
    st.markdown("### 📝 Hoja de Información (Opcional)")
    
    with st.container():
        if "Clase" in sheet_format:
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
            
        elif "Regalo" in sheet_format:
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
            
        elif "Trabajo" in sheet_format:
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
            
        elif "Fiesta" in sheet_format:
            st.markdown('<div class="info-sheet info-sheet-party">', unsafe_allow_html=True)
            st.markdown("#### 🎉 Información de la Celebración")
            
            col_a, col_b = st.columns(2)
            with col_a:
                event_name = st.text_input("Nombre del evento", "")
                event_type = st.selectbox("Tipo de evento", ["Cumpleaños", "Boda", "Graduación", "Fiesta", "Reunión", "Otro"])
                host = st.text_input("Anfitrión/Organizador", "")
            with col_b:
                location = st.text_input("Lugar", "")
                date_event = st.date_input("Fecha del evento", datetime.now())
                time_event = st.text_input("Hora", "")
            
            details = st.text_area("Detalles o notas", "", height=100)
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
    """Aplica el perfil de color a la imagen SIN BORDES"""
    if profile["saturation"] != 1.0:
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(profile["saturation"])
    
    if profile["contrast"] != 1.0:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(profile["contrast"])
    
    if profile["brightness"] != 1.0:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(profile["brightness"])
    
    # Aplicar tinte sutil SIN bordes
    if profile["tint"]:
        tint_overlay = Image.new('RGB', img.size, profile["tint"])
        img = Image.blend(img, tint_overlay, 0.15)
    
    return img

def get_sheet_emoji():
    profile = get_color_profile()
    return profile["emoji"]

def apply_orientation(img):
    """Aplica orientación seleccionada y rotación manual"""
    # Primero aplicar orientación automática si no es "Automática"
    if orientation != "Automática":
        width, height = img.size
        is_landscape = width > height
        
        if "Vertical" in orientation and is_landscape:
            img = img.rotate(90, expand=True)
        elif "Horizontal" in orientation and not is_landscape:
            img = img.rotate(90, expand=True)
    
    # Luego aplicar rotación manual del usuario
    if rotation_degrees > 0:
        img = img.rotate(-rotation_degrees, expand=True)  # Negativo para rotar en sentido horario
    
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
    """Crea una imagen de la hoja de información con LETRAS GRANDES Y BONITAS"""
    if "Natural" in format_type:
        return None
    
    sheet_width, sheet_height = 1240, 1754
    
    # Colores según el tipo
    if "Clase" in format_type:
        bg_color = (102, 126, 234)
        header_color = (102, 126, 234)
        accent = "✏️"
        title_text = "INFORMACIÓN DEL ESTUDIANTE"
    elif "Regalo" in format_type:
        bg_color = (255, 107, 107)
        header_color = (255, 107, 107)
        accent = "🎁"
        title_text = "REGALO ESPECIAL"
    elif "Trabajo" in format_type:
        bg_color = (17, 153, 142)
        header_color = (17, 153, 142)
        accent = "💼"
        title_text = "DOCUMENTO PROFESIONAL"
    elif "Fiesta" in format_type:
        bg_color = (255, 193, 7)
        header_color = (218, 165, 32)
        accent = "🎉"
        title_text = "INFORMACIÓN DEL EVENTO"
    else:
        return None
    
    # Crear hoja blanca
    sheet = Image.new('RGB', (sheet_width, sheet_height), (255, 255, 255))
    draw = ImageDraw.Draw(sheet)
    
    # Intentar cargar fuentes bonitas y grandes
    try:
        # Fuentes grandes y decorativas
        font_title = ImageFont.truetype("arialbd.ttf", 80)  # Arial Bold grande
        font_header = ImageFont.truetype("arialbd.ttf", 60)
        font_text = ImageFont.truetype("arial.ttf", 50)
        font_label = ImageFont.truetype("arialbd.ttf", 45)
        font_watermark = ImageFont.truetype("arialbd.ttf", 70)
    except:
        try:
            # Alternativa si no existe arialbd
            font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 80)
            font_header = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
            font_text = ImageFont.truetype("DejaVuSans.ttf", 50)
            font_label = ImageFont.truetype("DejaVuSans-Bold.ttf", 45)
            font_watermark = ImageFont.truetype("DejaVuSans-Bold.ttf", 70)
        except:
            # Fallback
            font_title = ImageFont.load_default()
            font_header = ImageFont.load_default()
            font_text = ImageFont.load_default()
            font_label = ImageFont.load_default()
            font_watermark = ImageFont.load_default()
    
    # Header con color - TÍTULO MUY GRANDE
    header_height = 180
    draw.rectangle([0, 0, sheet_width, header_height], fill=header_color)
    
    # Título centrado y grande
    title_full = f"{accent} {title_text}"
    draw.text((sheet_width//2, header_height//2), title_full, 
             fill=(255, 255, 255), font=font_title, anchor="mm")
    
    # Línea decorativa gruesa
    line_y = header_height + 30
    draw.line([(50, line_y), (sheet_width-50, line_y)], fill=bg_color, width=8)
    
    # Contenido con letras GRANDES
    y_pos = line_y + 60
    line_height = 90  # Más espacio entre líneas
    
    if "Clase" in format_type:
        info_data = [
            ("👤 ESTUDIANTE:", student_name if 'student_name' in locals() and student_name else "_______________________________"),
            ("📚 MATERIA:", subject if 'subject' in locals() and subject else "_______________________________"),
            ("👨‍🏫 PROFESOR(A):", teacher if 'teacher' in locals() and teacher else "_______________________________"),
            ("🎓 GRADO/GRUPO:", grade if 'grade' in locals() and grade else "_______________________________"),
            ("📅 FECHA:", date_class.strftime('%d/%m/%Y') if 'date_class' in locals() else "_______________________________"),
            ("🏫 ESCUELA:", school if 'school' in locals() and school else "_______________________________"),
        ]
        
        for label, value in info_data:
            # Label en negrita y color
            draw.text((60, y_pos), label, fill=header_color, font=font_label)
            # Valor en texto normal grande
            draw.text((500, y_pos), value, fill=(50, 50, 50), font=font_text)
            y_pos += line_height
        
        # Tema en caja destacada
        y_pos += 30
        draw.rectangle([50, y_pos, sheet_width-50, y_pos+250], outline=bg_color, width=4)
        draw.text((70, y_pos+20), "📝 TEMA/DESCRIPCIÓN:", fill=header_color, font=font_label)
        topic_text = topic if 'topic' in locals() and topic else "________________________________________\n________________________________________\n________________________________________"
        draw.text((70, y_pos+90), topic_text, fill=(80, 80, 80), font=font_text)
        
    elif "Regalo" in format_type:
        # Diseño centrado y grande para regalo
        center_x = sheet_width // 2
        
        y_pos += 40
        draw.text((center_x, y_pos), "🎀 PARA 🎀", fill=header_color, font=font_header, anchor="mm")
        y_pos += 100
        recipient_text = recipient if 'recipient' in locals() and recipient else "_______________________________"
        draw.text((center_x, y_pos), recipient_text, fill=(50, 50, 50), font=font_title, anchor="mm")
        
        y_pos += 120
        draw.text((center_x, y_pos), "💝 OCASIÓN 💝", fill=header_color, font=font_header, anchor="mm")
        y_pos += 100
        occasion_text = occasion if 'occasion' in locals() else "_______________________________"
        draw.text((center_x, y_pos), occasion_text, fill=(50, 50, 50), font=font_title, anchor="mm")
        
        y_pos += 120
        draw.text((center_x, y_pos), "💌 DE PARTE DE 💌", fill=header_color, font=font_header, anchor="mm")
        y_pos += 100
        sender_text = sender if 'sender' in locals() and sender else "_______________________________"
        draw.text((center_x, y_pos), sender_text, fill=(50, 50, 50), font=font_title, anchor="mm")
        
        y_pos += 120
        draw.text((center_x, y_pos), "📅 FECHA 📅", fill=header_color, font=font_header, anchor="mm")
        y_pos += 100
        date_text = date_gift.strftime('%d/%m/%Y') if 'date_gift' in locals() else "_______________________________"
        draw.text((center_x, y_pos), date_text, fill=(50, 50, 50), font=font_title, anchor="mm")
        
        # Mensaje en caja decorativa
        y_pos += 150
        draw.rectangle([100, y_pos, sheet_width-100, y_pos+300], fill=(255, 240, 245), outline=bg_color, width=6)
        draw.text((center_x, y_pos+40), "✨ MENSAJE ESPECIAL ✨", fill=header_color, font=font_header, anchor="mm")
        msg_text = message if 'message' in locals() and message else "¡Con mucho cariño!"
        draw.text((center_x, y_pos+150), msg_text, fill=(80, 80, 80), font=font_text, anchor="mm")
        
    elif "Trabajo" in format_type:
        info_data = [
            ("🏢 EMPRESA:", company if 'company' in locals() and company else "_______________________________"),
            ("📂 DEPARTAMENTO:", department if 'department' in locals() and department else "_______________________________"),
            ("👤 PREPARADO POR:", prepared_by if 'prepared_by' in locals() and prepared_by else "_______________________________"),
            ("📋 TÍTULO:", doc_title if 'doc_title' in locals() and doc_title else "_______________________________"),
            ("🔖 REFERENCIA:", doc_code if 'doc_code' in locals() and doc_code else "_______________________________"),
            ("📅 FECHA:", date_work.strftime('%d/%m/%Y') if 'date_work' in locals() else "_______________________________"),
        ]
        
        for label, value in info_data:
            draw.text((60, y_pos), label, fill=header_color, font=font_label)
            draw.text((550, y_pos), value, fill=(50, 50, 50), font=font_text)
            y_pos += line_height
        
        # Confidencialidad en caja destacada
        y_pos += 40
        conf_level = confidentiality if 'confidentiality' in locals() else "Interno"
        conf_colors = {
            "Público": (76, 175, 80),
            "Interno": (33, 150, 243),
            "Confidencial": (255, 152, 0),
            "Restringido": (244, 67, 54)
        }
        conf_color = conf_colors.get(conf_level, (128, 128, 128))
        
        box_height = 120
        draw.rectangle([100, y_pos, sheet_width-100, y_pos+box_height], fill=conf_color)
        draw.text((sheet_width//2, y_pos+box_height//2), f"🔒 NIVEL: {conf_level.upper()} 🔒", 
                 fill=(255, 255, 255), font=font_header, anchor="mm")
        
    elif "Fiesta" in format_type:
        center_x = sheet_width // 2
        
        y_pos += 40
        draw.text((center_x, y_pos), "🎊 EVENTO 🎊", fill=header_color, font=font_header, anchor="mm")
        y_pos += 100
        event_text = event_name if 'event_name' in locals() and event_name else "_______________________________"
        draw.text((center_x, y_pos), event_text, fill=(50, 50, 50), font=font_title, anchor="mm")
        
        y_pos += 120
        draw.text((center_x, y_pos), "🎈 TIPO 🎈", fill=header_color, font=font_header, anchor="mm")
        y_pos += 100
        type_text = event_type if 'event_type' in locals() else "_______________________________"
        draw.text((center_x, y_pos), type_text, fill=(50, 50, 50), font=font_title, anchor="mm")
        
        y_pos += 120
        draw.text((center_x, y_pos), "🎭 ANFITRIÓN 🎭", fill=header_color, font=font_header, anchor="mm")
        y_pos += 100
        host_text = host if 'host' in locals() and host else "_______________________________"
        draw.text((center_x, y_pos), host_text, fill=(50, 50, 50), font=font_title, anchor="mm")
        
        y_pos += 120
        draw.text((center_x, y_pos), "📍 LUGAR 📍", fill=header_color, font=font_header, anchor="mm")
        y_pos += 100
        loc_text = location if 'location' in locals() and location else "_______________________________"
        draw.text((center_x, y_pos), loc_text, fill=(50, 50, 50), font=font_title, anchor="mm")
        
        y_pos += 120
        draw.text((center_x, y_pos), "📅 FECHA Y HORA 📅", fill=header_color, font=font_header, anchor="mm")
        y_pos += 100
        datetime_text = f"{date_event.strftime('%d/%m/%Y') if 'date_event' in locals() else '___/___/_____'} - {time_event if 'time_event' in locals() and time_event else '__:__'}"
        draw.text((center_x, y_pos), datetime_text, fill=(50, 50, 50), font=font_title, anchor="mm")
        
        # Detalles
        y_pos += 150
        draw.rectangle([50, y_pos, sheet_width-50, y_pos+200], outline=bg_color, width=4)
        draw.text((70, y_pos+20), "📝 DETALLES:", fill=header_color, font=font_label)
        details_text = details if 'details' in locals() and details else "________________________________________\n________________________________________"
        draw.text((70, y_pos+90), details_text, fill=(80, 80, 80), font=font_text)
    
    # Marca de agua Yan GRANDE al final
    watermark_y = sheet_height - 120
    draw.text((sheet_width//2, watermark_y), "Yan", 
             fill=(230, 230, 230), font=font_watermark, anchor="mm")
    
    return sheet

def add_watermark_to_image(img, text="Yan"):
    """Añade marca de agua 'Yan' a la imagen"""
    watermarked = img.copy()
    draw = ImageDraw.Draw(watermarked)
    
    try:
        font = ImageFont.truetype("arialbd.ttf", 60)
    except:
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
        except:
            font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = img.width - text_width - 50
    y = img.height - text_height - 50
    
    # Sombra
    for offset in range(4):
        draw.text((x+offset, y+offset), text, font=font, fill=(0, 0, 0, 60))
    # Texto blanco
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 200))
    
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
                orient_icon = "📱" if "Vertical" in orientation else "💻" if "Horizontal" in orientation else "🔄"
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
                    <h3>{orient_icon}</h3>
                    <p>{orientation.split('(')[0].strip()}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Procesar imágenes
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            images_data = []
            color_profile = get_color_profile()
            
            for idx, file in enumerate(valid_files):
                try:
                    image = Image.open(file)
                    original_size = image.size
                    
                    # PASO 1: Aplicar orientación y rotación manual
                    image = apply_orientation(image)
                    
                    # PASO 2: Redimensionar
                    image = resize_to_page_size(image)
                    
                    # PASO 3: Aplicar perfil de color vibrante SIN BORDES
                    image = apply_color_profile(image, color_profile)
                    
                    # PASO 4: Convertir a RGB
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
                    
                    # PASO 5: Añadir marca de agua
                    image = add_watermark_to_image(image, "Yan")
                    
                    # Detectar si hubo rotación
                    was_rotated = (original_size[0] > original_size[1]) != (image.size[0] > image.size[1]) or rotation_degrees > 0
                    
                    images_data.append({
                        'image': image,
                        'name': os.path.splitext(file.name)[0],
                        'original': file,
                        'original_size': original_size,
                        'was_rotated': was_rotated,
                        'rotation_applied': rotation_degrees if rotation_degrees > 0 else "orientación"
                    })
                    
                    progress = (idx + 1) / len(valid_files)
                    progress_bar.progress(int(progress * 100))
                    status_text.text(f"Procesando {idx + 1} de {len(valid_files)}... 🎨 {sheet_format} 🔄 Rotación: {rotation_degrees}°")
                    
                except Exception as e:
                    st.error(f"Error con {file.name}: {str(e)}")
            
            progress_bar.empty()
            status_text.success(f"✅ ¡{len(images_data)} imágenes procesadas!")
            
            # PREVISUALIZACIÓN
            if images_data:
                st.markdown("### 👁️ Vista Previa")
                
                preview_col1, preview_col2 = st.columns([2, 1])
                
                with preview_col1:
                    # Mostrar hoja de información si aplica
                    info_img = create_info_sheet_image(sheet_format)
                    if info_img:
                        st.image(info_img, caption=f"📄 Hoja de información: {sheet_format}", 
                                use_container_width=True)
                    
                    # Mostrar primera imagen procesada
                    first_data = images_data[0]
                    st.image(first_data['image'], 
                            caption=f"🖼️ {first_data['name']} • Estilo: {sheet_format} • Marca: Yan", 
                            use_container_width=True)
                    
                    # Indicador de rotación
                    if first_data['was_rotated']:
                        rot_type = f"{first_data['rotation_applied']}°" if isinstance(first_data['rotation_applied'], int) else first_data['rotation_applied']
                        st.info(f"🔄 Imagen rotada: {rot_type}")
                
                with preview_col2:
                    # Información detallada
                    st.markdown("### 📋 Detalles del Proceso")
                    
                    # Mostrar cambios aplicados
                    changes = []
                    if "Natural" not in sheet_format:
                        changes.append(f"🎨 Color: {sheet_format}")
                    if first_data['was_rotated']:
                        changes.append(f"🔄 Rotación: {rotation_degrees}°" if rotation_degrees > 0 else f"🔄 Orientación: {orientation}")
                    changes.append("💧 Marca de agua Yan")
                    
                    for change in changes:
                        st.success(change)
                    
                    # Especificaciones técnicas
                    st.markdown("#### 📐 Especificaciones")
                    st.code(f"""
Original:     {first_data['original_size'][0]}×{first_data['original_size'][1]} px
Final:        {first_data['image'].width}×{first_data['image'].height} px
Rotación:     {rotation_degrees}° manual
Orientación:  {orientation.split('(')[0]}
Perfil color: {sheet_format}
Total imgs:   {len(images_data)}
                    """)
                    
                    # Lista de archivos
                    if len(images_data) > 1:
                        st.markdown("#### 🗂️ Archivos incluidos")
                        for i, data in enumerate(images_data, 1):
                            rotated = " 🔄" if data['was_rotated'] else ""
                            st.caption(f"{i}. {data['name']}{rotated}")
            
            # Botón de generación
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🚀 GENERAR PDF(S) CON MARCA YAN", key="convert", use_container_width=True):
                with st.spinner("Creando documentos vibrantes..."):
                    
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
                        
                        # Resumen visual del resultado
                        st.markdown(f"""
                        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white; margin: 1rem 0;">
                            <h2>✨ ¡PDF Creado con Éxito! ✨</h2>
                            <p>Estilo: <b>{sheet_format}</b> • {len(final_images)} páginas</p>
                            <p style="font-size: 0.9rem; opacity: 0.9;">
                                Rotación: {rotation_degrees}° • 
                                {len([d for d in images_data if d['was_rotated']])} imágenes ajustadas • 
                                Calidad {quality} DPI • 
                                Marca Yan™
                            </p>
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
    st.info("💡 **Tip:** Ajusta la rotación manual (0-360°) para orientar tus imágenes exactamente como deseas.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🚀 PDF Converter De Yan | Letras grandes, rotación personalizada y estilos vibrantes</p>
    <p style="font-size: 0.8rem;">Fuentes grandes y bonitas • Rotación 0-360° • Sin bordes • Marca Yan™</p>
</div>
""", unsafe_allow_html=True)