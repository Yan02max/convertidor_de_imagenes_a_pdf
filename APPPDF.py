import streamlit as st
from PIL import Image
import io
import os

st.set_page_config(page_title="Imagen a PDF", page_icon="📄")

st.title("🖼️ Convertidor de Imagen a PDF De Yan")
st.write("Sube una o varias imágenes y conviértelas a PDF")

# Subir archivos
uploaded_files = st.file_uploader(
    "Selecciona imágenes", 
    type=['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'webp'],
    accept_multiple_files=True
)

if uploaded_files:
    st.write(f"📁 {len(uploaded_files)} archivo(s) seleccionado(s)")
    
    # Opciones
    col1, col2 = st.columns(2)
    with col1:
        quality = st.slider("Calidad del PDF", 1, 100, 95)
    with col2:
        if len(uploaded_files) > 1:
            combine = st.checkbox("Combinar en un solo PDF", value=True)
        else:
            combine = True
    
    if st.button("🚀 Convertir a PDF", type="primary"):
        images = []
        
        # Procesar cada imagen
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            
            # Convertir a RGB si es necesario (para PNG con transparencia)
            if image.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')
            
            images.append(image)
        
        # Generar PDF
        if combine and len(images) > 1:
            # Todas las imágenes en un PDF
            first_image = images[0]
            other_images = images[1:]
            
            pdf_buffer = io.BytesIO()
            first_image.save(
                pdf_buffer, 
                'PDF', 
                resolution=100.0, 
                save_all=True, 
                append_images=other_images,
                quality=quality
            )
            pdf_buffer.seek(0)
            
            st.success("✅ ¡PDF generado con éxito!")
            st.download_button(
                label="📥 Descargar PDF combinado",
                data=pdf_buffer,
                file_name="imagenes_combinadas.pdf",
                mime="application/pdf"
            )
            
        else:
            # PDFs separados
            for i, (img, file) in enumerate(zip(images, uploaded_files)):
                pdf_buffer = io.BytesIO()
                img.save(pdf_buffer, 'PDF', resolution=100.0, quality=quality)
                pdf_buffer.seek(0)
                
                original_name = os.path.splitext(file.name)[0]
                
                st.download_button(
                    label=f"📥 Descargar {original_name}.pdf",
                    data=pdf_buffer,
                    file_name=f"{original_name}.pdf",
                    mime="application/pdf",
                    key=f"pdf_{i}"
                )

# Información adicional
st.divider()
st.info("""
**Formatos soportados:** PNG, JPG, JPEG, BMP, TIFF, WEBP

**Características:**
- Conversión de múltiples imágenes
- Combinación opcional en un solo PDF
- Mantiene la calidad original
- Soporte para imágenes con transparencia
""")