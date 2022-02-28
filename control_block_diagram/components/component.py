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

        self._border_left = None
        self._border_top = None
        self._border_right = None
        self._border_bottom = None

    def _set_border(self, *args):
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
        pass

    @staticmethod
    def get_size(components: (list, tuple) = ()):
        left = min([c.border_left for c in components])
        right = max([c.border_right for c in components])
        top = max([c.border_top for c in components])
        bottom = min([c.border_bottom for c in components])
        return (right - left) + 2, (top - bottom) + 2


def set_document(doc):
    doc.set_document()
    doc.set_cofiguration()
