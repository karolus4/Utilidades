Utilidades

Utilidades para procesamiento gráfico y descarga de audio video Esta aplicacion fue desarrollada a partir del codigo que recogi del canal de youtube de "class toni_dev" donde explica a grandes rasgos el uso de las librerias utilizadas. He adicionado un modulo de conversion de archivos .heic a jpg, webp a jpg y trate de optimizar la aplicacion, la cual trabaja correctamente en entorno local. En Streamlit Cloud la opcion de descarga de videos de Youtube daba un error si la ejecutas desde el navegador de una PC, mas no desde una tablet o celular. EL mensaje de error era:

pytube.exceptions.VideoUnavailable: This app has encountered an error. The original error message is redacted to prevent data leaks. Full error details have been recorded in the logs (if you're on Streamlit Cloud, click on 'Manage app' in the lower right of your app). Traceback:

El error lo corregi indicandole a streamlit en los requirements.txt que la libreria pytube la obtenga de : @ git+https://github.com/nficano/pytube@a32fff39058a6f7e5e59ecd06a7467b71197ce35 Esta publicado en la direccion https://droid-util.streamlit.app/