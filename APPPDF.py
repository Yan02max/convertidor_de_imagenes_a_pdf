import streamlit as st
from PIL import Image
import io
import os
import base64
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
    /* Animaciones y efectos */
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
    
    .progress-container {
        background: #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
        height: 30px;
        margin: 1rem 0;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #4CAF50, #8BC34A);
        transition: width 0.5s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
    }
    
    .file-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #4CAF50;
        transition: transform 0.2s;
    }
    
    .file-card:hover {
        transform: translateX(10px);
    }
    
    .download-btn {
        background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        border: none;
        cursor: pointer;
        font-size: 1.1rem;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
        transition: all 0.3s;
        animation: pulse 2s infinite;
    }
    
    .download-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(245, 87, 108, 0.6);
    }
    
    /* Ocultar elementos por defecto de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Header animado
st.markdown("""
<div class="main-header">
    <h1 style="font-size: 3.5rem; background: linear-gradient(45deg, #2196F3, #4CAF50); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        🚀 PDF Converter Yan
    </h1>
    <p style="font-size: 1.3rem; color: #666;">Conversión de imágenes con visualización en tiempo real</p>
</div>
""", unsafe_allow_html=True)

# Sidebar con estadísticas y configuración
with st.sidebar:
    st.markdown("### ⚙️ Configuración Avanzada")
    
    # Límite aumentado a 50MB por archivo
    max_file_size = st.number_input("Tamaño máx. por archivo (MB)", 1, 100, 50)
    max_files = st.number_input("Máximo de archivos", 1, 50, 20)
    
    quality = st.slider("Calidad PDF (DPI)", 50, 300, 150)
    compression = st.select_slider(
        "Nivel de compresión",
        options=["Mínima", "Baja", "Media", "Alta", "Máxima"],
        value="Media"
    )
    
    output_format = st.radio("Formato de salida", ["PDF único", "PDFs separados", "Ambos"])
    
    st.markdown("---")
    
    # Estadísticas en tiempo real
    if 'processed_files' not in st.session_state:
        st.session_state.processed_files = 0
        st.session_state.total_size = 0
    
    st.markdown("### 📊 Estadísticas")
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric("Archivos procesados", st.session_state.processed_files)
    with col_stat2:
        st.metric("MB procesados", f"{st.session_state.total_size:.1f}")

# Área principal con drag & drop visual
st.markdown("""
<div class="upload-zone">
    <h2>📁 Arrastra tus imágenes aquí</h2>
    <p style="color: #666;">o haz clic para seleccionar archivos</p>
    <p style="font-size: 0.9rem; color: #999;">Máximo {} archivos • Hasta {} MB cada uno</p>
</div>
""".format(max_files, max_file_size), unsafe_allow_html=True)

# Uploader con límites aumentados
uploaded_files = st.file_uploader(
    "", 
    type=['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'webp', 'gif', 'ico'],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

# Procesamiento
if uploaded_files:
    if len(uploaded_files) > max_files:
        st.error(f"❌ Demasiados archivos. Máximo permitido: {max_files}")
    else:
        # Validar tamaños
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
            # Dashboard de progreso visual
            st.markdown("### 📈 Progreso de Conversión")
            
            progress_cols = st.columns(3)
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
                est_time = len(valid_files) * 0.5
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                    <h3>~{est_time:.0f}s</h3>
                    <p>Tiempo estimado</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Barra de progreso animada
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Previsualización en grid
            st.markdown("### 👁️ Previsualización")
            preview_cols = st.columns(min(4, len(valid_files)))
            
            images_data = []
            
            for idx, (file, col) in enumerate(zip(valid_files, preview_cols * ((len(valid_files)//4)+1))):
                with col:
                    try:
                        image = Image.open(file)
                        
                        # Mostrar miniatura con efecto hover
                        st.image(image, caption=file.name, use_container_width=True)
                        
                        # Información de la imagen
                        info_col1, info_col2 = st.columns(2)
                        with info_col1:
                            st.caption(f"📐 {image.size[0]}x{image.size[1]}")
                        with info_col2:
                            st.caption(f"💾 {len(file.getvalue())/1024:.0f}KB")
                        
                        # Convertir a RGB si es necesario
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
                            'original': file
                        })
                        
                        # Actualizar progreso
                        progress = (idx + 1) / len(valid_files)
                        progress_bar.progress(int(progress * 100))
                        status_text.text(f"Procesando {idx + 1} de {len(valid_files)}...")
                        
                    except Exception as e:
                        st.error(f"Error con {file.name}: {str(e)}")
            
            progress_bar.empty()
            status_text.success("✅ ¡Todas las imágenes procesadas!")
            
            # Opciones de conversión
            st.markdown("### 🎯 Opciones de Salida")
            
            col_opt1, col_opt2, col_opt3 = st.columns(3)
            
            with col_opt1:
                page_size = st.selectbox("Tamaño de página", ["Original", "A4", "Carta", "Personalizado"])
            
            with col_opt2:
                orientation = st.radio("Orientación", ["Automática", "Vertical", "Horizontal"])
            
            with col_opt3:
                margin = st.slider("Margen (px)", 0, 50, 0)
            
            # Botón de conversión con efecto
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🚀 GENERAR PDF(S)", key="convert", use_container_width=True):
                with st.spinner("Generando documentos de alta calidad..."):
                    
                    # Simular procesamiento con animación
                    import time
                    
                    if output_format in ["PDF único", "Ambos"] and len(images_data) > 0:
                        # Crear PDF combinado
                        pdf_buffer = io.BytesIO()
                        
                        first_img = images_data[0]['image']
                        other_imgs = [d['image'] for d in images_data[1:]]
                        
                        # Aplicar calidad
                        quality_map = {
                            "Mínima": 30,
                            "Baja": 50,
                            "Media": 75,
                            "Alta": 90,
                            "Máxima": 95
                        }
                        
                        save_kwargs = {
                            'resolution': quality,
                            'save_all': True,
                            'append_images': other_imgs,
                            'quality': quality_map[compression]
                        }
                        
                        first_img.save(pdf_buffer, 'PDF', **save_kwargs)
                        pdf_buffer.seek(0)
                        
                        # Actualizar estadísticas
                        st.session_state.processed_files += len(images_data)
                        st.session_state.total_size += total_size
                        
                        # Mostrar éxito con animación
                        st.balloons()
                        
                        st.markdown("""
                        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white; margin: 1rem 0;">
                            <h2>🎉 ¡Conversión Exitosa!</h2>
                            <p>Tu PDF está listo para descargar</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Botón de descarga estilizado
                        st.download_button(
                            label=f"📥 Descargar PDF Único ({len(images_data)} páginas)",
                            data=pdf_buffer,
                            file_name=f"convertido_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    
                    # PDFs individuales
                    if output_format in ["PDFs separados", "Ambos"]:
                        st.markdown("### 📄 Archivos Individuales")
                        
                        individual_cols = st.columns(2)
                        for idx, data in enumerate(images_data):
                            with individual_cols[idx % 2]:
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
    <p>🚀 PDF Converter De Yan | Procesamiento masivo de imágenes</p>
    <p style="font-size: 0.8rem;">Soporta hasta 50 archivos simultáneos • Máximo 50MB por archivo</p>
</div>
""", unsafe_allow_html=True)