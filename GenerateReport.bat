@echo off  

python "%~dp0src\spotify_data_processing.py"
python "%~dp0src\report_generator.py"
python "%~dp0src\extra_profiling_report.py"

pause