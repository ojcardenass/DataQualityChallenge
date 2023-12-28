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
└── .gitignore
```

**src/: Contiene los scripts de código fuente.**
- spotify_data_processing.py: Script en Python que procesa el archivo JSON descargado de la API de Spotify y lo convierte al formato solicitado (dataset.csv).
- data_quality_analysis.py: Script en Python que realiza el análisis de calidad de datos sobre el conjunto de datos resultante.

**input/: Contiene los archivos que seran analizados.**
- taylor_swift_spotify.json: El archivo JSON descargado de la API de Spotify.

**output/: Contiene los archivos resultantes de los scripts.**
- **doc/: Contiene documentos y reportes.**
  - data_quality_report.pdf: Documento que presenta los resultados del análisis de calidad de datos, identificando las anomalías encontradas y proporcionando justificaciones.
- dataset.csv: El conjunto de datos procesado generado por *spotify_data_processing.py*.

**res/: Reservado para recursos adicionales como archivos multimedia o cualquier otro material necesario para explicar el proceso y los resultados.**

**README.md:** Instrucciones detalladas sobre cómo ejecutar el código en cada parte del desafío, así como una descripción de la estructura del repositorio y cómo interpretar los resultados.

**.gitignore:** Archivo que especifica los archivos y directorios que deben ser ignorados por el control de versiones Git.

## Instrucciones de Uso
### Parte 1: Procesamiento del Archivo JSON
- Ejecute src/spotify_data_processing.py proporcionando el archivo JSON dep/taylor_swift_spotify.json.
- El script generará el archivo dep/dataset.csv con el formato solicitado.

### Parte 2: Análisis de Calidad de Datos
- Luego de ejecutar *src/spotify_data_processing.py*. Ejecute src/data_quality_analysis.py.
- Consulte el archivo doc/data_quality_report.pdf para obtener detalles sobre las anomalías identificadas.

## Notas Importantes
- Asegúrese de tener instaladas las bibliotecas necesarias antes de ejecutar los scripts (Pandas y JSON).
- Consulte el README.md para obtener orientación adicional sobre el repositorio y su uso.
