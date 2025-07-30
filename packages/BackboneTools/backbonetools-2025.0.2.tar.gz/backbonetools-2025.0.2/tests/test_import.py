from importlib.util import find_spec


def test_import():
    # Check if the package can be imported
    assert find_spec("backbonetools") is not None, "Package 'backbonetools' not found"


def test_io_import():
    # Check if the submodules can be imported
    assert (
        find_spec("backbonetools.io") is not None
    ), "Submodule 'io' not found in 'backbonetools'"


def test_sub_import():
    from backbonetools.io import BackboneInput, BackboneResult

    assert True
