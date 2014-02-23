from bs4 import BeautifulSoup
import re

from hocrgeo.models.hocr import HOCRDocument

import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

PAGE = 'ocr_page'
CAREA = 'ocr_carea'
PAR = 'ocr_par'
LINE = 'ocr_line'
WORD = 'ocrx_word'

class HOCRParser:
    """
        Parse hOCR documents

        Takes either a file-like object or a filename
    """

    def __init__(self, inputfile=None):
        '''
        Initializes a HOCRParser

        :param inputfile: Optional file path or file-like object to use.

        '''
        self._rawdata = None
        self._bboxreg = re.compile(r'bbox (?P<x0>\d+) (?P<y0>\d+) (?P<x1>\d+) (?P<y1>\d+)')
        self._doc = None

        if inputfile:
            self.load_file(inputfile)

    def load_file(self, inputfile):
        '''Load a file from a filepath or a file-like instance'''
        fp = None
        if isinstance(inputfile, basestring):
            try:
                fp = open(inputfile, 'rb')
            except IOError, e:
                raise e
        else:
            fp = inputfile

        self._rawdata = fp.read()

    @property
    def document(self):
        return self._doc

    def parse(self, inputfile=None):
        '''Parse hOCR document into a python object.'''
        if inputfile:
            self.load_file(inputfile)
        elif not self._rawdata:
            raise Exception('No inputfile specified. You must specify an input file when instantiating or as an argument to the parse method')

        soup = BeautifulSoup(self._rawdata, "lxml")

        self._doc = HOCRDocument()

        # Extract ocr system metadata
        ocr_system = soup.find('meta', attrs={'name': 'ocr-system'})
        self._doc.add('ocr-system', ocr_system.get('content', None) if ocr_system else None)

        # Extract capabilities
        ocr_capabilities = soup.find('meta', attrs={'name': 'ocr-capabilities'})
        self._doc.add('ocr-capabilities', ocr_capabilities.get('content', ' ').split(' '))

        all_pages = soup.find_all('div', PAGE)
        logger.info('Found {0} page(s)'.format(len(all_pages)))

        for page in all_pages:
            page_obj = self._extract_features(page)
            # page_careas = page.find_all('div', CAREA)
            logger.info('Adding a page')
            self._doc.add_page(page_obj)

        # all_careas = soup.find_all('div', CAREA)
        # logger.info('Found {0} carea(s)'.format(len(all_careas)))

        # for carea in all_careas:
        #     carea_obj = self._extract_features(carea)
        #     logger.info('Adding a carea: {0}'.format(carea_obj))
        #     # page_obj['careas'].append(carea_obj)
        #     parent_obj = carea.parent.get('id', None)
        #     logger.info(parent_obj)

    def _extract_bbox(self, input_str):
        '''Regular expression matching on a input_str that should contain hOCR bbox coordinates.'''
        match = self._bboxreg.search(input_str)
        if match:
            return match.groupdict()
        return None

    def _extract_features(self, element):
        '''Extract basic hOCR features from a given element.'''
        features = {}
        features['id'] = element.get('id')
        features['bbox'] = self._extract_bbox(element.get('title', ''))
        return features

