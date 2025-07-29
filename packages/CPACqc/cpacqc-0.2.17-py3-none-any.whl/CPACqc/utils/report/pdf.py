import pandas as pd
from fnmatch import fnmatch
from CPACqc.core.logger import logger
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from colorama import Fore, Style
import os
import json
from dataclasses import dataclass, field
from CPACqc.services.report_generator_service import ReportGeneratorService

@dataclass
class Report(ReportGeneratorService):
    _instance: "Report" = field(default=None, init=False, repr=False)
    df: pd.DataFrame = None
    qc_dir: str = None
    sub_ses: str = None
    overlay_df: pd.DataFrame = None
    pdf_path: str = field(init=False)
    pdf_canvas: canvas.Canvas = field(init=False)
    width: int = field(init=False, default=letter[0])
    height: int = field(init=False, default=letter[1])
    styles: object = field(init=False, default_factory=getSampleStyleSheet)
    missing_files: list = field(default_factory=list)
    page_number: int = field(init=False, default=1)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Report, cls).__new__(cls)
        return cls._instance

    def __post_init__(self):
        if self.qc_dir and self.sub_ses:
            self.pdf_path = self.get_pdf_path()
            self.pdf_canvas = canvas.Canvas(self.pdf_path, pagesize=letter)
            self.page_number = 1
        else:
            self.pdf_path = None
            self.pdf_canvas = None

    @classmethod
    def destroy_instance(cls):
        if cls._instance:
            cls._instance = None

    def add_missing_files(self, missing_files):
        self.missing_files.append(missing_files)
        return

    def get_pdf_path(self):
        pdf = f"{self.sub_ses}_qc_report.pdf"
        base_dir = self.qc_dir if self.qc_dir and ".temp" not in self.qc_dir else os.getcwd()
        return os.path.join(base_dir, pdf)

    def show_content_page(self, chapter=None, scan=None):
        self.pdf_canvas.showPage()
        self.page_number += 1
        # Only add header/footer for regular content pages (not chapter/scan/missing files)
        if chapter is not None and scan is not None and chapter != "chapter_section" and scan != "subchapter_section":
            self.add_header(chapter, scan)
            self.add_footer(self.page_number)

    def add_front_page(self):
        logo_path = 'https://avatars.githubusercontent.com/u/2230402?s=200&v=4'
        logo_img = ImageReader(logo_path)
        logo_width = 150
        logo_height = 150

        self.pdf_canvas.setFont("Helvetica", 25)
        title = Paragraph(f"{self.sub_ses.replace('_', ' ')}", self.styles['Title'])
        title.wrapOn(self.pdf_canvas, self.width - 40, self.height)
        title.drawOn(self.pdf_canvas, 20, self.height - 100)

        self.pdf_canvas.drawImage(logo_img, (self.width - logo_width) / 2, (self.height - logo_height) / 2, width=logo_width, height=logo_height)
        self.pdf_canvas.setFont("Helvetica", 15)
        self.pdf_canvas.drawCentredString(self.width / 2, self.height - 120, "Quality Control Report")

        self.pdf_canvas.setFont("Helvetica", 12)
        self.pdf_canvas.drawCentredString(self.width / 2, 100, f"Created on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.pdf_canvas.drawCentredString(self.width / 2, 80, "CPAC Team")
        self.pdf_canvas.showPage()
        # Do not increment page_number or add header/footer

    def add_contents_page(self):
        self.pdf_canvas.setFont("Helvetica", 20)
        self.pdf_canvas.drawCentredString(self.width / 2, self.height - 100, "Contents")
        self.pdf_canvas.setFont("Helvetica", 12)
        y_position = self.height - 150
        chapters = sorted(set(self.df['datatype'].dropna()))

        for chapter in chapters:
            if y_position < 50:
                self.pdf_canvas.showPage()
                y_position = self.height - 50
            y_position -= 20
            self.pdf_canvas.setFillColor(colors.blue)
            self.pdf_canvas.drawString(80, y_position, f"{chapter}")
            text_width = self.pdf_canvas.stringWidth(chapter, "Helvetica", 12)
            self.pdf_canvas.linkRect("", f"chapter_{chapter}", (80, y_position - 2, 80 + text_width, y_position + 10), color=colors.blue)
            self.pdf_canvas.bookmarkPage(f"chapter_{chapter}")
            self.pdf_canvas.addOutlineEntry(f"{chapter}", f"chapter_{chapter}", level=0)
            y_position -= 10

            chapter_data = self.df[self.df['datatype'] == chapter]
            scans = sorted(set(chapter_data['scan'].dropna()))
            for scan in scans:
                if y_position < 50:
                    self.pdf_canvas.showPage()
                    y_position = self.height - 50
                self.pdf_canvas.setFillColor(colors.green)
                self.pdf_canvas.drawString(100, y_position, f"{scan}")
                text_width = self.pdf_canvas.stringWidth(scan, "Helvetica", 12)
                if scan.strip() == '':
                    self.pdf_canvas.linkRect("", f"subsection_{chapter}", (100, y_position - 2, 100 + text_width, y_position + 10), color=colors.green)
                    self.pdf_canvas.bookmarkPage(f"subsection_{chapter}")
                    self.pdf_canvas.addOutlineEntry(f"{chapter}", f"subsection_{chapter}", level=1)
                else:
                    self.pdf_canvas.linkRect("", f"subsection_{chapter}_{scan}", (100, y_position - 2, 100 + text_width, y_position + 10), color=colors.green)
                    self.pdf_canvas.bookmarkPage(f"subsection_{chapter}_{scan}")
                    self.pdf_canvas.addOutlineEntry(f"{chapter} - {scan}", f"subsection_{chapter}_{scan}", level=1)
                y_position -= 10

                scan_data = chapter_data[chapter_data['scan'] == scan]
                if not scan_data.empty:
                    ordered_images = []
                    extra_images = []
                    if self.overlay_df is not None:
                        ordered_images = scan_data[scan_data['resource_name'].isin(self.overlay_df['output'])]
                        extra_images = scan_data[~scan_data['resource_name'].isin(self.overlay_df['output'])]
                    else:
                        ordered_images = scan_data
                    ordered_images = ordered_images.drop_duplicates(subset='file_name', keep='last')
                    extra_images = extra_images.drop_duplicates(subset='file_name', keep='last')
                    for _, image_data in ordered_images.iterrows():
                        if y_position < 50:
                            self.pdf_canvas.showPage()
                            y_position = self.height - 50
                        self.pdf_canvas.setFillColor(colors.black)
                        self.pdf_canvas.drawString(120, y_position, f"{image_data['resource_name']}")
                        text_width = self.pdf_canvas.stringWidth(image_data['resource_name'], "Helvetica", 12)
                        self.pdf_canvas.linkRect("", f"image_{chapter}_{scan}_{image_data['resource_name']}", (120, y_position - 2, 120 + text_width, y_position + 10), color=colors.blue)
                        self.pdf_canvas.bookmarkPage(f"image_{chapter}_{scan}_{image_data['resource_name']}")
                        self.pdf_canvas.addOutlineEntry(f"{image_data['resource_name']}", f"image_{chapter}_{scan}_{image_data['resource_name']}", level=2)
                        y_position -= 13
                    for _, image_data in extra_images.iterrows():
                        if y_position < 50:
                            self.pdf_canvas.showPage()
                            y_position = self.height - 50
                        self.pdf_canvas.setFillColor(colors.black)
                        self.pdf_canvas.drawString(120, y_position, f"{image_data['resource_name']}")
                        text_width = self.pdf_canvas.stringWidth(image_data['resource_name'], "Helvetica", 12)
                        self.pdf_canvas.linkRect("", f"image_{chapter}_{scan}_{image_data['resource_name']}", (120, y_position - 2, 120 + text_width, y_position + 10), color=colors.blue)
                        self.pdf_canvas.bookmarkPage(f"image_{chapter}_{scan}_{image_data['resource_name']}")
                        self.pdf_canvas.addOutlineEntry(f"{image_data['resource_name']}", f"image_{chapter}_{scan}_{image_data['resource_name']}", level=2)
                        y_position -= 13
                y_position -= 10
        self.pdf_canvas.showPage()


    def add_images(self):
        chapters = sorted(set(self.df['datatype'].dropna()))
        for chapter in chapters:
            self.add_chapter_title_page(chapter)
            chapter_data = self.df[self.df['datatype'] == chapter]
            scans = sorted(set(chapter_data['scan'].dropna()))
            for scan in scans:
                self.add_scan_title_page(chapter, scan)
                scan_data = chapter_data[chapter_data['scan'] == scan]
                if not scan_data.empty:
                    ordered_images = []
                    extra_images = []
                    if self.overlay_df is not None:
                        ordered_images = scan_data[scan_data['resource_name'].isin(self.overlay_df['output'])]
                        extra_images = scan_data[~scan_data['resource_name'].isin(self.overlay_df['output'])]
                    else:
                        ordered_images = scan_data
                    ordered_images = ordered_images.drop_duplicates(subset='file_name', keep='last')
                    extra_images = extra_images.drop_duplicates(subset='file_name', keep='last')

                    y_position = self.height - 30
                    for _, image_data in ordered_images.iterrows():
                        y_position = self.add_image(image_data, chapter, scan, y_position)
                    for _, image_data in extra_images.iterrows():
                        y_position = self.add_image(image_data, chapter, scan, y_position)

    def add_chapter_title_page(self, chapter):
        self.pdf_canvas.setFont("Helvetica", 30)
        self.pdf_canvas.drawCentredString(self.width / 2, self.height / 2, chapter)
        self.pdf_canvas.bookmarkPage(f"chapter_{chapter}")
        self.pdf_canvas.showPage()  # This is fine, as chapter pages are not followed by headers/footers

    def add_scan_title_page(self, chapter, scan):
        if scan.strip() == '':
            print(Fore.YELLOW + f"Scan name is empty for chapter {chapter}. Skipping..." + Style.RESET_ALL)
            self.pdf_canvas.bookmarkPage(f"subsection_{chapter}")
            return
        self.pdf_canvas.setFont("Helvetica", 25)
        self.pdf_canvas.drawCentredString(self.width / 2, self.height / 2, f"{chapter} - {scan}")
        self.pdf_canvas.bookmarkPage(f"subsection_{chapter}_{scan}")
        self.pdf_canvas.showPage()  # This is fine, as scan pages are not followed by headers/footers

    def add_image(self, image_data, chapter, scan, y_position):
        image_path = os.path.join(self.qc_dir, image_data['relative_path'])
        if os.path.exists(image_path):
            # Add header/footer at the start of image/detail pages
            self.add_header(chapter, scan)
            self.add_footer(self.page_number)
            img = ImageReader(image_path)
            max_img_width = self.width - 20
            max_img_height = self.height - 100
            img_width, img_height = img.getSize()
            aspect_ratio = img_width / img_height
            if aspect_ratio > 1:
                img_width = max_img_width
                img_height = img_width / aspect_ratio
            else:
                img_height = max_img_height
                img_width = img_height * aspect_ratio
            if y_position - img_height - 140 < 0:
                self.page_number += 1
                self.pdf_canvas.showPage()
                self.add_header(chapter, scan)
                self.add_footer(self.page_number)
                y_position = self.height - 30
            self.pdf_canvas.setFont("Helvetica", 15)
            self.pdf_canvas.drawString(10, y_position - 20, f"{image_data['resource_name']}")
            self.pdf_canvas.bookmarkPage(f"image_{chapter}_{scan}_{image_data['resource_name']}")
            self.pdf_canvas.drawImage(img, (self.width - img_width) / 2, y_position - img_height - 40, width=img_width, height=img_height)
            table_height = self.add_image_details(image_data, y_position, img_height)
            json_table_height = self.add_json_details(image_data, y_position - img_height - table_height - 80, chapter, scan)
            y_position -= img_height + table_height + json_table_height + 90
            # Only increment page number and show page if more images/details are coming
            if y_position < 100:  # If not enough space for next image, start new page
                self.page_number += 1
                self.pdf_canvas.showPage()
            return y_position
        return y_position

    def add_json_details(self, image_data, y_position, chapter=None, scan=None):
        flat_json = image_data.get('json', None)
        if flat_json is None or flat_json == '' or flat_json == {}:
            print(Fore.YELLOW + f"JSON data is empty for {image_data.get('file_name', '')}. Skipping..." + Style.RESET_ALL)
            return 0
        if isinstance(flat_json, str):
            try:
                flat_json = json.loads(flat_json)
            except Exception as e:
                print(Fore.YELLOW + f"Could not parse JSON for {image_data.get('file_name', '')}: {e}" + Style.RESET_ALL)
                return 0
        if not flat_json or flat_json == {}:
            print(Fore.YELLOW + f"JSON data is empty for {image_data.get('file_name', '')}. Skipping..." + Style.RESET_ALL)
            return 0
        json_text = [["Json Field", "Value"]]
        for key, value in flat_json.items():
            if not key or (isinstance(value, float) and pd.isna(value)):
                continue
            self.styles['Normal'].textColor = colors.black
            para_key = Paragraph(str(key), self.styles['Normal'])
            para_value = Paragraph(str(value), self.styles['Normal'])
            json_text.append([para_key, para_value])
        if len(json_text) == 1:
            print(Fore.YELLOW + f"JSON data is empty for {image_data.get('file_name', '')}. Skipping..." + Style.RESET_ALL)
            return 0

        col1_width = min(180, self.width * 0.3)
        col2_width = self.width - 20 - col1_width

        margin_bottom = 40
        total_height = 0
        first_page = True
        row_idx = 1
        while row_idx < len(json_text):
            available_height = y_position - margin_bottom if first_page else self.height - 50 - margin_bottom
            rows = [json_text[0]]
            max_rows = 1
            for i in range(row_idx, len(json_text)):
                rows.append(json_text[i])
                t = Table(rows, colWidths=[col1_width, col2_width], repeatRows=1)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                h = t.wrap(self.width - 20, available_height)[1]
                if h > available_height:
                    break
                max_rows = i - row_idx + 1
            if max_rows == 0:
                break  # Prevent empty page
            rows = [json_text[0]] + json_text[row_idx:row_idx + max_rows]
            t = Table(rows, colWidths=[col1_width, col2_width], repeatRows=1)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            t.wrapOn(self.pdf_canvas, self.width - 20, self.height)
            t_height = t.wrap(self.width - 20, available_height)[1]
            t.drawOn(self.pdf_canvas, 10, y_position - t_height)
            y_position -= t_height
            total_height += t_height
            row_idx += max_rows
            if row_idx < len(json_text):
                # Only show a new page if there are more rows to add
                self.page_number += 1
                self.pdf_canvas.showPage()
                self.add_header(chapter, scan)
                self.add_footer(self.page_number)
                y_position = self.height - 50  # Start lower to avoid header overlap
                first_page = False
        return total_height + 10
    

    def add_image_details(self, image_data, y_position, img_height):
        label = f"{image_data['file_name']}"
        self.styles['Normal'].textColor = colors.whitesmoke
        wrapped_label = Paragraph(label, self.styles['Normal'])
        wrapped_label.wrapOn(self.pdf_canvas, self.width - 20, self.height)
        file_info = json.loads(image_data['file_info'])
        file_info_text = [
            ["Image:", wrapped_label],
            ["Orientation:", file_info['orientation']],
            ["Dimensions:", " x ".join(map(str, file_info['dimension']))],
            ["Resolution:", " x ".join(map(lambda x: str(round(x, 2)), file_info['resolution']))]
        ]
        if file_info['tr'] is not None:
            file_info_text.append(["TR:", str(round(file_info['tr'], 2))])
        if file_info['nos_tr'] is not None:
            file_info_text.append(["No of TRs:", str(file_info['nos_tr'])])
        table = Table(file_info_text, colWidths=[80, self.width - 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        table.wrapOn(self.pdf_canvas, self.width - 20, self.height)
        table_height = table.wrap(self.width - 20, self.height)[1]
        table.drawOn(self.pdf_canvas, 10, y_position - img_height - table_height - 60)
        return table_height


    def add_header(self, chapter, scan):
        self.pdf_canvas.setFont("Helvetica", 12)
        self.pdf_canvas.drawString(10, self.height - 30, f"Chapter : {chapter}/{scan}")

    def add_footer(self, page_number):
        self.pdf_canvas.drawRightString(self.width - 30, 20, str(page_number))

    def add_missing_files_page(self):
        if not self.missing_files:
            print(Fore.YELLOW + "No missing files to report." + Style.RESET_ALL)
            return
        self.pdf_canvas.bookmarkPage("Missing Files")
        self.pdf_canvas.setFont("Helvetica", 20)
        self.pdf_canvas.drawCentredString(self.width / 2, self.height - 120, "Missing Files")
        self.pdf_canvas.setFont("Helvetica", 12)
        y_position = self.height - 150
        for file in self.missing_files:
            print(Fore.YELLOW + f"Missing file: {file}" + Style.RESET_ALL)
            if y_position < 50:
                self.pdf_canvas.showPage()
                y_position = self.height - 50
            self.pdf_canvas.setFont("Helvetica", 12)
            self.pdf_canvas.drawString(70, y_position - 20, file)
            y_position -= 13
        self.pdf_canvas.showPage()
        self.pdf_canvas.setFont("Helvetica", 25)
        self.pdf_canvas.drawCentredString(self.width / 2, self.height / 2, "End of Report")
        self.pdf_canvas.showPage()


    def generate_report(self):
        print(Fore.YELLOW + "Generating PDF report..." + Style.RESET_ALL)
        self.add_front_page()
        self.add_contents_page()
        self.page_number = 1 
        self.add_images()
        self.add_missing_files_page()
        print(Fore.GREEN + "PDF report generated successfully." + Style.RESET_ALL)

    def save_report(self):
        if self.pdf_canvas:
            self.pdf_canvas.save()
            print(Fore.GREEN + f"PDF report saved at {self.pdf_path}" + Style.RESET_ALL)
        else:
            print(Fore.RED + "PDF canvas is not initialized." + Style.RESET_ALL)