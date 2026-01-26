from __future__ import annotations
import pytest
import tempfile
from pathlib import Path
import zipfile

from pmp_manip.otility.file import (
    read_all_files_of_zip, read_file_text, write_file_text,
    delete_file, delete_directory, create_zip_file, file_exists
)
from pmp_manip.otility.errors import (
    MANIPO_FileNotFoundError, MANIPO_FailedFileWriteError, MANIPO_FailedFileDeleteError, MANIPO_FailedFileReadError
)


class TestReadFileText:
    """Test read_file_text function."""
    
    def test_read_file_text_basic(self):
        """Test reading text from a file."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("Hello, World!")
            temp_path = f.name
        
        try:
            content = read_file_text(temp_path)
            assert content == "Hello, World!"
        finally:
            Path(temp_path).unlink()
    
    def test_read_file_text_with_pathlib(self):
        """Test reading text file using pathlib.Path."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("Test content")
            temp_path = Path(f.name)
        
        try:
            content = read_file_text(temp_path)
            assert content == "Test content"
        finally:
            temp_path.unlink()
    
    def test_read_file_text_nonexistent(self):
        """Test reading nonexistent file raises error."""
        with pytest.raises(MANIPO_FileNotFoundError):
            read_file_text("/nonexistent/path/file.txt")
    
    def test_read_file_text_encoding(self):
        """Test reading file with different encoding."""
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False, suffix=".txt") as f:
            f.write("UTF-8 content: café")
            temp_path = f.name
        
        try:
            content = read_file_text(temp_path, encoding="utf-8")
            assert "café" in content
        finally:
            Path(temp_path).unlink()


class TestWriteFileText:
    """Test write_file_text function."""
    
    def test_write_file_text_basic(self):
        """Test writing text to a file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_path = Path(tmpdir) / "test.txt"
            write_file_text(str(temp_path), "Test content")
            assert temp_path.read_text() == "Test content"
    
    def test_write_file_text_with_pathlib(self):
        """Test writing using pathlib.Path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_path = Path(tmpdir) / "test.txt"
            write_file_text(temp_path, "Pathlib content")
            assert temp_path.read_text() == "Pathlib content"
    
    def test_write_file_text_creates_file(self):
        """Test that write_file_text creates the file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_path = Path(tmpdir) / "new_file.txt"
            write_file_text(temp_path, "New file content")
            assert temp_path.exists()
            assert temp_path.read_text() == "New file content"
    
    def test_write_file_text_overwrite(self):
        """Test overwriting existing file."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("Old content")
            temp_path = f.name
        
        try:
            write_file_text(temp_path, "New content")
            assert Path(temp_path).read_text() == "New content"
        finally:
            Path(temp_path).unlink()
    
    def test_write_file_text_encoding(self):
        """Test writing with specific encoding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_path = Path(tmpdir) / "utf8_test.txt"
            write_file_text(temp_path, "UTF-8: café", encoding="utf-8")
            content = temp_path.read_text(encoding="utf-8")
            assert "café" in content


class TestDeleteFile:
    """Test delete_file function."""
    
    def test_delete_file_basic(self):
        """Test deleting an existing file."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        assert Path(temp_path).exists()
        delete_file(temp_path)
        assert not Path(temp_path).exists()
    
    def test_delete_file_with_pathlib(self):
        """Test deleting file using pathlib.Path."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = Path(f.name)
        
        assert temp_path.exists()
        delete_file(temp_path)
        assert not temp_path.exists()
    
    def test_delete_file_nonexistent(self):
        """Test deleting nonexistent file raises error."""
        with pytest.raises(MANIPO_FailedFileDeleteError):
            delete_file("/nonexistent/path/file.txt")


class TestDeleteDirectory:
    """Test delete_directory function."""
    
    def test_delete_directory_basic(self):
        """Test deleting an empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir) / "test_subdir"
            test_dir.mkdir()
            assert test_dir.exists()
            
            delete_directory(str(test_dir))
            assert not test_dir.exists()
    
    def test_delete_directory_with_contents(self):
        """Test deleting directory with files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir) / "test_dir"
            test_dir.mkdir()
            (test_dir / "file1.txt").write_text("content1")
            (test_dir / "file2.txt").write_text("content2")
            
            delete_directory(test_dir)
            assert not test_dir.exists()
    
    def test_delete_directory_with_pathlib(self):
        """Test deleting directory using pathlib.Path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir) / "subdir"
            test_dir.mkdir()
            
            delete_directory(test_dir)
            assert not test_dir.exists()
    
    def test_delete_directory_nonexistent(self):
        """Test deleting nonexistent directory raises error."""
        with pytest.raises(MANIPO_FailedFileDeleteError):
            delete_directory("/nonexistent/path/dir")


