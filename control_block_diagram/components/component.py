class Component:
    """
        Base class for a component. Saves the active document and the associated default parameters as a class variable
         so that they are already known at creation.
    """
    _document = None
    configuration = dict()

    @property
    def border_left(self):
        """Returns the left boundary of a component"""
        return self._border_left

    @property
    def border_top(self):
        """Returns the top boundary of a component"""
        return self._border_top

    @property
    def border_right(self):
        """Returns the right boundary of a component"""
        return self._border_right

    @property
    def border_bottom(self):
        """Returns the bottom boundary of a component"""
        return self._border_bottom

    def __init__(self):
        """Initializes a component and adds it to the active diagram."""
        if Component._document is not None:
            Component._document.append(self)
        self._configuration = Component.configuration

        self._border_left = None
        self._border_top = None
        self._border_right = None
        self._border_bottom = None

    def _set_border(self, *args):
        """Sets the boundaries of a component to subsequently determine the size of a document"""
        for point in args:
            if self._border_left is None:
                self._border_left = point.x
                self._border_right = point.x
                self._border_top = point.y
                self._border_bottom = point.y

            else:
                self._border_left = min(self._border_left, point.x)
                self._border_right = max(self._border_right, point.x)
                self._border_top = max(self._border_top, point.y)
                self._border_bottom = min(self._border_bottom, point.y)

    def build(self, pic):
        """Generates the code which will be written into the latex file"""
        pass

    @staticmethod
    def get_size(components: (list, tuple) = ()):
        """Calculates the size of a document"""
        left = min([c.border_left for c in components])
        right = max([c.border_right for c in components])
        top = max([c.border_top for c in components])
        bottom = min([c.border_bottom for c in components])
        return (right - left) + 2, (top - bottom) + 2


def set_document(doc):
    """Sets a document as an active document"""
    doc.set_document()
    doc.set_cofiguration()
