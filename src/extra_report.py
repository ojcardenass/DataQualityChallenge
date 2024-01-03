import utils_io
import pandas as pd
from ydata_profiling import ProfileReport

# Read the CSV file using the selected method
df = utils_io.get_dataset('url')

# Perform data analysis using ydata_profiling library
profile = ProfileReport(df, title="Profiling Report", correlations={"auto": {"calculate": False}}, missing_diagrams={"Heatmap": False})

profile.to_file("Extra_Report.html")