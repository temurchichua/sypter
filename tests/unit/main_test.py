def test_source_type_url(sypter):
    sypter.process_source("https://www.google.com")
    assert sypter.source_type == 'url'


def test_source_type_html(sypter):
    sypter.process_source("<html></html>")
    assert sypter.source_type == 'html'


def test_source_type_file(sypter):
    import os
    # tests root path
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(root_path, 'example.html')
    sypter.process_source(path)
    assert sypter.source_type == 'file'


def test_by_class(sypter):
    sypter.process_source('https://www.w3schools.com/html/tryit.asp?filename=tryhtml_id_css')
    assert sypter.test("w3-border", "class")


def test_by_class_and_number(sypter):
    sypter.process_source('https://www.w3schools.com/html/tryit.asp?filename=tryhtml_id_css')
    assert not sypter.test("w3-border2", "class", numeric_value=2)


def test_by_id(sypter):
    sypter.process_source('<div id="id01" class="this-is-class">some text</div>')
    assert sypter.test("id01", 'id')


def test_by_class_2(sypter):
    sypter.process_source('<div id="id01" class="this-is-class">some text</div>')
    assert sypter.test("this-is-class", 'class')


def test_by_id_and_attribute(sypter):
    sypter.process_source('<div id="id01" class="this-is-class" custom="Custom Attr">some text</div>')
    assert sypter.test("id01", "id", attribute_tests={'custom': 'Custom Attr'})


def test_by_id_and_attribute2(sypter):
    sypter.process_source('<div id="id01" class="this-is-class" custom="Custom Attr">some text</div>')
    assert not sypter.test("id01", "id", attribute_tests={'custom2': 'Custom Attr'})
