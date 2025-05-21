from pathlib import Path

from listing_generator.application.filters import IncludeExtensionFilter, EmptyFilter


def test_extension_filter():
    input_data = [
        Path("abc"),
        Path("foo.bar"),
        Path("foo.bar.baz"),
        Path("hello.cs"),
        Path("hello abc.afs"),
        Path("main.py"),
        Path("hello/main.py"),
        Path("hello/world/main.py"),
    ]

    root_filter = EmptyFilter(input_data)
    filter = IncludeExtensionFilter(root_filter, included_extensions=[".py", ".bar"])
    out_data = filter.filter()
    expected = [
        Path("foo.bar"),
        Path("main.py"),
        Path("hello/main.py"),
        Path("hello/world/main.py"),
    ]

    assert out_data == expected
