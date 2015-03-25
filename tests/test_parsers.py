#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the `parsers` module.
"""
import os
from tempfile import TemporaryDirectory
import unittest
import webbrowser
from zipfile import ZipFile

from clitoolkit.parsers import ImmoScout24


temp_dir = TemporaryDirectory()


def setup_module():
    """Open the zip file with samples into a temp directory."""
    with ZipFile(os.path.join(os.path.dirname(__file__), 'immoscout_samples.zip')) as zip:
        zip.extractall(temp_dir.name)


def teardown_module():
    """Clean the temp directory."""
    temp_dir.cleanup()


class TestImmoScout24(unittest.TestCase):
    def test_extract_urls_string(self):
        obj = ImmoScout24(
            'http://forward.immobilienscout24.de/9004EXPXXUA/expose/79605539?PID=63188280'
            'http://www.immobilienscout24.de/expose/79605539?PID=63188280&ftc=9004EXPXXUA&_s_cclid=1423869828'
            'http://forward.immobilienscout24.de/9004EXPXXUA/expose/79573194?PID=63188280'
            'http://forward.immobilienscout24.de/9004EXPXXUA/expose/79564822?PID=63188280')
        assert len(obj.urls) == 3

    def test_extract_urls_list(self):
        obj = ImmoScout24([
            'http://forward.immobilienscout24.de/9004EXPXXUA/expose/79605539?PID=63188280',
            'http://www.immobilienscout24.de/expose/79564822?PID=63188280&ftc=9004EXPXXUA&_s_cclid=1423869828'])
        assert len(obj.urls) == 2


def load_file_into_string(partial_filename):
    """Load a sample HTML file into a string.

    :param partial_filename:
    :return:
    """
    full_name = os.path.join(temp_dir.name, partial_filename + '.html')
    with open(full_name) as fp:
        return fp.read()


def mock_immo_scout(monkeypatch, function_name):
    """Mock the Immobilien Scout class for test purposes.

    :param monkeypatch:
    :param function_name:
    :return:
    """

    def mockreturn(self, ad_url):
        return load_file_into_string(function_name)

    monkeypatch.setattr(ImmoScout24, 'download_html', mockreturn)
    monkeypatch.setattr(webbrowser, 'open', lambda x: None)
    return ImmoScout24('http://forward.immobilienscout24.de/9004EXPXXUA/expose/79605539?PID=63188280').parse()


def test_street_and_neighborhood(monkeypatch):
    """Full ad with street and neighborhood.

    :param monkeypatch:
    """
    ad = mock_immo_scout(monkeypatch, test_street_and_neighborhood.__name__)
    assert ad.full_address == 'Husemannstraße 5, 10435 Berlin'
    assert ad.found


def test_not_found(monkeypatch):
    """Ad not found.

    :param monkeypatch:
    """
    ad = mock_immo_scout(monkeypatch, test_not_found.__name__)
    assert ad.full_address == ''
    assert not ad.found


def test_no_street(monkeypatch):
    """Ad without street, only with neighborhood.

    :param monkeypatch:
    """
    ad = mock_immo_scout(monkeypatch, test_no_street.__name__)
    assert ad.full_address == '10555 Berlin'
    assert ad.found


if __name__ == '__main__':
    unittest.main()
