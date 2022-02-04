import feedparser
import os
import pprint
import subprocess
import tempfile
from pathlib import Path


def test_basic():
    with tempfile.TemporaryDirectory() as tmpdir:
        site_dir = Path(tmpdir) / 'test_basic'

        result = subprocess.run([
            "mkdocs", "build",
            "--config-file", Path(__file__).parent / "fixtures/basic/mkdocs.yml",
            "--site-dir", site_dir,
            "--clean",
            # "--verbose",
        ])

        assert result.returncode == 0
        assert os.path.isfile(site_dir / 'index.html')
        assert os.path.isfile(site_dir / 'atom.xml')
        
        atom = feedparser.parse(site_dir / 'atom.xml')
        #pprint.pprint(atom)

    assert len(atom['entries']) == 1
    assert atom['entries'][0]['title'] == 'Test'
    assert atom['entries'][0]['updated'] == '2022-01-30T12:00:00+09:00'
    assert atom['entries'][0]['summary'] == '<h1>Test page</h1>'
