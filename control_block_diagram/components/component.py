class Component:
    _document = None
    configuration = dict()

    @property
    def border_left(self):
        return self._border_left

    @property
    def border_top(self):
        return self._border_top

    @property
    def border_right(self):
        return self._border_right

    @property
    def border_bottom(self):
        return self._border_bottom

    def __init__(self):
        if Component._document is not None:
            Component._document.append(self)
        self._configuration = Component.configuration

        self._border_left = 0
        self._border_top = 0
        self._border_right = 1
        self._border_bottom = 1

    def build(self, pic):
        pass


def set_document(doc):
    doc.set_document()
    doc.set_cofiguration()
