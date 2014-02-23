from lxml import etree


class HOCRParser:
    """
        Parse hOCR documents

        Takes either a file-like object or a filename
    """
    def __init__(self, input):
        self.input = input

    def parse(self):
        fp = None
        if isinstance(self.input, basestring):
            fp = open(self.input, 'rb')
        else:
            fp = input

        self.data = fp.read()

