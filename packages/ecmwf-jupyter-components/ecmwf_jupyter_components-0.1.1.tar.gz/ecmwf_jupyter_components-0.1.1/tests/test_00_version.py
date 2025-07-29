import ecmwf.jupyter_components


def test_version() -> None:
    assert ecmwf.jupyter_components.__version__ != "999"
