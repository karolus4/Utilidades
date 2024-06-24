import io
import os
import cv2
from shutil import rmtree
import streamlit as st 
from streamlit_option_menu import option_menu
from PIL import Image
from rembg import remove
from pytube import YouTube
import pillow_heif

# Funciones ####################################################

def quitar_background(image_upload):
    # pasando imagen a bytes
    image = Image.open(image_upload)
    image.save(ruta_completa)
    image_byte=io.BytesIO() # le indico que la varible se escribira en buffer de memoria
    image.save(image_byte, format="PNG")
    # Eliminando Fondo
    image_byte.seek(0)
    image_bytes_proccesed=remove(image_byte.read())
    imagen_procesada=Image.open(io.BytesIO(image_bytes_proccesed))
    return imagen_procesada

def foto_a_dibujo(archivo):
    imagen = cv2.imread(archivo)
    if imagen is not None:
        img_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        color_invertido = cv2.bitwise_not(img_gris)

        desenfoque=cv2.GaussianBlur(color_invertido, (21,21), 0)
        desenfoque_invertido = cv2.bitwise_not(desenfoque)
        dibujo = cv2.divide(img_gris, desenfoque_invertido, scale=256.0)
        return dibujo
    else:
        st.write('No se pudo cargar la imagen.')
        return None

def convertir_heic_jpg(ruta):
    try:
        print(ruta)
        heif_file = pillow_heif.read_heif(ruta)
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
        )
        ruta_temporal=os.path.join(SUBCARPETA_TEMPORAL,nuevo_nombre)
        jpeg_image = image.convert('RGB')
        nueva_imagen = jpeg_image.save(ruta_temporal, format="JPEG")
        st.image(ruta_temporal, caption='Imagen procesada', use_column_width=True)
        st.write('Conversion realizada...')  
        with open(ruta_temporal, 'rb') as f:
            image_data=f.read()
        st.download_button("Descargar imagen JPG", data=image_data, file_name=nuevo_nombre)
        rmtree("temporales")
        return None

    except Exception as e:
        print("Error converting the image:", str(e))
        return None

def convertir_webp_jpg(ruta):
    try:
        ruta_temporal=os.path.join(SUBCARPETA_TEMPORAL,nuevo_nombre)
        jpeg_image = Image.open(ruta)
        nueva_imagen = jpeg_image.save(ruta_temporal, format="JPEG")
        st.image(ruta_temporal, caption='Imagen procesada', use_column_width=True)
        st.write('Conversion realizada...')  
        with open(ruta_temporal, 'rb') as f:
            image_data=f.read()
        st.download_button("Descargar imagen JPG", data=image_data, file_name=nuevo_nombre)
        rmtree("temporales")
        return None

    except Exception as e:
        print("Error converting the image:", str(e))
        return None

def descarga_youtube(url, tipo):
    yt = YouTube(url)
    # Muestra información sobre el video
    st.write(f"**Título del video:** {yt.title}")
    st.write(f"**Duración:** {yt.length} segundos")

    # selecciona entre audio o video
    if tipo=='A':
        st.write('Extrayendo audio...')
        datos = yt.streams.filter(only_audio=True).first()
        extension = '.mp3'
        formato = 'audio/mpeg'                
    else:
        st.write('Extrayendo video...')          
        datos = yt.streams.filter(file_extension='mp4').get_highest_resolution()
        extension = '.mp4'
        formato = 'video/mp4'

    datos_file=datos.download(output_path='descargas')
    base, ext = os.path.splitext(datos_file)
    new_file=base+extension
    new_name=yt.title+extension    

    st.write('Proceso completado')        
    os.rename(datos_file, new_file)
    with open(new_file, "rb") as f:
        data1 = f.read()
    st.download_button("Descargar archivo", data=data1, file_name=new_name, mime=formato)

    rmtree("descargas")
    return None

####################################################################
# Frontend
####################################################################
st.set_page_config(page_title='DROID - Utilidades', layout='centered')
st.title('UTILIDADES DROID')
st.write('###')

