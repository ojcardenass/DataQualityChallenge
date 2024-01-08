from io import StringIO, BytesIO
from pathlib import Path

import utils_io
import pandas as pd
from ydata_profiling import ProfileReport



base = Path(__file__).parent.parent
       
# Directory to save the generated report
output_dir = base / 'output/doc/'

# Read the CSV file using the selected method
df = utils_io.get_dataset('url')

# Perform data analysis using ydata_profiling library
profile = ProfileReport(df, title="Profiling Report", correlations={"auto": {"calculate": False}}, missing_diagrams={"Heatmap": False})

profile.to_file(output_dir / "profilling_report.html")

try:
    bucket = 'dataqualitychallenge'
    utils_io.upload_file(output_dir / "profilling_report.html", bucket, 'profilling_report.html')
except Exception as e:
    print("Error uploading dataset to S3: ", e)