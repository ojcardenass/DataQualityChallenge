import time
import sys
import locale
from datetime import datetime, timedelta
from pathlib import Path
import tkinter as tk
from tkinter.messagebox import showinfo
from io import StringIO, BytesIO

from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak, Image, Spacer, Table, TableStyle, KeepTogether)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
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
            # self.draw_canvas(page_count)
            if (self._pageNumber > 2):
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

        self.setFontSize(9)
        text = 'Dataset Quality Report'
        self.setFillColor(black)
        self.drawString(60, 745, text)

        self.setFontSize(9)
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
        # Read the CSV file using the selected method
        self.dataset = utils_io.get_dataset('url')

        title = "data_quality_report"
        # Directory to save the generated report
        self.output_dir = base / 'output/doc/'
        self.path = str(self.output_dir / f"{title}.pdf")

        # Document properties and list of elements
        self.styleSheet = getSampleStyleSheet()
        self.justify_text = ParagraphStyle('BodyText', parent=self.styleSheet['BodyText'], alignment=TA_JUSTIFY)
        self.elements = []
        self.width, self.height = LETTER

         # Standard plot size
        self.plot_width = 1.7 * inch
        self.plot_height = 1.7 * inch

        self.anomalies = anomalies_data(self.dataset)
             
        def build_report():
            # Template on which the report will be generated
            self.doc = SimpleDocTemplate(self.path, pagesize=LETTER, leftMargin=0.7 * inch, title=title)
            self.doc.build(self.elements, canvasmaker=FooterCanvas)

        # Dictionary of processes, the order defines the position in which they will be presented in the report.
        # Important: build_report must always be at the end
        processes = {
            "First Page": self.firstPage,
            "Table of contents": self.secondPage,
            "Sources Report": self.sources,
            "Regards": self.regards,
            "Data Overview ": self.overview,
            "Scores": self.scores,
            "Unique Value Analysis": self.graph_overview,
            "Nullity Matrix": self.nullity,
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


    # Portada
    def firstPage(self):
        spacer = Spacer(30, 100)
        self.elements.append(spacer)

        psHeaderText = ParagraphStyle('Hed0', fontSize=22, alignment=TA_CENTER, borderWidth=3, textColor=black)
        text = 'Informe Calidad de Datos'
        # Flowable element for the title
        paragraphReportHeader = Paragraph(text, psHeaderText)
        self.elements.append(paragraphReportHeader)

        spacer = Spacer(30, 450)
        self.elements.append(spacer)

        psDetalle = ParagraphStyle('Resumen', fontSize=12, leading=14, justifyBreaks=1, alignment=TA_CENTER, justifyLastLine=1)
        text = f"""
        Grupo R5<br/>
        """
        paragraphReportSummary = Paragraph(text, psDetalle)
        self.elements.append(paragraphReportSummary)

        self.elements.append(PageBreak())

    def secondPage(self):

        psHeaderText = ParagraphStyle('Hed0', fontSize=22, alignment=TA_CENTER, borderWidth=3, textColor=black)
        text = 'Reporte de anomalías'
        paragraphReportHeader = Paragraph(text, psHeaderText)
        self.elements.append(paragraphReportHeader)


        spacer = Spacer(30, 250)
        self.elements.append(spacer)

        psHeaderText = ParagraphStyle('Hed0', fontSize=15, leftIndent=50, leading=20, alignment=TA_LEFT, borderWidth=3, textColor=black)
        text = '1. Fuente de datos'
        paragraphReportHeader = Paragraph(text, psHeaderText)
        self.elements.append(paragraphReportHeader)

        spacer = Spacer(10, 2)
        self.elements.append(spacer)

        psHeaderText = ParagraphStyle('Hed0', fontSize=15, leftIndent=50, leading=20, alignment=TA_LEFT, borderWidth=3, textColor=black)
        text = '2. Consideraciones de anomalías'
        paragraphReportHeader = Paragraph(text, psHeaderText)
        self.elements.append(paragraphReportHeader)


        psHeaderText = ParagraphStyle('Hed0', fontSize=15, leftIndent=50, leading=20, alignment=TA_LEFT, borderWidth=3, textColor=black)
        text = '3. Estadísticas (Métricas)'
        paragraphReportHeader = Paragraph(text, psHeaderText)
        self.elements.append(paragraphReportHeader)        
        
        spacer = Spacer(10, 2)
        self.elements.append(spacer)

        psHeaderText = ParagraphStyle('Hed0', fontSize=15, leftIndent=50, leading=20, alignment=TA_LEFT, borderWidth=3, textColor=black)
        text = '4. Ejemplos de anomalías'
        paragraphReportHeader = Paragraph(text, psHeaderText)
        self.elements.append(paragraphReportHeader)

        self.elements.append(PageBreak())

    def sources(self):

        psHeaderText = ParagraphStyle('Hed0', fontSize=19, alignment=TA_CENTER, borderWidth=3, textColor=black)
        text = '1. Fuente de datos'
        paragraphReportHeader = Paragraph(text, psHeaderText)
        self.elements.append(paragraphReportHeader)

        spacer = Spacer(30, 50)
        self.elements.append(spacer)

        data = sources_report()
        source = data['source']
        description = data['description']
        definition = data['definition']

        paragraphReport = Paragraph(source, self.styleSheet['Definition'])
        self.elements.append(paragraphReport)

        spacer = Spacer(30, 4)
        self.elements.append(spacer)

        paragraphReport = Paragraph(description, self.justify_text)
        self.elements.append(paragraphReport)

        spacer = Spacer(30, 4)
        self.elements.append(spacer)

        paragraphReport = Paragraph(definition, self.justify_text)
        self.elements.append(paragraphReport)

        self.elements.append(PageBreak())

    def regards(self):

        psHeaderText = ParagraphStyle('Hed0', fontSize=19, alignment=TA_CENTER, borderWidth=3, textColor=black)
        text = '2. Consideraciones de Anomalías'
        paragraphReportHeader = Paragraph(text, psHeaderText)
        self.elements.append(paragraphReportHeader)

        spacer = Spacer(30, 50)
        self.elements.append(spacer)

        anomalies_list = regards_data()

        style = self.styleSheet["Definition"]

        # Create a list of Paragraphs with enumeration
        paragraphs = [Paragraph(f"2.{i + 1:02d} {anomaly}", style) for i, anomaly in enumerate(anomalies_list)]
        self.elements.extend(paragraphs)

        self.elements.append(PageBreak())


    # Section
    def overview(self):
        data_o = overview(self.dataset)
        # Styles for the section title
        psHeaderText = ParagraphStyle('Hed0', fontSize=19, alignment=TA_CENTER, borderWidth=3, textColor=black)
        text = '3. Estadistícas (Métricas)'
        paragraphReportHeader = Paragraph(text, psHeaderText)

        spacer = Spacer(10, 15)

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
        data = [(stat_table, var_table)]
        table = Table(data, [250, 250])
        table.setStyle(TableStyle([
            ('VALIGN',(0,0),(-1,-1),'TOP'),
        ]))

        data_o = overview(self.dataset)
        stats = analysis_stats(self.dataset)

        anomalies = stats['analyzed']
        notAnaliz = stats['notAnalyzed']
        good_data = stats['good']

        data = [good_data, notAnaliz, anomalies]
        labels = ["Datos buenos", "Datos no analizados", "Datos anomalías"]

        imgdata = utils_io.pie_plot(data=data, title="Resumen de análisis", labels=labels)

        # Read the image of the graph and set the size it will be saved in
        img_data = Image(imgdata, width=2.5 * inch, height=2.5 * inch)

        data1 = [value for key, value in self.anomalies.items() if value > 0 and key != 'Total']
        labels1 = [key for key, value in self.anomalies.items() if value > 0 and key != 'Total']

        imgdata1 = utils_io.pie_plot(data=data1, title="Tipos de anomalías", labels=labels1)

        # Read the image of the graph and set the size it will be saved in
        img_data1 = Image(imgdata1, width=2.5 * inch, height=2.5 * inch)

         # New table that contains the last 2 images
        data = [(img_data, img_data1)]
        table1 = Table(data, 220)
        table1.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), transparent),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))


        # Group all the elements of this section
        block = KeepTogether([paragraphReportHeader, spacer, table, spacer, table1])
        self.elements.append(block)

        spacer = Spacer(10, 10)
        self.elements.append(spacer)


    def graph_overview(self):
        data_o = overview(self.dataset)
        # Styles for the section title
        psHeaderText2 = ParagraphStyle('Hed1', fontSize=15, alignment=TA_LEFT, borderWidth=3, textColor=black)
        text2 = 'Unique Value Analysis'
        # Flowable element for the title
        paragraphReportHeader2 = Paragraph(text2, psHeaderText2)

        spacer2 = Spacer(10, 6)

        object_data = [
            ["Object Columns", ""],
            ["", ""],
        ]
        object_data.extend(data_o['str_types'])

        num_data = [
            ["Numeric Columns", ""],
            ["", ""],
        ]
        num_data.extend(data_o['num_types'])

        date_data = [
            ["Date Time Columns", ""],
            ["", ""],
        ]
        date_data.extend(data_o['date_types'])

        col_widths = 125
        row_height = 0.4*inch

        obj_row_height = utils_io.multiple_row_height(row_height,object_data)
        num_row_height = utils_io.multiple_row_height(row_height,num_data)
        dat_row_height = utils_io.multiple_row_height(row_height,date_data)

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

        object_table = Table(object_data, colWidths=col_widths, rowHeights=obj_row_height, hAlign="LEFT")
        object_table.setStyle(table_style)

        num_table = Table(num_data, colWidths=col_widths, rowHeights=num_row_height, hAlign="LEFT")
        num_table.setStyle(table_style)

        date_table = Table(date_data, colWidths=col_widths, rowHeights=dat_row_height, hAlign="LEFT")
        date_table.setStyle(table_style)

        # New table that contains the last 3 tables
        data1 = [(object_table, num_table, date_table)]
        table1 = Table(data1, [180, 180, 100])
        table1.setStyle(TableStyle([
            ('VALIGN',(0,0),(-1,-1),'TOP'),
        ]))
        
        block1 = KeepTogether([paragraphReportHeader2, spacer2, table1])
        self.elements.append(block1)

    def scores(self):

        # Styles for the section title
        psHeaderText = ParagraphStyle('Hed0', fontSize=15, alignment=TA_LEFT, borderWidth=3, textColor=black)
        text = 'Overall Scores'
        # Flowable element for the title
        paragraphReportHeader1 = Paragraph(text, psHeaderText)

        spacer = Spacer(10, 10)

        incomplete_data = completeness(self.dataset)
        duplicated_data = uniqueness(self.dataset)
        invalid_data = validity(self.dataset)
        inaccurate_data = accuracy(self.dataset)

        data_o = overview(self.dataset)
        all_data = data_o['all']
        rows = data_o['rows']

        # Generate the table with the stat data
        # Completeness graph
        # TODO: For every test made != 0 generate an image with the data and the name
        completeness_data=[all_data, incomplete_data]
        imgdata_compl = utils_io.donut_plot(completeness_data, 'Completeness')

        # Read the image of the graph and set the size it will be saved in
        img_completeness = Image(imgdata_compl, width=self.plot_width, height=self.plot_height)


        # Uniqueness graph
        unique_data = [all_data, duplicated_data]
        imgdata_uniq = utils_io.donut_plot(unique_data, 'Uniqueness')

        # Read the image of the graph and set the size it will be saved in
        img_unique = Image(imgdata_uniq, width=self.plot_width, height=self.plot_height)


        # Validity graph
        valid_data = [all_data, invalid_data]
        imgdata_valid = utils_io.donut_plot(valid_data, 'Validity')

        # Read the image of the graph and set the size it will be saved in
        img_valid = Image(imgdata_valid, width=self.plot_width, height=self.plot_height)


        # Accurate graph
        accur_data = [all_data, inaccurate_data]
        imgdata_accur = utils_io.donut_plot(accur_data, 'Accuracy')

        # Read the image of the graph and set the size it will be saved in
        img_accurate = Image(imgdata_accur, width=self.plot_width, height=self.plot_height)

        # Overall data quality score
        overall_score = (1 - (incomplete_data + duplicated_data + invalid_data + inaccurate_data) / all_data) * 100

        psText = ParagraphStyle(name='a', fontSize=12, alignment=TA_LEFT, borderWidth=3, textColor=black)
        text2 = f"Data Quality Score: {overall_score:.1f}"
        # Flowable element for the title
        paragraph1 = Paragraph(text2, psText)

        # New table that contains the last 4 images
        data = [(img_completeness, img_unique, img_valid, img_accurate)]
        table = Table(data, 150)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), transparent),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))


        block = KeepTogether([paragraphReportHeader1, spacer, paragraph1, table])
        self.elements.append(block)

        spacer = Spacer(10, 10)
        self.elements.append(spacer)


    def nullity(self):
        # Styles for the section title
        psHeaderText1 = ParagraphStyle('Hed1', fontSize=15, alignment=TA_LEFT, borderWidth=3, textColor=black)
        text1 = 'Nullity Matrix'
        # Flowable element for the title
        paragraphReportHeader1 = Paragraph(text1, psHeaderText1)

        spacer1 = Spacer(10, 6)

        # Generate the nullity matrix
        fig = missingno.matrix(self.dataset, color=(.19,.95,.43))
        fig_copy = fig.get_figure()

        # Save the image as a stream of in-memory bytes
        imgdata = BytesIO()
        fig_copy.savefig(imgdata, format='png', bbox_inches='tight')
        imgdata.seek(0)  # rewind the data

        # Read the image of the graph and set the size it will be saved in
        img = Image(imgdata)
        img.drawHeight = 4 * inch
        img.drawWidth = 7.5 * inch

        block = KeepTogether([paragraphReportHeader1, spacer1, img])
        self.elements.append(block)

        spacer = Spacer(10, 20)
        self.elements.append(spacer)

if __name__ == '__main__':
    try:
        start = time.time()
        report = DataProfilingPDF()
        end = time.time()
        exc_time = end - start
        print(f"Report generated in {exc_time:.2f} seconds")

    except ValueError as ve:
        print(f"Error: {ve}")
        sys.exit(1)