# Menu
selected = option_menu(
    menu_title=None,
    options=["Home", "Quitar Fondo", "Foto a Dibujo", "HEIC a JPG", "WEBP a JPG", "Descargar Video Youtube"],
    icons=["house", "bi-eye-slash", "camera", "caret-right-square-fill", "camera"],
    orientation="horizontal"
)

if selected == "Home":
    with st.container(): 
        left_column, right_column= st.columns(2)
        with left_column:
            st.image('images/droid.png')
        with right_column:
            st.subheader('Utilidades Web Gratuitas')
            st.write(
                """Bienvenido a la seccion de utilidades de la empresa
                Droid S.A.C. Aqui ponemos a disposicion del publico una
                serie de aplicaciones que le permitiran el manejo rapido
                de funciones graficas y de video solo para usos legales.
                Agradecemos su visita.
                """
            )
            
if selected == "Quitar Fondo":
    with st.container(): 
        left_column, right_column= st.columns(2)
        with left_column:
            st.image('images/killbackground.png')
        with right_column:
            st.subheader('Quitar Fondo de Imagen')
            st.write(
                """Usamos la funcion remove de la libreria rembg
                para la eliminacion automatica del fondo de la 
                imagen
                """
            )
    imagen_subida = st.file_uploader('Subir imagen a procesar ...', type=['jpg', 'jpeg', 'png'])
    if imagen_subida is not None:
        # Carpeta temporal en el proyecto
        SUBCARPETA_TEMPORAL = 'temporales'
        if not os.path.exists(SUBCARPETA_TEMPORAL):
            os.mkdir(SUBCARPETA_TEMPORAL)
        
        st.image(imagen_subida, caption='Imagen Subida', use_column_width=True)
        ruta_completa = os.path.join(SUBCARPETA_TEMPORAL, imagen_subida.name) # Capturando ruta completa
        #****************************
        remove_button = st.button(label='Quitar Fondo')
        if remove_button:
            imagen_procesada=quitar_background(imagen_subida)
            st.image(imagen_procesada, caption='Fondo Removido', use_column_width=True)
            ruta_completa = os.path.join(SUBCARPETA_TEMPORAL,"imagen_procesada.png") 
            imagen_procesada.save(ruta_completa)
            with open(ruta_completa, 'rb') as f:
                image_data=f.read()
            st.download_button("Descargar imagen procesada", data=image_data, file_name='imagen_procesada.png')
            rmtree("temporales")
        
if selected == "Foto a Dibujo":
    with st.container(): 
        left_column, right_column= st.columns(2)
        with left_column:
            st.image('images/fotototrace.jpg')
        with right_column:
            st.header('Filtro de Fotografia a dibujo a Lapiz')
            st.write(
                """Usamos la libreria opencv de python para la
                conversion de la imagen a trazos.
                """                
            )
    imagen_subida = st.file_uploader('Subir imagen a procesar ...', type=['jpg', 'jpeg', 'png'])

    if imagen_subida is not None:
        nombre_del_archivo=imagen_subida.name
        # Carpeta temporal en el proyecto
        SUBCARPETA_TEMPORAL = 'temporales'
        if not os.path.exists(SUBCARPETA_TEMPORAL):
            os.mkdir(SUBCARPETA_TEMPORAL)
        ruta_completa = os.path.join(SUBCARPETA_TEMPORAL, nombre_del_archivo)    
        with open(ruta_completa, "wb") as f:
            f.write(imagen_subida.read())    

        st.image(imagen_subida, caption='Imagen Subida', use_column_width=True)
        dibujo_button = st.button(label='Convertir a Dibujo')
        if dibujo_button:
            imagen_procesada=foto_a_dibujo(ruta_completa)
            st.image(imagen_procesada, caption='Foto a Dibujo', use_column_width=True)
            ruta_completa = os.path.join(SUBCARPETA_TEMPORAL,"foto_a_dibujo.png") 
            cv2.imwrite(ruta_completa, imagen_procesada)
            with open(ruta_completa, 'rb') as f:
                image_data=f.read()
            st.download_button("Descargar imagen procesada", data=image_data, file_name="foto_a_dibujo.png")
            rmtree("temporales")

