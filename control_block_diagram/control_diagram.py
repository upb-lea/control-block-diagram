from pylatex import Document, TikZ
from pylatex.package import Package
from tkinter import filedialog
from tkinter import *
from .components.component import Component
import os
import tempfile
from .pdf_viewer import PDFViewer


class ControllerDiagram:

    def __init__(self, data_type: (str, tuple, list) = (), **configuration):
        self._data_type = data_type if isinstance(data_type, (tuple, list)) else [data_type]
        self._pdf_name = None
        self._clean_tex = 'tex' not in self._data_type
        self._components = []
        self._pdf_viewer = None
        self._configuration_input = configuration
        self._configuration = dict()
        self.set_document()
        self._doc = None
        self._temp_file = None
        self._min_x = 0
        self._min_y = 0
        self._max_x = 0
        self._max_y = 0

    def set_document(self):
        Component._document = self
        self._configuration['draw'] = self._configuration_input.get('draw', 'black')
        self._configuration['fill'] = self._configuration_input.get('fill', 'white')
        self._configuration['line_width'] = self._configuration_input.get('line_width', 'thin')
        self._configuration['fontsize'] = self._configuration_input.get('fontsize', r'\normalsize')
        self._configuration['text_color'] = self._configuration_input.get('text_color', 'black')

        Component.configuration = self._configuration

    def append(self, component):
        if isinstance(component, (list, tuple)):
            for comp in component:
                self.append(comp)
        else:
            self._components.append(component)

    def build(self):
        size = Component.get_size(self._components)
        self._doc = Document(page_numbers=False, geometry_options={'includeheadfoot': False,
                                                                   'top': '0.3cm', 'left': '0.3cm',
                                                                   'paperwidth': str(size[0]) + 'cm',
                                                                   'paperheight': str(size[1]) + 'cm'})
        self._doc.packages.append(Package('upgreek'))
        with self._doc.create(TikZ()) as pic:
            for component in self._components:
                component.build(pic)

        for filename in self._get_filename():
            name, data_type = filename.split('.', 1)
            if data_type == 'pdf':
                self._doc.generate_pdf(name, compiler='pdflatex', clean_tex=self._clean_tex)
                self._pdf_name = filename
            elif data_type == 'tex':
                self._doc.generate_tex(name)

    def _build_temp(self):
        filename = tempfile.gettempdir() + r'\ControlBlockDiagram'
        self._temp_file = filename + '.pdf'
        self._doc.generate_pdf(filename, compiler='pdflatex', clean_tex=True)

    def _delete_temp(self):
        os.remove(self._temp_file)

    def show(self):
        if self._pdf_name is not None:
            self._pdf_viewer = PDFViewer(self._pdf_name)
            self._pdf_viewer.show_pdf()

        else:
            self._build_temp()
            self._pdf_viewer = PDFViewer(self._temp_file)
            self._pdf_viewer.show_pdf()
            self._delete_temp()

    def open(self):
        if self._pdf_name is not None:
            self._pdf_viewer = PDFViewer(self._pdf_name)
        else:
            self._build_temp()
            self._pdf_viewer = PDFViewer(self._temp_file)

        self._pdf_viewer.open_pdf()

    def close(self):
        self._pdf_viewer.close_pdf()
        if self._temp_file is not None:
            self._delete_temp()

    def _get_filename(self):
        win = Tk()
        win.withdraw()
        for data_type in self._data_type:
            if 'pdf' == data_type:
                filetypes = (('Portable Document Format (*.pdf)', '*.pdf'), ('All Files', '*.*'))
                yield filedialog.asksaveasfilename(initialdir='/', title='Save as', filetypes=filetypes,
                                                   defaultextension='.pdf')
            elif 'tex' == data_type:
                filetypes = (('TeX Document (*.tex)', '*.tex'), ('All Files', '*.*'))
                yield filedialog.asksaveasfilename(initialdir='/', title='Save as', filetypes=filetypes,
                                                   defaultextension='.tex')
            else:
                raise ValueError(
                    f'The file type {data_type} is not supported. Use the Portable Document Format (pdf) or Tex Document (tex) file type.')
