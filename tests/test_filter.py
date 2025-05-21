from pathlib import Path
import pytest

from listing_generator.application.filters import (
    ExcludeExtensionFilter,
    IncludeExtensionFilter,
    EmptyFilter,
    InlcudeFileNameFilter,
    ExcludeFileNameFilter,
)


@pytest.fixture
def file_list():
    return [
        Path(".gitignore"),
        Path("src/.gitignore"),
        Path("abc/def/foo.pyc"),
        Path("abc"),
        Path("foo.bar"),
        Path("foo.bar.baz"),
        Path("hello.cs"),
        Path("__init__.py"),
        Path("hello/__init__.py"),
        Path("hello/world/__init__.py"),
        Path("this.py"),
        Path("hello/this.py"),
        Path("hello/world/this.py"),
        Path("hello abc.afs"),
        Path("main.py"),
        Path("hello/main.py"),
        Path("hello/world/main.py"),
    ]


def test_empty_filter(file_list):
    assert EmptyFilter(file_list).filter() == file_list


def test_include_extension_filter(file_list):
    root_filter = EmptyFilter(file_list)
    filter = IncludeExtensionFilter(root_filter, included_extensions=[".py", ".bar"])
    out_data = filter.filter()
    expected = [
        Path("foo.bar"),
        Path("__init__.py"),
        Path("hello/__init__.py"),
        Path("hello/world/__init__.py"),
        Path("this.py"),
        Path("hello/this.py"),
        Path("hello/world/this.py"),
        Path("main.py"),
        Path("hello/main.py"),
        Path("hello/world/main.py"),
    ]

    assert set(out_data) == set(expected)


def test_exclude_extension_filter(file_list):
    root_filter = EmptyFilter(file_list)
    filter = ExcludeExtensionFilter(root_filter, excluded_extensions=[".py", ".bar"])
    out_data = filter.filter()
    expected = [
        Path(".gitignore"),
        Path("src/.gitignore"),
        Path("abc/def/foo.pyc"),
        Path("abc"),
        Path("foo.bar.baz"),
        Path("hello.cs"),
        Path("hello abc.afs"),
    ]

    assert set(out_data) == set(expected)


def test_inlude_file_name_filter(file_list):
    root_filter = EmptyFilter(file_list)
    filter = InlcudeFileNameFilter(
        root_filter, included_filenames=["main.py", ".gitignore", "foo.bar"]
    )
    out_data = filter.filter()
    expected = [
        Path(".gitignore"),
        Path("src/.gitignore"),
        Path("foo.bar"),
        Path("main.py"),
        Path("hello/main.py"),
        Path("hello/world/main.py"),
    ]
    assert set(out_data) == set(expected)


def test_exclude_file_name_filter(file_list):
    root_filter = EmptyFilter(file_list)
    filter = ExcludeFileNameFilter(
        root_filter, excluded_filenames=["main.py", ".gitignore", "foo.bar"]
    )
    out_data = filter.filter()
    expected = [
        Path("abc/def/foo.pyc"),
        Path("abc"),
        Path("foo.bar.baz"),
        Path("__init__.py"),
        Path("hello/__init__.py"),
        Path("hello/world/__init__.py"),
        Path("this.py"),
        Path("hello/this.py"),
        Path("hello/world/this.py"),
        Path("hello.cs"),
        Path("hello abc.afs"),
    ]

    assert set(out_data) == set(expected)


def test_inlude_all_name_filter(file_list):
    root_filter = EmptyFilter(file_list)
    filter = InlcudeFileNameFilter(root_filter, included_filenames=["*"])
    out_data = filter.filter()
    assert set(file_list) == set(out_data)


def test_include_all_extension(file_list):
    root_filter = EmptyFilter(file_list)
    filter = IncludeExtensionFilter(root_filter, included_extensions=["*"])
    out_data = filter.filter()
    assert set(file_list) == set(out_data)


def test_nesting_filter(file_list):
    root_filter = EmptyFilter(file_list)
    filter = ExcludeFileNameFilter(
        IncludeExtensionFilter(root_filter, included_extensions=[".py"]),
        excluded_filenames=["__init__.py"],
    )
    expected = [
        Path("this.py"),
        Path("hello/this.py"),
        Path("hello/world/this.py"),
        Path("main.py"),
        Path("hello/main.py"),
        Path("hello/world/main.py"),
    ]
    out_data = filter.filter()

    assert set(out_data) == set(expected)
