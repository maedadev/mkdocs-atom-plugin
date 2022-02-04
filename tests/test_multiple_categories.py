import feedparser
import os
import pprint
import subprocess
import tempfile
from pathlib import Path


def test_multiple_categories():
    with tempfile.TemporaryDirectory() as tmpdir:
        site_dir = Path(tmpdir) / 'test_basic'

        result = subprocess.run([
            "mkdocs", "build",
            "--config-file", Path(__file__).parent / "fixtures/multiple_categories/mkdocs.yml",
            "--site-dir", site_dir,
            "--clean",
            #"--verbose",
        ])

        assert result.returncode == 0
        assert os.path.isfile(site_dir / 'atom.xml')
        
        atom = feedparser.parse(site_dir / 'atom.xml')
        #pprint.pprint(atom)

    assert len(atom['entries']) == 1
    assert len(atom['entries'][0]['tags']) == 2
    assert atom['entries'][0]['tags'][0]['term'] == 'category:baseball'
    assert atom['entries'][0]['tags'][0]['label'] == 'baseball'
    assert atom['entries'][0]['tags'][1]['term'] == 'category:soccer'
    assert atom['entries'][0]['tags'][1]['label'] == 'soccer'
