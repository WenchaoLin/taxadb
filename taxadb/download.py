#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tqdm import tqdm

import shutil
import logging
import tarfile
import requests


def ncbi(path, filename, base_url='https://ftp.ncbi.nlm.nih.gov/'):
    """newer download function using requests

    EXPERIMENTAL

    Arguments:
        url: a string encoding a valid url
    """
    logger = logging.getLogger(__name__)

    url = base_url + path + filename
    request = requests.get(url, stream=True)

    logger.info('Downloading %s' % filename)
    total_size = int(request.headers.get('content-length', 0))
    chunk_size = 1024
    written = 0
    with open(filename, 'wb') as f:
        for chunk in tqdm(request.iter_content(chunk_size=chunk_size),
                          total=total_size/chunk_size,
                          unit='KB', unit_scale=True):
            if chunk:
                f.write(chunk)
                f.flush()


def unpack(filename):
    """uncompress a tar.gz archive
    """
    logger = logging.getLogger(__name__)

    logger.info('Unpacking %s' % filename)
    with tarfile.open(filename, "r:gz") as archive:
        archive.extractall()
        archive.close()


# ncbi(path='pub/taxonomy/', filename='taxdump.tar.gz')