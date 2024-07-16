from . import build

def test_sassDoesNothingForEmptyList():
    out = [o for o in build.parseSassFiles([])]
    assert len(out) == 0

