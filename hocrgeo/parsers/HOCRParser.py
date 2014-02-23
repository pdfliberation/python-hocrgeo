from bs4 import BeautifulSoup
import re

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
    def __init__(self, input=None):
        self.input = input
        self.rawdata = None
        self.data = None
        self._bboxreg = re.compile(r'bbox (?P<x0>\d+) (?P<y0>\d+) (?P<x1>\d+) (?P<y1>\d+)')
        if self.input:
            self.load_file()

    def load_file(self, input=None):
        if input:
            self.input = input
        fp = None
        if isinstance(self.input, basestring):
            try:
                fp = open(self.input, 'rb')
            except IOError, e:
                raise e
        else:
            fp = input

        self.rawdata = fp.read()

    def _extract_bbox(self, input_str):
        match = self._bboxreg.search(input_str)
        if match:
            return match.groupdict()
        return None

    def _extract_features(self, elem):
        features = {}
        features['id'] = elem.get('id')
        features['bbox'] = self._extract_bbox(elem.get('title', ''))
        return features

    def parse(self):
        if not self.rawdata:
            self.load_file()

        soup = BeautifulSoup(self.rawdata, "lxml")

        obj = {}

        # Extract ocr system metadata
        ocr_system = soup.find('meta', attrs={'name':'ocr-system'})
        obj['ocr-system'] = ocr_system.get('content', None) if ocr_system else None

        # Extract capabilities
        ocr_capabilities = soup.find('meta', attrs={'name':'ocr-capabilities'})
        obj['ocr-capabilities'] = ocr_capabilities.get('content', ' ').split(' ')

        all_pages = soup.find_all('div', PAGE)
        n_pages = len(all_pages)
        pages = []

        logger.info('Found {0} page(s)'.format(n_pages))

        for page in all_pages:
            page_obj = self._extract_features(page)
            page_careas = page.find_all('div', CAREA)
            page_obj['careas'] = []

        for carea in page_careas:
            logger.info('Adding a carea')
            carea_obj = self._extract_features(carea)
            page_obj['careas'].append(carea_obj)


            logger.info('Adding a page')
            pages.append(page_obj)

        obj['pages'] = pages
        self.data = obj


