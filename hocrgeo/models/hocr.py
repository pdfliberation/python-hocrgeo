from __future__ import unicode_literals

from shapely.geometry import Polygon, box

from shapely import speedups

if speedups.available:
    speedups.enable()


class HOCRMeta(object):
    """Metadata about an hOCR document"""
    def __init__(self, obj=None):
        super(HOCRMeta, self).__init__()
        if isinstance(obj, dict):
            self._raw = obj
            for k,v in self._raw:
                attr_name = k.replace('ocr-', '', 1)
                setattr(self, attr_name, v)


class HOCRElement(object):
    """Generic element in hOCR that can define an id and a bbox"""

    def __init__(self, obj=None):
        super(HOCRElement, self).__init__()
        self._raw = obj
        self._id = None
        self._bbox = None
        if self._raw:
            if isinstance(self._raw, dict):
                for key, value in self._raw.items():
                    attr_name = key.replace('ocr-', '', 1)
                    value = self._raw.get(key)
                    if isinstance(value, dict):
                        value = HOCRElement(value)
                    elif isinstance(value, list):
                        value_list = []
                        for item in value:
                            elem = HOCRElement(item)
                            value_list.append(elem)
                        value = value_list
                    setattr(self, attr_name, value)

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        self._id = value

    @property
    def bbox(self):
        return self._bbox
    @bbox.setter
    def bbox(self, value):
        if isinstance(value, Polygon):
            self._bbox = value
        elif isinstance(value, tuple):
            self._bbox = box(*value)
        elif value is None:
            self._bbox = None
        else:
            raise TypeError('bbox is not a shapely box or tuple of coordinates')


class HOCRPage(HOCRElement):
    """An HOCRPage contains a bbox, image, pagenumber, etc."""

    def __init__(self, obj):
        super(HOCRPage, self).__init__()
        self._raw = obj
        self._image = None
        self._pageno = None
        self._content_areas = None
        self._paragraphs = None
        for key, value in self._raw.items():
            attr_name = key.replace('ocr-', '', 1)
            if attr_name is 'careas':
                careas = []
                for item in list(value):
                    elem = HOCRElement(item)
                    careas.append(elem)
                self._content_areas = careas
            else:
                setattr(self, attr_name, value)

    @property
    def image(self):
        return self._image
    @image.setter
    def image(self, value):
        self._image = value

    @property
    def pageno(self):
        return self._pageno
    @pageno.setter
    def pageno(self, value):
        self._pageno = int(value)

    @property
    def content_areas(self):
        return self._content_areas

    @property
    def paragraphs(self):
        return self._paragraphs


class HOCRDocument(object):
    """Python representation of an hOCR document."""

    metadata_keys = ('capabilities', 'system')

    def __init__(self, obj=None, meta=None):
        super(HOCRDocument, self).__init__()
        self._raw = obj
        self._meta = meta if meta else HOCRMeta()
        self._pages = []
        if self._raw:
            for key,value in self._raw.items():
                attr_name = key.replace('ocr-', '', 1)
                if attr_name in HOCRDocument.metadata_keys:
                    setattr(self._meta, attr_name, value)
                else:
                    if attr_name is 'pages':
                        for p in list(value):
                            page = HOCRPage(p)
                            self._pages.append(page)
                    else:
                        setattr(self, attr_name, value)

    @property
    def meta(self):
        return self._meta
    @meta.setter
    def meta(self, value):
        if isinstance(value, HOCRMeta):
            self._meta = value
        elif isinstance(value, dict):
            self._meta = HOCRMeta(value)

    @property
    def pages(self):
        return self._pages
    @pages.setter
    def pages(self, value):
        self._pages = value

