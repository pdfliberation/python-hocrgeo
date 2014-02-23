from collections import OrderedDict

class HOCRDocument:
    """
    Class that wraps a dictionary with some useful methods
    """
    def __init__(self):
        self._pages = OrderedDict()
        self._data = {
            'pages': self._pages
        }

    def add(self, name, item):
        '''Add aribtrary information to the document'''
        self._data[name] = item

    def add_page(self, page):
        '''Add a page element to the document'''
        self._pages.append(page)

    def get_page(self, id):
        '''
        Retrieve a page by it's id

        :param id: id of the page element you wish to retrieve
        '''
        self._pages

    @property
    def pages(self):
        return self._pages

    def __str__(self):
        return self._data.__str__()

    def __repr__(self):
        return '<HOCRDocument {0}>'.format(self.__str__())
