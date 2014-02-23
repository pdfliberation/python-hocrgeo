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
        id = page.get('id')
        self._pages[id] = page

    def get_page(self, id):
        '''
        Retrieve a page by it's id

        :param id: id of the page element you wish to retrieve
        '''
        return self._pages[id]

    @property
    def pages(self):
        return self._pages.values()

    def to_dict(self):
        '''Return the document as a dictionary. So it is serliazable'''
        _datadict = self._data.copy()
        _datadict['pages'] = self._pages.values()
        return _datadict

    def __str__(self):
        return self._data.__str__()

    def __repr__(self):
        return '<HOCRDocument {0}>'.format(self.__str__())
