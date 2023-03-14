from pylatex import Document, TikZ
from pylatex.package import Package
from tkinter import filedialog
from tkinter import *
from .components.component import Component
import os
import sys
import tempfile
from IPython.display import display
from .pdf_viewer import PDFViewer
from .pdf_viewer import PDFViewerNB


class ControllerDiagram:
    """
        This is the base class for all diagrams. A diagram is automatically set as active diagram after instantiation
        and all subsequent components are added to it. A diagram can finally be saved as a .tex or a .pdf file.
    """

    @property
    def filename(self):
        """Returns the name of the PDF file"""
        if self._pdf_name is not None:
            return self._pdf_name
        elif self._temp_file is not None:
            return self._temp_file

    def __init__(self, packages: (tuple, list) = ('upgreek',), **configuration):
        """
            Initializes a new diagram and sets it as the active diagram.
                :param packages:       Required Latex Packages
                :param configuration:  Possible default parameters for the entire diagram
        """
        self._packages = packages
        self._configuration_input = configuration
        self._configuration = dict()
        self._data_type = None
        self._pdf_name = None
        self._local_name = None
        self._clean_tex = None
        self._components = []
        self._pdf_viewer = None
        self._doc = None
        self._temp_file = None
        self._changed = True
        self._size = (0, 0)
        self.set_document()

    def set_document(self):
        """
             Sets a passed diagram as active diagram and loads the default parameters.
        """
        Component._document = self
        self._configuration['draw'] = self._configuration_input.get('color', 'black')
        self._configuration['text_color'] = self._configuration_input.get('color', 'black')
        self._configuration['draw'] = self._configuration_input.get('draw', self._configuration['draw'])
        self._configuration['fill'] = self._configuration_input.get('fill', 'white')
        self._configuration['rounded_corners'] = self._configuration_input.get('rounded_corners', '0pt')
        self._configuration['line_width'] = self._configuration_input.get('line_width', 'thick')
        self._configuration['line_style'] = self._configuration_input.get('line_style', 'solid')
        self._configuration['fontsize'] = self._configuration_input.get('fontsize', r'\normalsize')
        self._configuration['font'] = self._configuration_input.get('font', r'')
        self._configuration['text_color'] = self._configuration_input.get('text_color',
                                                                          self._configuration['text_color'])

        Component.configuration = self._configuration

    def append(self, component):
        """
            Adds a new component to a diagram.
                component: Component or list of components to be added
        """

        if isinstance(component, (list, tuple)):
            for comp in component:
                self.append(comp)
        else:
            self._components.append(component)
            self._changed = True

    def save(self, *data_type):
        """
            First creates a latex file from the added components. From this file a PDF file can be created and saved.
        """

        # Store the data types
        self._data_type = data_type if isinstance(data_type, (tuple, list)) else [data_type]
        self._clean_tex = 'tex' not in self._data_type

        # build the pylatex document
        self._build()

        # Opens the window for selecting the folder and entering the file name and generates the desired file
        for filename in self._get_filename():
            name, data_type = filename.rsplit('.', 1)
            if data_type == 'pdf':
                self._doc.generate_pdf(name, compiler='pdflatex', clean_tex=self._clean_tex)
                self._pdf_name = filename
            elif data_type == 'tex' and 'pdf' not in self._data_type:
                self._doc.generate_tex(name)

    def _build(self):
        """
            Builds the pylatex document
        """

        self.size = Component.get_size(self._components)  # Determines the size of the latex document
        # Creates the latex document
        self._doc = Document(page_numbers=False, geometry_options={'includeheadfoot': False,
                                                                   'top': '0.3cm', 'left': '0.3cm',
                                                                   'paperwidth': str(self.size[0]) + 'cm',
                                                                   'paperheight': str(self.size[1]) + 'cm'})

        # Adds the required latex packages to the document
        for package in self._packages:
            self._doc.packages.append(Package(package))

        # Sorts the components by level
        self._components.sort(key=lambda comp: comp.level)

        # Adds all components to the latex document
        with self._doc.create(TikZ()) as pic:
            for component in self._components:
                component.build(pic)

        self._changed = False

    def build_temp(self):
        """
             Creates a temporary PDF file to display it in the PDF Viewer.
        """
        filename = tempfile.gettempdir() + r'\ControlBlockDiagram'
        self._temp_file = filename + '.pdf'
        if self._doc is None or self._changed:
            self._build()
        self._doc.generate_pdf(filename, compiler='pdflatex', clean_tex=True)
        return self._temp_file

    def delete_temp(self):
        """
             Deletes the temporary PDF file.
        """
        os.remove(self._temp_file)

    def show(self):
        """
            Displays the PDF file in the PDF Viewer. If it is a temporary PDF file, it will be created before and then
            deleted after closing the window. The program will continue to run after the window is closed.
        """

        if 'ipykernel' in sys.modules:
            self._build_local()
            display(PDFViewerNB(self._local_name, size=(int(min(900, self.size[0] * 50 + 50)),
                                                                int(self.size[1] * 50 + 50))))

        elif self._pdf_name is not None:
            self._pdf_viewer = PDFViewer(self._pdf_name, size=(int(self.size[0] * 40), int(self.size[1] * 45)))
            self._pdf_viewer.show_pdf()

        else:
            self.build_temp()
            self._pdf_viewer = PDFViewer(self._temp_file, size=(int(self.size[0] * 40), int(self.size[1] * 45)))
            self._pdf_viewer.show_pdf()
            self.delete_temp()

    def _build_local(self):
        """
            Builds a PDF file in the current working directory
        """
        self._local_name = os.getcwd() + r'ControlBlockDiagram'
        if self._doc is None or self._changed:
            self._build()
        self._doc.generate_pdf(self._local_name, compiler='pdflatex', clean_tex=True)

    def _delete_local(self):
        """
            Delete the local file
        """
        os.remove(self._local_name + '.pdf')

    def open(self):
        """
            Opens an existing PDF file in the PDF Viewer or creates a temporary PDF file. The PDF Viewer is started in
            the background so that the program flow is not interrupted. The window is closed by the close method and
            the temporary PDF file is deleted.
        """
        
        if 'ipykernel' in sys.modules:
            self._build_local()
            display(PDFViewerNB('ControlBlockDiagram.pdf', size=(int(min(900, self.size[0] * 50 + 50)),
                                                                int(self.size[1] * 50 + 50))))
        else:
            if self._pdf_name is not None:
                self._pdf_viewer = PDFViewer(self._pdf_name, size=(int(self.size[0] * 40), int(self.size[1] * 45)))
            else:
                self.build_temp()
                self._pdf_viewer = PDFViewer(self._temp_file, size=(int(self.size[0] * 40), int(self.size[1] * 45)))

            self._pdf_viewer.open_pdf()

    def close(self):
        """
            Closes the PDF Viewer and deletes the temporary PDF file if necessary.
        """
        if 'ipykernel' in sys.modules:
            if self._temp_file is not None:
                self.delete_temp()
        else:
            self._pdf_viewer.close_pdf()
            if self._temp_file is not None:
                self.delete_temp()

    def __del__(self):
        """
            Delete all temporary files
        """
        if self._temp_file is not None:
            try:
                self.delete_temp()
            except FileNotFoundError:
                pass
        if self._local_name is not None:
            try:
                self._delete_local()
            except FileNotFoundError:
                pass

    def _get_filename(self):
        """
             Creates the window for selecting the folder and entering the file name.
        """
        win = Tk()
        win.withdraw()
        for data_type in self._data_type:
            if 'pdf' == data_type:
                filetypes = (('Portable Document Format (*.pdf)', '*.pdf'), ('All Files', '*.*'))
                yield filedialog.asksaveasfilename(initialdir='/', title='Save as', filetypes=filetypes,
                                                   defaultextension='.pdf')
            elif 'tex' == data_type and 'pdf' not in self._data_type:
                filetypes = (('TeX Document (*.tex)', '*.tex'), ('All Files', '*.*'))
                yield filedialog.asksaveasfilename(initialdir='/', title='Save as', filetypes=filetypes,
                                                   defaultextension='.tex')
            elif data_type not in ['pdf', 'tex']:
                raise ValueError(
                    f'The file type {data_type} is not supported. Use the Portable Document Format (pdf) or Tex'
                    f' Document (tex) file type.')
