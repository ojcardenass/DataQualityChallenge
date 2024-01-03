import time
import sys
import locale
from datetime import datetime, timedelta
from pathlib import Path
import tkinter as tk
from tkinter.messagebox import showinfo
from io import StringIO, BytesIO

from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak, Image, Spacer, Table, TableStyle, KeepTogether)
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor, black, white, transparent
from reportlab.platypus.flowables import Flowable
from reportlab.lib.pagesizes import LETTER, inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from tqdm import tqdm
from colorama import just_fix_windows_console, Fore, Style

from data_quality_analysis import *
import utils_io
import missingno


just_fix_windows_console()

base = Path(__file__).parent.parent
# StringIO buffer to capture error prints
error_buffer = StringIO()

# Set the locale to English
locale.setlocale(locale.LC_ALL, 'en_EN.UTF-8')

# Class for the header and footer of the canvas
class FooterCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
        self.width, self.height = LETTER

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_canvas(page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_canvas(self, page_count):
        page = "Page %s of %s" % (self._pageNumber, page_count)
        x = 128

        self.saveState()

        self.setStrokeColorRGB(0, 0, 0)
        self.setLineWidth(0.5)
        self.line(66, 55, LETTER[0] - 66, 55)

        self.setFontSize(18)
        text = 'Dataset Profiling'
        self.setFillColor(black)
        self.drawString(60, 745, text)

        self.setFontSize(10)
        date = datetime.now().strftime('%A, %d %B %Y').replace(' 0', ' ')
        info = f" Generated on: {date}"
        self.setFillColor(black)
        self.drawString(60, 58, info)

        self.setStrokeColorRGB(0, 0, 0)
        self.setFillColor(black)
        self.drawString(LETTER[0] / 2.2, 45, page)
        self.restoreState()

# DataProfilingPDF class
class DataProfilingPDF():

    def __init__(self):
        self.dataset = utils_io.get_dataset('url')

        title = "data_quality_report"
        # Directory to save the generated report
        self.output_dir = base / 'output/doc/'
        self.path = str(self.output_dir / f"{title}.pdf")

        # Document properties and list of elements
        self.styleSheet = getSampleStyleSheet()
        self.elements = []
        self.width, self.height = LETTER

        def build_report():
            # Template on which the report will be generated
            self.doc = SimpleDocTemplate(self.path, pagesize=LETTER, leftMargin=0.7 * inch, title=title)
            self.doc.build(self.elements, canvasmaker=FooterCanvas)

        # Dictionary of processes, the order defines the position in which they will be presented in the report.
        # Important: build_report must always be at the end
        processes = {
            "Graph Overview Price Evolution": self.overview,
            "Create Report": build_report,
        }

        # Progress bar and script execution
        for key, process in tqdm(processes.items(), desc="Total Progress", position=0):
            tqdm.write(f"\rProcessing: {key} ...")
            process()

        # List of errors found
        error_buffer.seek(0)
        print(f"{Fore.RED}\nErrors:{Style.RESET_ALL}")
        print(f"{Fore.RED}{error_buffer.read()}{Style.RESET_ALL}")
        error_buffer.close()

    # Section
    def overview(self):
        data_o = overview(self.dataset)
        # Styles for the section title
        psHeaderText = ParagraphStyle('Hed0', fontSize=15, alignment=TA_LEFT, borderWidth=3, textColor=black)
        text = 'Overview'
        # Flowable element for the title
        paragraphReportHeader = Paragraph(text, psHeaderText)

        # Space between the title and the image
        spacer = Spacer(10, 10)

        # Generate the table with the stat data
        stat_data = [
            ["Dataset statistics", ""],
            ["", ""],
            ["Number of variables", data_o['cols']],
            ["Number of observations", data_o['rows']],
            ["Total data", data_o['all']],
            ["Missing cells", data_o['total_missing_values']],
            ["Missing cells (%)", f"{data_o['total_missing_values_percentage']:.2f}"],
            ["Duplicate rows", data_o['duplicate_rows']],
            ["Duplicate rows (%)", f"{data_o['duplicate_rows_percentage']:.2f}"],
        ]

        var_type = [
            ["Variable types", ""],
            ["", ""],
            ["Numeric", data_o['numerics']],
            ["Text", data_o['strings']],
            ["Date Time", data_o['date_time']],
        ]

        col_widths = 200
        row_height = 0.4*inch

        std_row_height = utils_io.multiple_row_height(row_height,stat_data)
        var_row_height = utils_io.multiple_row_height(row_height,var_type)
        
        # Standard table style format
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 1), transparent),                 # Color de fondo blanco para las fila 1
            # ('BACKGROUND', (0, 1), (-1, 1), HexColor(0xCCCCCC)),    # Color de fondo gris para la fila 2
            ('TEXTCOLOR', (0, 0), (-1, -1), black),                 # Color de texto para todas las celdas
            ('FONTSIZE', (0, 0), (-1, 1), 14),                      # Tamaño de fuente primera fila
            ('FONTSIZE', (0, 1), (-1, -1), 8.2),                      # Tamaño de fuente demas fila
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),                    # Alinear todo a la izquierda
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),                     # Alinear a la derecha la segunda columna de la primera fila
            ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),                   # Alinear a la derecha la tercera columna
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),                 # Alinear verticalmente los datos
            ('RIGHTPADDING', (1, 0), (1, 0), -240),                 # Padding negativo para la segunda columna de la primera fila
            # ('GRID', (0, 0), (-1, -1), 0.5, black)                  # Bordes de la tabla'
        ])

        stat_table = Table(stat_data, colWidths=col_widths, rowHeights=std_row_height, hAlign="LEFT")
        stat_table.setStyle(table_style)

        var_table = Table(var_type, colWidths=col_widths, rowHeights=var_row_height, hAlign="LEFT")
        var_table.setStyle(table_style)

        # New table that contains the last 2 tables
        data= [(stat_table, var_table)]
        table = Table(data, [250, 250])
        table.setStyle(TableStyle([
            ('VALIGN',(0,0),(-1,-1),'TOP'),
        ]))

        spacer = Spacer(10, 10)

        # Styles for the section title
        psHeaderText1 = ParagraphStyle('Hed1', fontSize=15, alignment=TA_LEFT, borderWidth=3, textColor=black)
        text1 = 'Nullity Matrix'
        # Flowable element for the title
        paragraphReportHeader1 = Paragraph(text1, psHeaderText1)

        spacer1 = Spacer(10, 6)

        # Read the CSV file using the selected method
        df = utils_io.get_dataset('url')

        # Generate the nullity matrix
        fig = missingno.matrix(df)
        fig_copy = fig.get_figure()

        # Save the image as a stream of in-memory bytes
        imgdata = BytesIO()
        fig_copy.savefig(imgdata, format='png', bbox_inches='tight')
        imgdata.seek(0)  # rewind the data

        # Read the image of the graph and set the size it will be saved in
        img = Image(imgdata)
        img.drawHeight = 4 * inch
        img.drawWidth = 7.5 * inch

        # Group all the elements of this section
        block = KeepTogether([paragraphReportHeader, spacer, table, spacer, paragraphReportHeader1, spacer1, img])
        self.elements.append(block)

        spacer = Spacer(10, 20)
        self.elements.append(spacer)


if __name__ == '__main__':
    try:
        start = time.time()
        report = DataProfilingPDF()
        end = time.time()
        exc_time = end - start

    except ValueError as ve:
        print(f"Error: {ve}")
        sys.exit(1)
