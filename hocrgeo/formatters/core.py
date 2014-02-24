from shapely.geometry import Polygon, box

from shapely import speedups

if speedups.available:
    speedups.enable()

class ShapelyFormatter:
    '''Formats a HOCRDocument into shapely geometry'''
    def __init__(self, hocr_document=None):
        if hocr_document:
            self.parse_hocr(hocr_document)

    def parse_hocr(self, hocr_document):
        '''
        Parse a hocr_document created by from hocrgeo.parsers.hocr.HOCRParser

        :param hocr_document: instance of hocrparser.document.
        '''

        def _extract_polys_from_feature_tree(polygons, root, feature_keys):
            def _poly_from_object(obj):
                bbox = obj.get('bbox', None)
                if bbox:
                    poly = box(bbox.get('x0'), bbox.get('y0'), bbox.get('x1'), bbox.get('y1'))
                    return poly
                return None

            features = root.get(feature_keys[0])
            for f in features:
                poly = _poly_from_object(f)
                polygons.append(poly)

                child_keys = feature_keys[1:]
                if child_keys:
                    _extract_polys_from_feature_tree(polygons, f, child_keys)

        self._polygons = []

        features = ('pages', 'careas', 'paragraphs', 'lines', 'words')

        _extract_polys_from_feature_tree(self._polygons, hocr_document, features)
