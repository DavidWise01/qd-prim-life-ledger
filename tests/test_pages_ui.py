from html.parser import HTMLParser
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "docs" / "index.html"
CSS = ROOT / "docs" / "assets" / "styles.css"
JS = ROOT / "docs" / "assets" / "app-v3.js"


class UIParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.layers = []
        self.radios = []
        self.labels = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if "data-layer-link" in a:
            self.layers.append((tag, a.get("href")))
        if tag == "input" and a.get("type") == "radio":
            self.radios.append((a.get("name"), a.get("id"), "checked" in a))
        if tag == "label" and a.get("for"):
            self.labels.append(a["for"])


def parse():
    p = UIParser()
    p.feed(HTML.read_text(encoding="utf-8"))
    return p


def test_pages_uses_native_control_v9():
    html = HTML.read_text(encoding="utf-8")
    assert "./assets/app-v3.js?v=9" in html
    assert "./assets/styles.css?v=9" in html
    assert "data-js-status" in html
    assert "data-self-check" in html


def test_eight_layer_links_have_real_targets():
    p = parse()
    assert len(p.layers) == 8
    for tag, href in p.layers:
        assert tag == "a"
        assert href and href.startswith("#")
        assert href[1:] in p.ids


def test_native_emergence_and_memory_state_counts():
    p = parse()
    emergence = [r for r in p.radios if r[0] == "emergence-state"]
    memory = [r for r in p.radios if r[0] == "memory-state"]
    assert len(emergence) == 9
    assert len(memory) == 8
    assert sum(1 for r in emergence if r[2]) == 1
    assert sum(1 for r in memory if r[2]) == 1


def test_every_control_label_targets_a_real_radio():
    p = parse()
    radio_ids = {radio_id for _, radio_id, _ in p.radios}
    control_labels = [target for target in p.labels if target.startswith("em") or target.startswith("mem")]
    assert control_labels
    assert all(target in radio_ids for target in control_labels)


def test_css_contains_native_state_transition_selectors():
    css = CSS.read_text(encoding="utf-8")
    assert "#em8:checked ~ .emergence-lattice" in css
    assert "#mem7:checked ~ .memory-state-deck .state-7" in css
    assert ".memory-state-panel" in css
    assert ".em-next" in css


def test_v3_javascript_is_optional_diagnostics_only():
    js = JS.read_text(encoding="utf-8")
    assert "NATIVE 8/8 CONTROL PASS" in js
    assert "input[name=\"emergence-state\"]" in js
    assert "input[name=\"memory-state\"]" in js
    assert "preventDefault" not in js
    assert "data-action" not in js


def test_v3_javascript_syntax_when_node_is_available():
    node = shutil.which("node")
    if node is None:
        return
    completed = subprocess.run([node, "--check", str(JS)], capture_output=True, text=True)
    assert completed.returncode == 0, completed.stderr
