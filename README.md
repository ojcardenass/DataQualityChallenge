# Repositorio: Spotify Data Quality Engineer Challenge

Este repositorio contiene la solución a un desafío técnico que implica el procesamiento de datos provenientes de la API de Spotify y la realización de un análisis de calidad de datos sobre el conjunto resultante. El repositorio está organizado de la siguiente manera:

## Estructura del Repositorio
```bash
├── src
│   ├── spotify_data_processing.py
│   └── data_quality_analysis.py
├── input
│   └── taylor_swift_spotify.json
├── output
│   ├── doc
│   │   └── data_quality_report.pdf
│   └── dataset.csv
├── res
├── README.md
├── requirements.txt
└── .gitignore
```

**src/: Contiene los scripts de código fuente.**
- spotify_data_processing.py: Script en Python que procesa el archivo JSON descargado de la API de Spotify y lo convierte al formato solicitado (dataset.csv).
- data_quality_analysis.py: Script en Python que realiza el análisis de calidad de datos sobre el conjunto de datos resultante.
- report_generator.py: Script en Python que genera un informe de calidad de datos basado en los tests y comentarios definidos en data_quality_analysis.py.
- utils_io.py: Este módulo provee funciones utilitarias para las operaciones de input/output
- extra_profiling_report.py: Script en Python que genera un informe adicional de perfilado de datos, proporcionando estadísticas y visualizaciones sobre el conjunto de datos procesado.

**input/: Contiene los archivos que seran analizados.**
- input.txt: Este archivo contiene el enlace donde se encuentra almacenado el archivo JSON descargado de la API de Spotify.

**output/: Contiene los archivos resultantes de los scripts.**
- **doc/: Contiene documentos y reportes.**
  - data_quality_report.pdf: Documento que presenta los resultados del análisis de calidad de datos, identificando las anomalías encontradas y proporcionando justificaciones.
  - profilling_report.html (opcional): Este archivo contiene un informe adicional de perfilado de datos, que proporciona estadísticas y visualizaciones detalladas sobre el conjunto de datos procesado. Puede ser generado ejecutando el script extra_profiling_report.py.
- dataset.csv: El conjunto de datos procesado generado por *spotify_data_processing.py*.

**GenerateReport.bat:** Archivo por lotes que simplifica la ejecución de las operaciones necesarias para el desafío. Este archivo ejecuta los scripts en el orden correcto y además genera un análisis descriptivo adicional.

Para utilizar GenerateReport.bat, siga los siguientes pasos:
1. Asegúrese de tener instaladas las bibliotecas necesarias mencionadas en requirements.txt.
2. Abra una ventana de comandos en la ubicación del archivo GenerateReport.bat.
3. Ejecute el archivo GenerateReport.bat.
4. El archivo ejecutará los siguientes scripts en orden:
  - src/spotify_data_processing.py
  - src/report_generator.py
  - extra_profiling_report.py (opcional)
5. Consulte los archivos de salida generados en la carpeta output/ para obtener los resultados.

**README.md:** Instrucciones detalladas sobre cómo ejecutar el código en cada parte del desafío, así como una descripción de la estructura del repositorio y cómo interpretar los resultados.

**.gitignore:** Archivo que especifica los archivos y directorios que deben ser ignorados por el control de versiones Git.

## Instrucciones de Uso
### Parte 1: Procesamiento del Archivo JSON
- Ejecute src/spotify_data_processing.py proporcionando el archivo JSON input/taylor_swift_spotify.json.
- El script generará el archivo output/dataset.csv.

### Parte 2: Análisis de Calidad de Datos
- Luego de ejecutar *src/spotify_data_processing.py*. Ejecute src/report_generator.py. Este consultará los test y comentarios definidos en *src/data_quality_analysis.py*
- Consulte el archivo output/doc/data_quality_report.pdf para obtener detalles sobre las anomalías identificadas.

### Opcional:
- Se proporciona un archivo por lotes (archivo GenerateReport.bat) para simplificar la ejecución de las operaciones. Este archivo ejecuta los scripts en el orden correcto y además genera un análisis descriptivo adicional.

### Links S3:
- dataset.csv: https://dataqualitychallenge.s3.us-east-2.amazonaws.com/dataset.csv
- data_quality_report.pdf: https://dataqualitychallenge.s3.us-east-2.amazonaws.com/data_quality_report.pdf
- profilling_report.html (opcional): https://dataqualitychallenge.s3.us-east-2.amazonaws.com/profilling_report.html

## Notas Importantes
- Idealmente, los repositorios no deben contener datos de producción, pero en este desafío se incluyen con fines de demostración.
- Hay dos versiones de salida de los datos: una local y otra en la nube de AWS (S3). Puede encontrar el enlace de la versión en la nube en el archivo README.md.
- Asegúrese de tener instaladas las bibliotecas necesarias antes de ejecutar los scripts (Pandas y JSON). Ver requirements.txt
- Consulte el README.md para obtener orientación adicional sobre el repositorio y su uso.

