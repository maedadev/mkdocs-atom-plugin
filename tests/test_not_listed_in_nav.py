import feedparser
import os
import pprint
import subprocess
import tempfile
from pathlib import Path


def test_not_listed_in_nav():
    with tempfile.TemporaryDirectory() as tmpdir:
        site_dir = Path(tmpdir) / 'test_not_listed_in_nav'

        result = subprocess.run([
            "mkdocs", "build",
            "--config-file", Path(__file__).parent / "fixtures/not_listed_in_nav/mkdocs.yml",
            "--site-dir", site_dir,
            "--clean",
            #"--verbose",
        ])

        assert result.returncode == 0
        assert os.path.isfile(site_dir / 'index.html')
        assert os.path.isfile(site_dir / 'atom.xml')
        
        atom = feedparser.parse(site_dir / 'atom.xml')
        pprint.pprint(atom)

    assert len(atom['entries']) == 2
    assert atom['entries'][0]['title'] == 'About'
    assert atom['entries'][0]['updated'] == '2022-02-03T11:00:00+0000'
    assert atom['entries'][0]['summary'] == '<h1>About this site</h1>'
