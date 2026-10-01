from html.parser import HTMLParser
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "docs" / "index.html"
JS = ROOT / "docs" / "assets" / "app-v2.js"


class UIParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.layers = []
        self.actions = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if "data-layer-link" in a:
            self.layers.append((tag, a.get("href")))
        if "data-action" in a:
            self.actions.append((tag, a.get("data-action"), a.get("href")))


def test_pages_uses_fresh_v2_controller():
    html = HTML.read_text(encoding="utf-8")
    assert "./assets/app-v2.js?v=8" in html
    assert "./assets/styles.css?v=8" in html
    assert "data-js-status" in html
    assert "data-self-check" in html


def test_eight_layer_links_have_real_fallback_targets():
    parser = UIParser()
    parser.feed(HTML.read_text(encoding="utf-8"))
    assert len(parser.layers) == 8
    for tag, href in parser.layers:
        assert tag == "a"
        assert href and href.startswith("#")
        assert href[1:] in parser.ids


def test_enhanced_actions_still_have_native_href_fallbacks():
    parser = UIParser()
    parser.feed(HTML.read_text(encoding="utf-8"))
    actions = {name: (tag, href) for tag, name, href in parser.actions}
    assert {"grow-emergence", "reset-emergence", "memory-next", "memory-prev", "memory-reset"} <= set(actions)
    for tag, href in actions.values():
        assert tag == "a"
        assert href and href.startswith("#")


def test_v2_controller_uses_delegated_actions_and_self_check():
    js = JS.read_text(encoding="utf-8")
    assert "document.addEventListener('click'" in js
    assert "event.target.closest('[data-action]')" in js
    assert "8/8 UI TETHER PASS" in js
    assert "memory-next" in js
    assert "grow-emergence" in js


def test_v2_javascript_syntax_when_node_is_available():
    node = shutil.which("node")
    if node is None:
        return
    completed = subprocess.run([node, "--check", str(JS)], capture_output=True, text=True)
    assert completed.returncode == 0, completed.stderr
