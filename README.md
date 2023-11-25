# Utilidades
Utilidades para procesamiento gráfico y descarga de audio video
Esta aplicacion fue desarrollada a partir del codigo que recogi del canal de youtube de "class toni_dev" donde explica a grandes
rasgos el uso de las librerias utilizadas. He adicionado un modulo de conversion de archivos .heic a jpg y trate de optimizar la 
aplicacion, la cual trabaja correctamente en entorno local. En Streamlit Cloud la opcion de descarga de videos de Youtube daba
un error si la ejecutas desde el navegador de una PC, mas no desde una tablet o celular. EL mensaje de error era:

pytube.exceptions.VideoUnavailable: This app has encountered an error. The original error message is redacted to prevent data leaks.
Full error details have been recorded in the logs (if you're on Streamlit Cloud, click on 'Manage app' in the lower right of your app). Traceback:

No pude encontrar que ocasiona este error en Streamlit Cloud, lo raro era que si la ejecutabas desde el codespace del mismo streamlit no daba error.
He cambiado la libreria pytube desde direcciones alternativas (ver archivo requirements.txt) y tampoco lo soluciono la primera vez. 
Volvi a crear el repositorio, lo sincronice, y luego lo envie a streamlit Cloud; y ahora si todo trabaja bien.
