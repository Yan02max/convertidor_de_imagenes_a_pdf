import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import io
import os
from datetime import datetime

# Configuración de página optimizada
st.set_page_config(
    page_title="Converter - Imagen a PDF De Yan", 
    icon="🚀",
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
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'preview_images' not in st.session_state:
    st.session_state.preview_images = []
    st.session_state.processed_files = 0
    st.session_state.total_size = 0

# Header
st.markdown("""
<div class="main-header">
    <h1 style="font-size: 3.5rem; background: linear-gradient(45deg, #2196F3, #4CAF50); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        🚀 PDF Converter Yan
    </h1>
    <p style="font-size: 1.3rem; color: #666;">Hojas de información grandes y visibles desde lejos</p>
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
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        max_files = st.number_input("Máximo archivos", 1, 50, 20)
        quality = st.slider("Calidad PDF (DPI)", 50, 300, 150)
    
    with col2:
        max_file_size = st.number_input("Tamaño máx. (MB)", 1, 100, 50)
        margin = st.slider("Margen (mm)", 0, 50, 0)
    
    with col3:
        sheet_format = st.selectbox(
            "🎨 Estilo de Color",
            ["Natural", "Clase/Escolar (Azul)", "Regalo (Rosa)", "Trabajo (Verde)", "Fiesta (Dorado)"]
        )
        
        page_size = st.selectbox(
            "Tamaño de página",
            ["Original", "A4", "Carta", "Personalizado"]
        )
    
    with col4:
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
    
    col5, col6, col7 = st.columns(3)
    
    custom_width, custom_height = 210, 297
    with col5:
        if page_size == "Personalizado":
            st.markdown("**Dimensiones:**")
            c1, c2 = st.columns(2)
            with c1:
                custom_width = st.number_input("Ancho (mm)", 50, 500, 210)
            with c2:
                custom_height = st.number_input("Alto (mm)", 50, 500, 297)
    
    with col6:
        project_name = st.text_input(
            "📝 Nombre del proyecto",
            value=f"Proyecto_Yan_{datetime.now().strftime('%Y%m%d')}"
        )
    
    with col7:
        st.markdown("**🎚️ Rotación Manual**")
        rotation_degrees = st.slider("Grados", 0, 360, 0, 90)
        if rotation_degrees > 0:
            st.info(f"🔄 Rotación: {rotation_degrees}°")
    
    st.markdown('</div>', unsafe_allow_html=True)

# HOJA DE INFORMACIÓN OPCIONAL - CAMPOS GRANDES Y VISIBLES
show_info_sheet = "Natural" not in sheet_format

if show_info_sheet:
    st.markdown("### 📝 Hoja de Información (Opcional)")
    
    with st.container():
        if "Clase" in sheet_format:
            st.markdown("#### ✏️ Información del Estudiante")
            
            col_a, col_b = st.columns(2)
            with col_a:
                student_name = st.text_input("👤 NOMBRE DEL ESTUDIANTE", "", 
                                           help="Escribe en mayúsculas para mejor visibilidad")
                subject = st.text_input("📚 MATERIA/ASIGNATURA", "")
                teacher = st.text_input("👨‍🏫 PROFESOR(A)", "")
            with col_b:
                grade = st.text_input("🎓 GRADO/GRUPO", "")
                date_class = st.date_input("📅 FECHA", datetime.now())
                school = st.text_input("🏫 ESCUELA/INSTITUCIÓN", "")
            
            topic = st.text_area("📝 TEMA O DESCRIPCIÓN", "", height=150,
                               help="Este texto aparecerá grande en la hoja de presentación")
            
        elif "Regalo" in sheet_format:
            st.markdown("#### 🎁 Información del Regalo")
            
            col_a, col_b = st.columns(2)
            with col_a:
                recipient = st.text_input("🎀 PARA (DESTINATARIO)", "", 
                                        help="Nombre de quien recibe el regalo")
                occasion = st.selectbox("💝 OCASIÓN", 
                                        ["CUMPLEAÑOS 🎂", "ANIVERSARIO 💕", "NAVIDAD 🎄", 
                                         "SAN VALENTÍN ❤️", "GRADUACIÓN 🎓", "OTRO 🎈"])
            with col_b:
                sender = st.text_input("💌 DE PARTE DE (REMITENTE)", "")
                date_gift = st.date_input("📅 FECHA DEL REGALO", datetime.now())
            
            message = st.text_area("✨ MENSAJE ESPECIAL", "¡CON MUCHO CARIÑO! ❤️", height=150,
                               help="Este mensaje se verá muy grande en el PDF")
            
        elif "Trabajo" in sheet_format:
            st.markdown("#### 💼 Información del Documento")
            
            col_a, col_b = st.columns(2)
            with col_a:
                company = st.text_input("🏢 EMPRESA/ORGANIZACIÓN", "",
                                      help="Nombre completo de la empresa")
                department = st.text_input("📂 DEPARTAMENTO", "")
                prepared_by = st.text_input("👤 PREPARADO POR", "")
            with col_b:
                doc_title = st.text_input("📋 TÍTULO DEL DOCUMENTO", "",
                                        help="Título principal visible desde lejos")
                doc_code = st.text_input("🔖 CÓDIGO/REFERENCIA", "")
                date_work = st.date_input("📅 FECHA", datetime.now())
            
            confidentiality = st.select_slider(
                "🔒 NIVEL DE CONFIDENCIALIDAD",
                options=["PÚBLICO 🌐", "INTERNO 📋", "CONFIDENCIAL 🔐", "RESTRINGIDO 🚫"],
                value="INTERNO 📋"
            )
            
        elif "Fiesta" in sheet_format:
            st.markdown("#### 🎉 Información de la Celebración")
            
            col_a, col_b = st.columns(2)
            with col_a:
                event_name = st.text_input("🎊 NOMBRE DEL EVENTO", "",
                                         help="Nombre llamativo y grande")
                event_type = st.selectbox("🎈 TIPO DE EVENTO",
                                        ["CUMPLEAÑOS 🎂", "BODA 💒", "GRADUACIÓN 🎓", 
                                         "FIESTA 🎉", "REUNIÓN 🤝", "OTRO 🎁"])
                host = st.text_input("🎭 ANFITRIÓN/ORGANIZADOR", "")
            with col_b:
                location = st.text_input("📍 LUGAR/UBICACIÓN", "")
                date_event = st.date_input("📅 FECHA DEL EVENTO", datetime.now())
                time_event = st.text_input("⏰ HORA", "00:00")
            
            details = st.text_area("📝 DETALLES IMPORTANTES", "", height=150,
                               help="Información adicional visible desde lejos")

def get_color_profile():
    """Retorna el perfil de color según el formato seleccionado"""
    profiles = {
        "Natural": {
            "saturation": 1.0,
            "contrast": 1.0,
            "brightness": 1.0,
            "tint": None,
            "emoji": "🖼️",
            "header_color": (100, 100, 100),
            "accent_color": (150, 150, 150)
        },
        "Clase/Escolar (Azul)": {
            "saturation": 1.2,
            "contrast": 1.1,
            "brightness": 1.05,
            "tint": (180, 200, 255),
            "emoji": "✏️",
            "header_color": (41, 98, 255),  # Azul fuerte
            "accent_color": (102, 126, 234)
        },
        "Regalo (Rosa)": {
            "saturation": 1.3,
            "contrast": 1.0,
            "brightness": 1.1,
            "tint": (255, 200, 220),
            "emoji": "🎁",
            "header_color": (255, 20, 147),  # Rosa fuerte
            "accent_color": (255, 105, 180)
        },
        "Trabajo (Verde)": {
            "saturation": 1.1,
            "contrast": 1.15,
            "brightness": 1.0,
            "tint": (200, 255, 220),
            "emoji": "💼",
            "header_color": (0, 128, 0),  # Verde oscuro
            "accent_color": (17, 153, 142)
        },
        "Fiesta (Dorado)": {
            "saturation": 1.4,
            "contrast": 1.2,
            "brightness": 1.15,
            "tint": (255, 235, 180),
            "emoji": "🎉",
            "header_color": (218, 165, 32),  # Dorado
            "accent_color": (255, 193, 7)
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
    
    if profile["tint"]:
        tint_overlay = Image.new('RGB', img.size, profile["tint"])
        img = Image.blend(img, tint_overlay, 0.15)
    
    return img

def get_sheet_emoji():
    profile = get_color_profile()
    return profile["emoji"]

def apply_orientation(img):
    """Aplica orientación seleccionada y rotación manual"""
    if orientation != "Automática":
        width, height = img.size
        is_landscape = width > height
        
        if "Vertical" in orientation and is_landscape:
            img = img.rotate(90, expand=True)
        elif "Horizontal" in orientation and not is_landscape:
            img = img.rotate(90, expand=True)
    
    if rotation_degrees > 0:
        img = img.rotate(-rotation_degrees, expand=True)
    
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
    """Crea una imagen de la hoja de información que CUBRE TODO EL ESPACIO con letras GRANDES"""
    if "Natural" in format_type:
        return None
    
    # Tamaño A4 en alta resolución (300 DPI para mejor calidad)
    sheet_width, sheet_height = 2480, 3508
    
    profile = get_color_profile()
    header_color = profile["header_color"]
    accent_color = profile["accent_color"]
    
    # Colores y emojis según el tipo
    if "Clase" in format_type:
        bg_color = (240, 248, 255)  # Azul muy claro
        title_text = "📚 INFORMACIÓN DEL ESTUDIANTE 📚"
        emoji_deco = ["✏️", "📖", "🎓", "⭐", "🏆"]
    elif "Regalo" in format_type:
        bg_color = (255, 240, 245)  # Rosa muy claro
        title_text = "🎁 REGALO ESPECIAL 🎁"
        emoji_deco = ["💝", "🎀", "✨", "🌟", "❤️"]
    elif "Trabajo" in format_type:
        bg_color = (240, 255, 240)  # Verde muy claro
        title_text = "💼 DOCUMENTO PROFESIONAL 💼"
        emoji_deco = ["📊", "💻", "📈", "✅", "🏢"]
    elif "Fiesta" in format_type:
        bg_color = (255, 250, 240)  # Crema/dorado claro
        title_text = "🎉 INFORMACIÓN DEL EVENTO 🎉"
        emoji_deco = ["🎊", "🎈", "🥳", "✨", "🎵"]
    else:
        return None
    
    # Crear hoja con fondo de color suave
    sheet = Image.new('RGB', (sheet_width, sheet_height), bg_color)
    draw = ImageDraw.Draw(sheet)
    
    # Intentar cargar fuentes grandes y bonitas
    try:
        # Fuentes muy grandes para visibilidad desde lejos
        font_title = ImageFont.truetype("arialbd.ttf", 180)      # Título enorme
        font_header = ImageFont.truetype("arialbd.ttf", 120)   # Headers grandes
        font_text = ImageFont.truetype("arialbd.ttf", 100)     # Texto grande
        font_label = ImageFont.truetype("arialbd.ttf", 90)     # Labels
        font_emoji = ImageFont.truetype("seguiemj.ttf", 200)     # Emojis grandes (Windows)
    except:
        try:
            font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 180)
            font_header = ImageFont.truetype("DejaVuSans-Bold.ttf", 120)
            font_text = ImageFont.truetype("DejaVuSans-Bold.ttf", 100)
            font_label = ImageFont.truetype("DejaVuSans-Bold.ttf", 90)
            font_emoji = ImageFont.truetype("DejaVuSans.ttf", 200)
        except:
            # Fallback con fuentes grandes aunque sean default
            font_title = ImageFont.load_default()
            font_header = ImageFont.load_default()
            font_text = ImageFont.load_default()
            font_label = ImageFont.load_default()
            font_emoji = ImageFont.load_default()
    
    # Dibujar emojis decorativos en las esquinas GRANDES
    # Esquina superior izquierda
    draw.text((80, 80), emoji_deco[0], fill=header_color, font=font_emoji)
    # Esquina superior derecha
    draw.text((sheet_width - 280, 80), emoji_deco[1], fill=header_color, font=font_emoji)
    # Esquina inferior izquierda
    draw.text((80, sheet_height - 280), emoji_deco[2], fill=header_color, font=font_emoji)
    # Esquina inferior derecha
    draw.text((sheet_width - 280, sheet_height - 280), emoji_deco[3], fill=header_color, font=font_emoji)
    
    # Banda superior con título ENORME
    header_height = 400
    draw.rectangle([0, 0, sheet_width, header_height], fill=header_color)
    
    # Título centrado y muy grande
    draw.text((sheet_width//2, header_height//2), title_text, 
             fill=(255, 255, 255), font=font_title, anchor="mm")
    
    # Emojis adicionales en el header
    draw.text((150, header_height//2), emoji_deco[4], fill=(255, 255, 255), font=font_emoji, anchor="mm")
    draw.text((sheet_width - 150, header_height//2), emoji_deco[4], fill=(255, 255, 255), font=font_emoji, anchor="mm")
    
    # Línea decorativa gruesa
    line_y = header_height + 50
    draw.line([(100, line_y), (sheet_width-100, line_y)], fill=accent_color, width=20)
    
    # CONTENIDO PRINCIPAL - OCUPA TODO EL ESPACIO
    margin = 150
    content_width = sheet_width - (2 * margin)
    y_pos = line_y + 100
    
    # Función para dibujar secciones grandes
    def draw_big_section(label, value, emoji_icon, y_position):
        # Fondo de la sección
        section_height = 350
        draw.rectangle([margin, y_position, sheet_width-margin, y_position+section_height], 
                      outline=accent_color, width=8)
        
        # Emoji grande a la izquierda
        draw.text((margin + 50, y_position + section_height//2), 
                 emoji_icon, fill=header_color, font=font_emoji, anchor="mm")
        
        # Label arriba grande
        draw.text((margin + 200, y_position + 60), label, 
                 fill=header_color, font=font_label)
        
        # Valor enorme en el centro
        display_value = value.upper() if value else "________________________"
        # Truncar si es muy largo pero mantener fuente grande
        if len(display_value) > 30:
            display_value = display_value[:27] + "..."
        
        draw.text((sheet_width//2, y_position + section_height//2 + 30), 
                 display_value, fill=(50, 50, 50), font=font_header, anchor="mm")
        
        return y_position + section_height + 80
    
    if "Clase" in format_type:
        # Secciones grandes para clase
        y_pos = draw_big_section("ESTUDIANTE", 
                                student_name if 'student_name' in locals() else "", 
                                "👤", y_pos)
        y_pos = draw_big_section("MATERIA", 
                                subject if 'subject' in locals() else "", 
                                "📚", y_pos)
        y_pos = draw_big_section("PROFESOR(A)", 
                                teacher if 'teacher' in locals() else "", 
                                "👨‍🏫", y_pos)
        y_pos = draw_big_section("GRADO/GRUPO", 
                                grade if 'grade' in locals() else "", 
                                "🎓", y_pos)
        y_pos = draw_big_section("FECHA", 
                                date_class.strftime('%d/%m/%Y') if 'date_class' in locals() else "", 
                                "📅", y_pos)
        y_pos = draw_big_section("ESCUELA", 
                                school if 'school' in locals() else "", 
                                "🏫", y_pos)
        
        # Tema en caja grande al final
        topic_box_height = 500
        draw.rectangle([margin, y_pos, sheet_width-margin, y_pos+topic_box_height], 
                      fill=(255, 255, 255), outline=header_color, width=12)
        draw.text((sheet_width//2, y_pos + 80), "📝 TEMA 📝", 
                 fill=header_color, font=font_header, anchor="mm")
        
        topic_text = topic if 'topic' in locals() and topic else "________________________\n________________________\n________________________"
        # Dividir texto en líneas si es largo
        lines = topic_text.split('\n')[:4]  # Máximo 4 líneas
        line_y = y_pos + 200
        for line in lines:
            draw.text((sheet_width//2, line_y), line.upper(), 
                     fill=(80, 80, 80), font=font_text, anchor="mm")
            line_y += 120
        
    elif "Regalo" in format_type:
        # Diseño centrado y muy grande para regalo
        center_x = sheet_width // 2
        
        # Destinatario grande
        y_pos += 50
        draw.rectangle([margin, y_pos, sheet_width-margin, y_pos+400], 
                      fill=(255, 255, 255), outline=header_color, width=10)
        draw.text((center_x, y_pos + 80), "🎀 PARA 🎀", 
                 fill=header_color, font=font_header, anchor="mm")
        recipient_text = (recipient if 'recipient' in locals() and recipient else "________________________").upper()
        draw.text((center_x, y_pos + 250), recipient_text, 
                 fill=(50, 50, 50), font=font_title, anchor="mm")
        y_pos += 480
        
        # Ocasión
        draw.rectangle([margin, y_pos, sheet_width-margin, y_pos+350], 
                      fill=header_color, outline=accent_color, width=10)
        draw.text((center_x, y_pos + 80), "💝 OCASIÓN 💝", 
                 fill=(255, 255, 255), font=font_header, anchor="mm")
        occasion_text = occasion if 'occasion' in locals() else "________________________"
        draw.text((center_x, y_pos + 220), occasion_text, 
                 fill=(255, 255, 255), font=font_title, anchor="mm")
        y_pos += 430
        
        # Remitente
        draw.rectangle([margin, y_pos, sheet_width-margin, y_pos+350], 
                      fill=(255, 255, 255), outline=header_color, width=10)
        draw.text((center_x, y_pos + 80), "💌 DE PARTE DE 💌", 
                 fill=header_color, font=font_header, anchor="mm")
        sender_text = (sender if 'sender' in locals() and sender else "________________________").upper()
        draw.text((center_x, y_pos + 220), sender_text, 
                 fill=(50, 50, 50), font=font_title, anchor="mm")
        y_pos += 430
        
        # Fecha
        draw.rectangle([margin, y_pos, sheet_width-margin, y_pos+300], 
                      outline=accent_color, width=8)
        draw.text((center_x, y_pos + 80), "📅 FECHA 📅", 
                 fill=header_color, font=font_header, anchor="mm")
        date_text = date_gift.strftime('%d/%m/%Y') if 'date_gift' in locals() else "________________________"
        draw.text((center_x, y_pos + 200), date_text, 
                 fill=(50, 50, 50), font=font_title, anchor="mm")
        y_pos += 380
        
        # Mensaje especial - CAJA ENORME
        msg_box_height = 700
        draw.rectangle([margin, y_pos, sheet_width-margin, y_pos+msg_box_height], 
                      fill=(255, 240, 245), outline=header_color, width=15)
        draw.text((center_x, y_pos + 100), "✨ MENSAJE ESPECIAL ✨", 
                 fill=header_color, font=font_header, anchor="mm")
        
        msg_text = message if 'message' in locals() and message else "¡CON MUCHO CARIÑO!"
        # Centrar mensaje y hacerlo grande
        draw.text((center_x, y_pos + msg_box_height//2 + 50), msg_text.upper(), 
                 fill=(255, 20, 147), font=font_title, anchor="mm")
        
    elif "Trabajo" in format_type:
        # Secciones grandes para trabajo
        y_pos = draw_big_section("EMPRESA", 
                                company if 'company' in locals() else "", 
                                "🏢", y_pos)
        y_pos = draw_big_section("DEPARTAMENTO", 
                                department if 'department' in locals() else "", 
                                "📂", y_pos)
        y_pos = draw_big_section("PREPARADO POR", 
                                prepared_by if 'prepared_by' in locals() else "", 
                                "👤", y_pos)
        y_pos = draw_big_section("TÍTULO DEL DOCUMENTO", 
                                doc_title if 'doc_title' in locals() else "", 
                                "📋", y_pos)
        y_pos = draw_big_section("REFERENCIA", 
                                doc_code if 'doc_code' in locals() else "", 
                                "🔖", y_pos)
        y_pos = draw_big_section("FECHA", 
                                date_work.strftime('%d/%m/%Y') if 'date_work' in locals() else "", 
                                "📅", y_pos)
        
        # Confidencialidad - CAJA DESTACADA
        conf_box_height = 400
        draw.rectangle([margin, y_pos, sheet_width-margin, y_pos+conf_box_height], 
                      fill=header_color, outline=accent_color, width=15)
        
        conf_level = confidentiality if 'confidentiality' in locals() else "INTERNO 📋"
        draw.text((sheet_width//2, y_pos + 100), "🔒 NIVEL DE CONFIDENCIALIDAD 🔒", 
                 fill=(255, 255, 255), font=font_header, anchor="mm")
        draw.text((sheet_width//2, y_pos + conf_box_height//2 + 50), conf_level, 
                 fill=(255, 255, 255), font=font_title, anchor="mm")
        
    elif "Fiesta" in format_type:
        center_x = sheet_width // 2
        
        # Evento grande
        y_pos += 30
        draw.rectangle([margin, y_pos, sheet_width-margin, y_pos+400], 
                      fill=(255, 255, 255), outline=header_color, width=10)
        draw.text((center_x, y_pos + 80), "🎊 EVENTO 🎊", 
                 fill=header_color, font=font_header, anchor="mm")
        event_text = (event_name if 'event_name' in locals() and event_name else "________________________").upper()
        draw.text((center_x, y_pos + 250), event_text, 
                 fill=(50, 50, 50), font=font_title, anchor="mm")
        y_pos += 480
        
        # Tipo
        draw.rectangle([margin, y_pos, sheet_width-margin, y_pos+350], 
                      fill=header_color, outline=accent_color, width=10)
        draw.text((center_x, y_pos + 80), "🎈 TIPO DE EVENTO 🎈", 
                 fill=(255, 255, 255), font=font_header, anchor="mm")
        type_text = event_type if 'event_type' in locals() else "________________________"
        draw.text((center_x, y_pos + 220), type_text, 
                 fill=(255, 255, 255), font=font_title, anchor="mm")
        y_pos += 430
        
        # Anfitrión
        draw.rectangle([margin, y_pos, sheet_width-margin, y_pos+350], 
                      fill=(255, 255, 255), outline=header_color, width=10)
        draw.text((center_x, y_pos + 80), "🎭 ANFITRIÓN 🎭", 
                 fill=header_color, font=font_header, anchor="mm")
        host_text = (host if 'host' in locals() and host else "________________________").upper()
        draw.text((center_x, y_pos + 220), host_text, 
                 fill=(50, 50, 50), font=font_title, anchor="mm")
        y_pos += 430
        
        # Lugar
        draw.rectangle([margin, y_pos, sheet_width-margin, y_pos+350], 
                      fill=header_color, outline=accent_color, width=10)
        draw.text((center_x, y_pos + 80), "📍 LUGAR 📍", 
                 fill=(255, 255, 255), font=font_header, anchor="mm")
        loc_text = (location if 'location' in locals() and location else "________________________").upper()
        draw.text((center_x, y_pos + 220), loc_text, 
                 fill=(255, 255, 255), font=font_title, anchor="mm")
        y_pos += 430
        
        # Fecha y hora
        draw.rectangle([margin, y_pos, sheet_width-margin, y_pos+300], 
                      outline=header_color, width=8)
        draw.text((center_x, y_pos + 80), "📅 FECHA Y HORA 📅", 
                 fill=header_color, font=font_header, anchor="mm")
        datetime_text = f"{date_event.strftime('%d/%m/%Y') if 'date_event' in locals() else '__/__/____'} - {time_event if 'time_event' in locals() and time_event else '__:__'}"
        draw.text((center_x, y_pos + 200), datetime_text, 
                 fill=(50, 50, 50), font=font_title, anchor="mm")
        y_pos += 380
        
        # Detalles
        details_box_height = 500
        draw.rectangle([margin, y_pos, sheet_width-margin, y_pos+details_box_height], 
                      fill=(255, 250, 240), outline=header_color, width=10)
        draw.text((center_x, y_pos + 80), "📝 DETALLES 📝", 
                 fill=header_color, font=font_header, anchor="mm")
        
        details_text = details if 'details' in locals() and details else "________________________________\n________________________________\n________________________________"
        lines = details_text.split('\n')[:3]
        line_y = y_pos + 200
        for line in lines:
            draw.text((center_x, line_y), line.upper(), 
                     fill=(80, 80, 80), font=font_text, anchor="mm")
            line_y += 120
    
    # Marca de agua Yan GRANDE al final
    watermark_y = sheet_height - 200
    try:
        font_watermark = ImageFont.truetype("arialbd.ttf", 150)
    except:
        font_watermark = ImageFont.load_default()
    
    draw.text((sheet_width//2, watermark_y), "Yan", 
             fill=(220, 220, 220), font=font_watermark, anchor="mm")
    
    # Redimensionar a resolución estándar para el PDF
    sheet = sheet.resize((1240, 1754), Image.Resampling.LANCZOS)
    
    return sheet

def add_watermark_to_image(img, text="Yan"):
    """Añade marca de agua 'Yan' a la imagen"""
    watermarked = img.copy()
    draw = ImageDraw.Draw(watermarked)
    
    try:
        font = ImageFont.truetype("arialbd.ttf", 60)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = img.width - text_width - 50
    y = img.height - text_height - 50
    
    for offset in range(4):
        draw.text((x+offset, y+offset), text, font=font, fill=(0, 0, 0, 60))
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
                    
                    image = apply_orientation(image)
                    image = resize_to_page_size(image)
                    image = apply_color_profile(image, color_profile)
                    
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
                    
                    image = add_watermark_to_image(image, "Yan")
                    
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
                    status_text.text(f"Procesando {idx + 1} de {len(valid_files)}... 🎨 {sheet_format}")
                    
                except Exception as e:
                    st.error(f"Error con {file.name}: {str(e)}")
            
            progress_bar.empty()
            status_text.success(f"✅ ¡{len(images_data)} imágenes procesadas!")
            
            # PREVISUALIZACIÓN
            if images_data:
                st.markdown("### 👁️ Vista Previa")
                
                preview_col1, preview_col2 = st.columns([2, 1])
                
                with preview_col1:
                    info_img = create_info_sheet_image(sheet_format)
                    if info_img:
                        st.image(info_img, caption=f"📄 Hoja de información: {sheet_format} (LETRA GRANDE)", 
                                use_container_width=True)
                    
                    first_data = images_data[0]
                    st.image(first_data['image'], 
                            caption=f"🖼️ {first_data['name']} • Estilo: {sheet_format} • Marca: Yan", 
                            use_container_width=True)
                    
                    if first_data['was_rotated']:
                        rot_type = f"{first_data['rotation_applied']}°" if isinstance(first_data['rotation_applied'], int) else first_data['rotation_applied']
                        st.info(f"🔄 Imagen rotada: {rot_type}")
                
                with preview_col2:
                    st.markdown("### 📋 Detalles del Proceso")
                    
                    changes = []
                    if "Natural" not in sheet_format:
                        changes.append(f"🎨 Color: {sheet_format}")
                    if first_data['was_rotated']:
                        changes.append(f"🔄 Rotación: {rotation_degrees}°" if rotation_degrees > 0 else f"🔄 Orientación: {orientation}")
                    changes.append("💧 Marca de agua Yan")
                    
                    for change in changes:
                        st.success(change)
                    
                    st.markdown("#### 📐 Especificaciones")
                    st.code(f"""
Original:     {first_data['original_size'][0]}×{first_data['original_size'][1]} px
Final:        {first_data['image'].width}×{first_data['image'].height} px
Rotación:     {rotation_degrees}° manual
Orientación:  {orientation.split('(')[0]}
Perfil color: {sheet_format}
Total imgs:   {len(images_data)}
                    """)
                    
                    if len(images_data) > 1:
                        st.markdown("#### 🗂️ Archivos incluidos")
                        for i, data in enumerate(images_data, 1):
                            rotated = " 🔄" if data['was_rotated'] else ""
                            st.caption(f"{i}. {data['name']}{rotated}")
            
            # Botón de generación
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🚀 GENERAR PDF(S) CON MARCA YAN", key="convert", use_container_width=True):
                with st.spinner("Creando documentos con letras grandes..."):
                    
                    final_images = []
                    
                    if show_info_sheet:
                        info_sheet_img = create_info_sheet_image(sheet_format)
                        if info_sheet_img:
                            final_images.append(info_sheet_img)
                    
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
                        
                        st.markdown(f"""
                        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white; margin: 1rem 0;">
                            <h2>✨ ¡PDF Creado con Éxito! ✨</h2>
                            <p>Estilo: <b>{sheet_format}</b> • {len(final_images)} páginas</p>
                            <p style="font-size: 0.9rem; opacity: 0.9;">
                                Letras GRANDES • Rotación: {rotation_degrees}° • 
                                {len([d for d in images_data if d['was_rotated']])} imágenes ajustadas • 
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
    st.info("💡 **Tip:** Las hojas de información usan letras  grandes (hasta 180px) para ser mas visibles. ¡Perfecto para presentaciones!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🚀 PDF Converter De Yan | visibilidad total</p>
    <p style="font-size: 0.8rem;">Fuentes hasta 180px • Emojis decorativos • Cubre toda la página • Marca Yan™</p>
</div>
""", unsafe_allow_html=True)