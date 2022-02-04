import feedparser
import os
import pprint
import subprocess
import tempfile
from pathlib import Path


def test_multiple_authors():
    with tempfile.TemporaryDirectory() as tmpdir:
        site_dir = Path(tmpdir) / 'test_basic'

        result = subprocess.run([
            "mkdocs", "build",
            "--config-file", Path(__file__).parent / "fixtures/multiple_authors/mkdocs.yml",
            "--site-dir", site_dir,
            "--clean",
            #"--verbose",
        ])

        assert result.returncode == 0
        assert os.path.isfile(site_dir / 'atom.xml')
        
        atom = feedparser.parse(site_dir / 'atom.xml')
        #pprint.pprint(atom)

    assert len(atom['entries']) == 1
    assert len(atom['entries'][0]['authors']) == 2
    assert atom['entries'][0]['authors'][0]['name'] == 'foo'
    assert atom['entries'][0]['authors'][0]['email'] == 'foo@example.com'
    assert atom['entries'][0]['authors'][1]['name'] == 'bar'
    assert atom['entries'][0]['authors'][1]['email'] == 'bar@example.com'
