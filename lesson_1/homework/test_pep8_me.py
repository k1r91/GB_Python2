# usage (in current directory: python3 -m pytest
import os
import pytest

from pep8_me import *

test_data1 = [('files/file2/', 'parts.md5', 'file2', 12),
             ('files/file1/', 'parts.md5', 'file1', 239)]


@pytest.mark.parametrize('files_dir, hash_file, outfile, expected', test_data1)
def test_glue_files(files_dir, hash_file, outfile, expected):
    assert glue_files(files_dir, hash_file, outfile) == expected

test_data2 = [('file2: PDF document, version 1.4', 'pdf'),
             ('file1: JPEG image data, JFIF standard 1.01, '
              'resolution (DPI), density 72x72, segment '
              'length 16, progressive, precision 8, 1280x853, frames 3', 'jpeg')]


@pytest.mark.parametrize('got, expected', test_data2)
def test_get_file_extension(got, expected):
    assert get_file_extension(got) == expected

test_data3 = [('file1.jpeg', 1024, 239), ('file2.pdf', 1024, 12)]


@pytest.mark.parametrize('file_name, piece_size, expected', test_data3)
def test_part_file(file_name, piece_size, expected):
    assert part_file(file_name, piece_size) == expected

test_data4 = [('/test1.txt', '.', '10KB', 10240),
              ("/test2.txt", ".", '1024', 1024),
              ("/test11.txt", ".", '2MB', 2097152),
              ("/test21.txt", ".", '1B', 1)]


@pytest.mark.parametrize('namef, dir_name, size, expected', test_data4)
def test_create_file(namef, dir_name, size, expected):
    assert create_file(namef, dir_name, size) == expected

test_data5 = [('/test25.txt', 'test', '2B')]


@pytest.mark.parametrize('namef, dir_name, size', test_data5)
def test_create_file_exists(namef, dir_name, size):
    create_file(namef, dir_name, size)
    assert os.path.exists(os.path.join(dir_name, namef[1:]))