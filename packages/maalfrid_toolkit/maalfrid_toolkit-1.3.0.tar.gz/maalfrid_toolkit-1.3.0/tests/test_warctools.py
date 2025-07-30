import os
import pytest
import maalfrid_toolkit.warc_tools as warc_tools

test_file_path = os.path.join(os.path.dirname(__file__), "testfiles")

@pytest.fixture
def load_html_warc():
    with open(os.path.join(test_file_path, "html.warc.gz"), "rb") as stream:
        yield stream

@pytest.fixture
def load_pdf_warc():
    with open(os.path.join(test_file_path, "pdf.warc.gz"), "rb") as stream:
        yield stream

@pytest.fixture
def load_docx_warc():
    with open(os.path.join(test_file_path, "docx.warc.gz"), "rb") as stream:
        yield stream

def test_warc_filter(load_html_warc):
    records = [record for record in warc_tools.filter_warc(load_html_warc, content_types=["text/html"])]
    assert len(records) == 1

def test_maalfrid_record_init(load_html_warc):
    for record in warc_tools.filter_warc(load_html_warc, content_types=["text/html"]):
        maalfrid_record = warc_tools.convert_to_maalfrid_record(record, warc_file_name="testfiles/html.warc.gz")
        assert maalfrid_record.content_type.startswith("text/html")

def test_maalfrid_record_ft_extract_html(load_html_warc):
    for record in warc_tools.filter_warc(load_html_warc, content_types=["text/html"]):
        maalfrid_record = warc_tools.convert_to_maalfrid_record(record, warc_file_name="testfiles/html.warc.gz")
        maalfrid_record.extract_full_text()
        assert maalfrid_record.full_text[2].startswith("Dataa vart samla inn") == True

def test_maalfrid_record_ft_extract_pdf(load_pdf_warc):
    for record in warc_tools.filter_warc(load_pdf_warc, content_types=["application/pdf"]):
        maalfrid_record = warc_tools.convert_to_maalfrid_record(record, warc_file_name="testfiles/pdf.warc.gz")
        maalfrid_record.extract_full_text()
        assert maalfrid_record.full_text[2].startswith("The corpus") == True

def test_maalfrid_record_ft_extract_doc(load_docx_warc):
    for record in warc_tools.filter_warc(load_docx_warc, content_types=['application/vnd.openxmlformats-officedocument.wordprocessingml.document']):
        maalfrid_record = warc_tools.convert_to_maalfrid_record(record, warc_file_name="testfiles/docx.warc.gz")
        maalfrid_record.extract_full_text()
        assert maalfrid_record.full_text[2].startswith("(2019–2020)") == True

def test_maalfrid_record_get_simhash(load_html_warc):
    for record in warc_tools.filter_warc(load_html_warc, content_types=["text/html"]):
        maalfrid_record = warc_tools.convert_to_maalfrid_record(record, warc_file_name="testfiles/html.warc.gz", calculate_simhash=True)
        maalfrid_record.extract_full_text()
        assert maalfrid_record.simhash_value == 11772415046536287686
