from src.sfchecks.tools import file


def test_read(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("test")
    text = file.read(file_path)
    assert text == "test"
