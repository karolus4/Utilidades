# Utilidades
Utilidades para procesamiento gráfico y descarga de audio video
Esta aplicacion fue desarrollada a partir del codigo que recogi del canal de youtube de "class toni_dev" donde explica a grandes
rasgos el uso de las librerias utilizadas. He adicionado un modulo de conversion de archivos .heic a jpg y trate de optimizar la 
aplicacion, la cual trabaja correctamente en entorno local. En Streamlit Cloud solo la opcion de descarga de videos de Youtube da
un error si la ejecutas desde el navegador de una PC. EL mensaje de error es:

pytube.exceptions.VideoUnavailable: This app has encountered an error. The original error message is redacted to prevent data leaks.
Full error details have been recorded in the logs (if you're on Streamlit Cloud, click on 'Manage app' in the lower right of your app). Traceback:

File "/home/adminuser/venv/lib/python3.9/site-packages/streamlit/runtime/scriptrunner/script_runner.py", 
line 534, in _run_script exec(code, module.dict) File "/mount/src/utilidades/app.py", line 195, 
in file_path = descarga_youtube(url_path, 'A') File "/mount/src/utilidades/app.py", line 45, 
in descarga_youtube datos = yt.streams.filter(only_audio=True).first() 
File "/home/adminuser/venv/lib/python3.9/site-packages/pytube/main.py", 
line 295, in streams self.check_availability() File "/home/adminuser/venv/lib/python3.9/site-packages/pytube/main.py",
line 222, in check_availability raise exceptions.VideoUnavailable(video_id=self.video_id)

No he podido encontrar que ocasiona este error en Streamlit Cloud, lo raro es que si ejecutas desde el codespace del mismo streamlit funciona,
tambien funciona bien ejecutandola desde un navegador de dispositivo movil. He cambiado la libreria pytube desde direcciones alternativas y 
tampoco resuelve el problema.
