
class Component:
    _document = None

    def __init__(self):
        if Component._document is not None:
            Component._document.append(self)

    def build(self, pic):
        pass


def set_document(doc):
    Component._document = doc
