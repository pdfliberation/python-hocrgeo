from __future__ import unicode_literals

from io import TextIOBase

try:
    TextIOBase = file
except NameError:
  pass # Forward compatibility with Py3k

from bs4 import BeautifulSoup
import re

import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

class HOCRParser:
    """
        Parse hOCR documents

        Takes either a file-like object or a filename
    """

    def __init__(self, fs=None):
        '''
        Initializes a HOCRParser

        :param input: Optional file-like object to read or hOCR as a string.

        '''
        self._rawdata = None
        self._bboxreg = re.compile(r'bbox (?P<x0>\d+) (?P<y0>\d+) (?P<x1>\d+) (?P<y1>\d+)')
        self._doc = None

        if fs:
            self._rawdata = self._get_data_string(fs)

    def _get_data_string(self, fs):
        if isinstance(fs, TextIOBase):
            return fs.read()
        else:
            try:
                if isinstance(fs, unicode):
                    return fs
                else:
                    clean_fs = unicode(fs, encoding='utf-8')
                    if isinstance(clean_fs, unicode):
                        return clean_fs
            except NameError:
                if isinstance(fs, str):
                    return fs
        raise TypeError('Input is not a readable string or file object')

    def load(self, fsfile):
        '''Load a file from a filepath or a file-like instance'''
        fp = None
        if isinstance(fsfile, str):
            try:
                fp = open(fsfile, 'rb')
            except IOError as e:
                raise e
        elif isinstance(fs, TextIOBase):
            fp = fsfile
        else:
            raise TypeError('argument must be a file object or a valid filepath')

        self._rawdata = self._get_data_string(fp)

    def loads(self, fs):
        if isinstance(fs, str):
            self._rawdata = self._get_data_string(fs)
        else:
            raise TypeError('argument must be a string or unicode instance')

    @property
    def document(self):
        '''Parsed HOCR document'''
        return self._doc

    def parse(self):
        '''Parse hOCR document into a python object.'''

        def _extract_objects_from_element(root, el_name, el_class):
            nodes = root.find_all(el_name, el_class)
            objects = []
            for n in nodes:
                obj = _extract_features(n)
                objects.append(obj)

            return (nodes, objects)

        def _extract_bbox(fs_str):
            '''Regular expression matching on a fs_str that should contain hOCR bbox coordinates.'''
            match = self._bboxreg.search(fs_str)
            if match:
                match_grp = match.groupdict()
                for key,value in match_grp.items():
                    match_grp[key] = int(value)
                return match_grp
            return None

        def _extract_features(element):
            '''Extract basic hOCR features from a given element.'''
            features = {}
            features['id'] = element.get('id')
            features['bbox'] = _extract_bbox(element.get('title', ''))
            return features

        if not self._rawdata:
            raise Exception('No fsfile specified. You must specify an fs file when instantiating or as an argument to the parse method')

        soup = BeautifulSoup(self._rawdata, "lxml")

        self._doc = {}

        # Extract ocr system metadata
        ocr_system = soup.find('meta', attrs={'name': 'ocr-system'})
        self._doc['ocr-system'] = ocr_system.get('content', None) if ocr_system else None

        # Extract capabilities
        ocr_capabilities = soup.find('meta', attrs={'name': 'ocr-capabilities'})
        self._doc['ocr-capabilities'] = ocr_capabilities.get('content', ' ').split(' ') if ocr_capabilities else None

        page_nodes, page_objects = _extract_objects_from_element(soup, 'div', 'ocr_page')
        page_tup = list(zip(page_nodes, page_objects))
        logger.info('Found {0} page(s)'.format(len(page_tup)))

        for page_node, page_obj in page_tup:
            carea_nodes, carea_objects = _extract_objects_from_element(page_node, 'div', 'ocr_carea')
            careas_tup = list(zip(carea_nodes, carea_objects))

            for c_node, c_obj in careas_tup:
                para_nodes, para_objects = _extract_objects_from_element(c_node, 'p', 'ocr_par')
                paras_tup = list(zip(para_nodes, para_objects))

                for para_node, para_obj in paras_tup:
                    line_nodes, line_objects = _extract_objects_from_element(para_node, 'span', 'ocr_line')
                    lines_tup = list(zip(line_nodes, line_objects))

                    for l_node, l_obj in lines_tup:
                        word_nodes, word_objects = _extract_objects_from_element(l_node, 'span', 'ocrx_word')
                        words_tup = list(zip(word_nodes, word_objects))

                        for w_node, w_obj in words_tup:
                            word_str = w_node.get_text(strip=True)
                            if word_str:
                                logger.info(word_str)
                                w_obj['text'] = w_node.get_text()
                        l_obj['words'] = word_objects

                    para_obj['lines'] = line_objects

                c_obj['paragraphs'] = para_objects

            page_obj['careas'] = carea_objects

        self._doc['pages'] = page_objects




