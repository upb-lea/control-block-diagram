from pylatex import Document, TikZ
from tkinter import filedialog
from tkinter import *
import os
import tempfile
import subprocess


class ControllerDiagram:

    def __init__(self, data_type: (str, tuple, list) = ()):
        self._data_type = data_type if isinstance(data_type, (tuple, list)) else [data_type]
        self._pdf_name = None
        self._clean_tex = 'tex' not in self._data_type
        self._components = []
        self._subprocess = None

    def append(self, component):
        if isinstance(component, (list, tuple)):
            self._components.extend(component)
        else:
            self._components.append(component)

    def build(self):
        doc = Document(page_numbers=False, geometry_options={'landscape': True, 'includeheadfoot': False})
        with doc.create(TikZ()) as pic:
            for component in self._components:
                component.build(pic)

        for filename in self._get_filename():
            name, data_type = filename.split('.', 1)
            if data_type == 'pdf':
                doc.generate_pdf(name, compiler='pdflatex', clean_tex=self._clean_tex)
                self._pdf_name = filename
            elif data_type == 'tex':
                doc.generate_tex(name)

    def show(self):
        if self._pdf_name is not None:
            os.system(self._pdf_name)
        if 'pdf' not in self._data_type:
            os.remove(self._pdf_name)

    def open(self):
        if self._pdf_name is not None:
            self._subprocess = subprocess.Popen(self._pdf_name, shell=True, stdout=subprocess.PIPE)

    def close(self):
        if len(self._data_type) == 0:
            os.remove(self._pdf_name)

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
        if 'pdf' not in self._data_type:
            yield tempfile.gettempdir() + r'\ControlBlockDiagram.pdf'
