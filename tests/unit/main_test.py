import pytest
from manage import *


def test_source_type_url():
    sypter = Sypter("https://www.google.com")
    assert sypter._get_source_type() == 'url'


def test_source_type_html():
    sypter = Sypter("<html></html>")
    assert sypter._get_source_type() == 'html'


def test_source_type_file():
    import os
    # tests root path
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(root_path, 'example.html')
    sypter = Sypter(path)
    assert sypter._get_source_type() == 'file'


def test_if_exists_by_class():
    sypter = Sypter('https://www.w3schools.com/html/tryit.asp?filename=tryhtml_id_css')
    assert sypter.if_exists_by_class("w3-border")


def test_if_exists_by_class_with_number():
    sypter = Sypter('https://www.w3schools.com/html/tryit.asp?filename=tryhtml_id_css')
    assert sypter.if_exists_by_class("w3-border", number=1)


def test_if_exists_by_class_with_min_num():
    sypter = Sypter('https://www.w3schools.com/html/tryit.asp?filename=tryhtml_id_css')
    assert sypter.if_exists_by_class("w3-border", min_num=1)


def test_if_exists_by_class_with_max_num():
    sypter = Sypter('https://www.w3schools.com/html/tryit.asp?filename=tryhtml_id_css')
    assert sypter.if_exists_by_class("w3-border", max_num=1)


def test_if_exists_by_class_with_min_num_and_max_num():
    sypter = Sypter('https://www.w3schools.com/html/tryit.asp?filename=tryhtml_id_css')
    assert sypter.if_exists_by_class("w3-border", min_num=1, max_num=1)


def test_if_exists_by_class_with_min_num_and_max_num_and_number():
    sypter = Sypter('https://www.w3schools.com/html/tryit.asp?filename=tryhtml_id_css')
    assert sypter.if_exists_by_class("w3-border", min_num=1, max_num=1, number=1)


def test_if_exists_by_class_with_min_num_and_max_num_and_number_and_not_exists():
    sypter = Sypter('https://www.w3schools.com/html/tryit.asp?filename=tryhtml_id_css')
    assert not sypter.if_exists_by_class("w3-border2", min_num=1, max_num=1, number=2)


