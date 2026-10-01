import common


def test_common_package_importable() -> None:
    assert common.__doc__ is not None