class TestCreateZipFile:
    """Test create_zip_file function."""
    
    def test_create_zip_file_basic(self):
        """Test creating a basic ZIP file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = Path(tmpdir) / "test.zip"
            contents = {
                "file1.txt": b"Content 1",
                "file2.txt": b"Content 2",
            }
            
            create_zip_file(str(zip_path), contents)
            assert zip_path.exists()
            
            # Verify contents
            with zipfile.ZipFile(zip_path, "r") as z:
                assert z.read("file1.txt") == b"Content 1"
                assert z.read("file2.txt") == b"Content 2"
    
    def test_create_zip_file_with_pathlib(self):
        """Test creating ZIP file using pathlib.Path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = Path(tmpdir) / "test.zip"
            contents = {"test.txt": b"Test content"}
            
            create_zip_file(zip_path, contents)
            assert zip_path.exists()
            
            with zipfile.ZipFile(zip_path, "r") as z:
                assert z.read("test.txt") == b"Test content"
    
    def test_create_zip_file_empty(self):
        """Test creating an empty ZIP file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = Path(tmpdir) / "empty.zip"
            create_zip_file(zip_path, {})
            assert zip_path.exists()
            
            with zipfile.ZipFile(zip_path, "r") as z:
                assert len(z.namelist()) == 0
    
    def test_create_zip_file_nested_paths(self):
        """Test creating ZIP with nested file paths."""
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = Path(tmpdir) / "nested.zip"
            contents = {
                "dir1/file1.txt": b"Nested content 1",
                "dir1/dir2/file2.txt": b"Nested content 2",
            }
            
            create_zip_file(zip_path, contents)
            
            with zipfile.ZipFile(zip_path, "r") as z:
                assert z.read("dir1/file1.txt") == b"Nested content 1"
                assert z.read("dir1/dir2/file2.txt") == b"Nested content 2"


class TestReadAllFilesOfZip:
    """Test read_all_files_of_zip function."""
    
    def test_read_all_files_of_zip_basic(self):
        """Test reading all files from a ZIP."""
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = Path(tmpdir) / "test.zip"
            contents = {
                "file1.txt": b"Content 1",
                "file2.txt": b"Content 2",
                "file3.txt": b"Content 3",
            }
            create_zip_file(zip_path, contents)
            
            result = read_all_files_of_zip(str(zip_path))
            assert result == contents
    
    def test_read_all_files_of_zip_with_pathlib(self):
        """Test reading ZIP using pathlib.Path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = Path(tmpdir) / "test.zip"
            contents = {"test.txt": b"Test"}
            create_zip_file(zip_path, contents)
            
            result = read_all_files_of_zip(zip_path)
            assert result == contents
    
    def test_read_all_files_of_zip_nonexistent(self):
        """Test reading nonexistent ZIP file raises error."""
        with pytest.raises(MANIPO_FileNotFoundError):
            read_all_files_of_zip("/nonexistent/path/file.zip")
    
    def test_read_all_files_of_zip_empty(self):
        """Test reading empty ZIP file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = Path(tmpdir) / "empty.zip"
            create_zip_file(zip_path, {})
            
            result = read_all_files_of_zip(zip_path)
            assert result == {}


class TestFileExists:
    """Test file_exists function."""
    
    def test_file_exists_true(self):
        """Test file_exists returns True for existing file."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            assert file_exists(temp_path) is True
        finally:
            Path(temp_path).unlink()
    
    def test_file_exists_false(self):
        """Test file_exists returns False for nonexistent file."""
        assert file_exists("/nonexistent/path/file.txt") is False
    
    def test_file_exists_with_pathlib(self):
        """Test file_exists with pathlib.Path."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = Path(f.name)
        
        try:
            assert file_exists(temp_path) is True
        finally:
            temp_path.unlink()
    
    def test_file_exists_directory(self):
        """Test file_exists with directory path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            assert file_exists(tmpdir) is True
