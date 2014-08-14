from __future__ import (absolute_import, unicode_literals)

from shapely.geometry import Polygon, box

from hocrgeo.formatters.core import ShapelyFormatter

class WKFormatter(ShapelyFormatter):
    """Formats a HOCRParser document as well-known text"""

    @property
    def wkt(self):
        if self._polygons:
            return '\n'.join([p.wkt for p in self._polygons])
        return None