if selected == "HEIC a JPG":
    with st.container(): 
        left_column, right_column= st.columns(2)
        with left_column:
            st.image('images/heictojpg.jpg')
        with right_column:
            st.header('Conversor de imagenes formato .heic a .jpg')
            st.write(
                """Proceso de recodificacion de archivo pasando del formato
                propietario usado en sistemas apple al formato universal jpg.
                """                
            )
    imagen_subida = st.file_uploader('Subir imagen a procesar ...', type=['HEIC', 'heic'])

    if imagen_subida is not None:
        nombre_del_archivo=imagen_subida.name
        nuevo_nombre=os.path.splitext(nombre_del_archivo)[0] + ".jpg"
        # Carpeta temporal en el proyecto
        SUBCARPETA_TEMPORAL = 'temporales'
        if not os.path.exists(SUBCARPETA_TEMPORAL):
            os.mkdir(SUBCARPETA_TEMPORAL)

        ruta_completa = os.path.join(SUBCARPETA_TEMPORAL, nombre_del_archivo)
        
        with open(ruta_completa, "wb") as f:
            f.write(imagen_subida.read())    
        dibujo_button = st.button(label='Convertir a JPG')

        if dibujo_button:
            convertir_heic_jpg(ruta_completa)      

if selected == "WEBP a JPG":
    with st.container(): 
        left_column, right_column= st.columns(2)
        with left_column:
            st.image('images/webptojpg.jpg')
        with right_column:
            st.header('Conversor de imagenes formato .webp a .jpg')
            st.write(
                """Proceso de conversion del formato de archivo webp usado en 
                internet al formato universal jpg.
                """                
            )
    imagen_subida = st.file_uploader('Subir imagen a procesar ...', type=['WEBP', 'webp'])

    if imagen_subida is not None:
        nombre_del_archivo=imagen_subida.name
        nuevo_nombre=os.path.splitext(nombre_del_archivo)[0] + ".jpg"
        # Carpeta temporal en el proyecto
        SUBCARPETA_TEMPORAL = 'temporales'
        if not os.path.exists(SUBCARPETA_TEMPORAL):
            os.mkdir(SUBCARPETA_TEMPORAL)

        ruta_completa = os.path.join(SUBCARPETA_TEMPORAL, nombre_del_archivo)
        ruta_temporal = os.path.join(SUBCARPETA_TEMPORAL, nuevo_nombre)
        
        with open(ruta_completa, "wb") as f:
            f.write(imagen_subida.read())    

        dibujo_button = st.button(label='Convertir a JPG')

        if dibujo_button:
            convertir_webp_jpg(ruta_completa)  
         
            
if selected=="Descargar Video Youtube":
    with st.container(): 
        left_column, right_column= st.columns((1,2))
        with left_column:
            st.image('images/youtube.jpg')
        with right_column:
            st.header('Descargar Video de Youtube')
            st.write(
                """A traves de esta aplicacion podemos descargar
                audio y videos en alta resolucion desde Youtube.
                Debes ingresar la direccion URL, escoger el tipo de archivo de descarga
                y despues de procesar podras descargarlo. 
                """                
            )
    with st.container():
        url_path = st.text_input('Ingresar direccion URL del Video de Youtube', value='')
        left_column, right_column= st.columns((1,2))
        with left_column:
            type = st.radio("¿Que desea Extraer?", ["Audio", "Video 720p"])        
            descarga_button = st.button(label='Procesar archivo')                      
        with right_column:                 
            if descarga_button:
                if type == 'Audio':
                    file_path = descarga_youtube(url_path, 'A')                   
                elif type == 'Video 720p':
                    file_path = descarga_youtube(url_path, 'V') 