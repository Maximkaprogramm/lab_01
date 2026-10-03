import subprocess


def test_help():
    result = subprocess.run(
        ["python3", "-m", "toolkit", "--help"],
        capture_output=True,
        text=True,
        check=False
    )
    assert result.returncode == 0
    assert "usage:" in result.stdout
    assert "calc" in result.stdout
    assert "convert" in result.stdout



def test_calc_command():
    result = subprocess.run(
        ["python3", "-m", "toolkit", "calc", "10 + 5"],
        capture_output=True,
        text=True,
        check=False
    )
    assert result.returncode == 0
    assert "15" in result.stdout

def test_convert_command():
    result = subprocess.run(
        ["python3", "-m", "toolkit", "convert", "1500", "--from", "g", "--to", "kg"],
        capture_output=True,
        text=True,
        check=False
    )
    assert result.returncode == 0
    assert "1" in result.stdout


def test_convert_incompatible_units():
    result = subprocess.run(
        ["python3", "-m", "toolkit", "convert", "123", "--from", "kg", "--to", "m"],
        capture_output=True,
        text=True,
        check=False
    )
    assert result.returncode == 2
    assert "incompatible units" in result.stderr