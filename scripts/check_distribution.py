"""Check that both archives contain the message-count API and their licenses."""

import tarfile
import tomllib
import zipfile
from email.parser import BytesParser
from hashlib import sha256
from pathlib import Path

project = tomllib.loads(Path("pyproject.toml").read_text())["project"]
version = project["version"]
expected = {
    "pyelternportal/counts.py",
}
archives = sorted(Path("dist").glob("*.whl")) + sorted(Path("dist").glob("*.tar.gz"))
assert len(archives) == 2, "Expected exactly one wheel and one source distribution"
for archive in archives:
    assert version in archive.name
    if archive.suffix == ".whl":
        with zipfile.ZipFile(archive) as wheel:
            names = wheel.namelist()
            metadata = BytesParser().parsebytes(
                wheel.read(next(name for name in names if name.endswith("/METADATA")))
            )
            assert metadata["Version"] == version
            assert metadata["Name"] == project["name"]
            assert expected <= set(names)
            for name in expected:
                assert wheel.read(name) == (Path("src") / name).read_bytes()
            assert any(name.endswith("/licenses/LICENSE.extensions") for name in names)
            assert any(name.endswith("/licenses/LICENSE") for name in names)
    else:
        with tarfile.open(archive) as source:
            names = source.getnames()
            root = names[0].split("/")[0]
            for name in expected:
                file = source.extractfile(f"{root}/src/{name}")
                assert (
                    file is not None
                    and file.read() == (Path("src") / name).read_bytes()
                )
            assert f"{root}/LICENSE.extensions" in names
            assert f"{root}/LICENSE" in names
            assert f"{root}/tests/test_counts.py" in names
            assert f"{root}/scripts/check_distribution.py" in names
    print(f"{sha256(archive.read_bytes()).hexdigest()}  {archive.name}")
