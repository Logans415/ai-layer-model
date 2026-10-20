"""Validate model/skill consistency and the public-only release boundary. MIT."""

import json

# XML parsing is limited to the checked-in repository SVG fixture.
import xml.etree.ElementTree as ET  # nosec B405
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
model = json.loads((ROOT / "model/layers.json").read_text(encoding="utf-8"))
assert [x["id"] for x in model["layers"]] == list(range(1, 10))
assert model["planes"] == {
    "Substrate": [1, 2],
    "Cognition": [3, 4, 5, 6],
    "Systems": [7, 8, 9],
}
assert all(x["id"] in model["planes"][x["plane"]] for x in model["layers"])
assert [x["id"] for x in model["build_companion"]] == [
    "B" + str(i) for i in range(1, 8)
]
assert (ROOT / "model/layers.json").read_bytes() == (
    ROOT / "skills/map-ai-stack/references/layers.json"
).read_bytes(), "Bundled skill definitions drifted"
assert len(model["cross_cutting"]) >= 5
# The file is a checked-in build artifact, never an external XML response.
ET.parse(ROOT / "assets/ai-layer-model.svg")  # nosec B314
for f in [
    "README.md",
    "LICENSE",
    "LICENSES/CC-BY-4.0.txt",
    "LICENSES/MIT.txt",
    "CITATION.cff",
    "PROVENANCE.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "skills/map-ai-stack/SKILL.md",
]:
    assert (ROOT / f).is_file(), f
assert model["version"] in (ROOT / "CITATION.cff").read_text(encoding="utf-8")
forbidden = []
for p in ROOT.rglob("*"):
    if not p.is_file() or ".git" in p.parts:
        continue
    if p.suffix.lower() in {
        ".ppt",
        ".pptx",
        ".pptm",
        ".pps",
        ".ppsx",
        ".odp",
        ".keynote",
        ".docx",
        ".xlsx",
        ".pdf",
        ".html",
        ".htm",
        ".mp4",
        ".webm",
        ".mov",
        ".mp3",
        ".wav",
        ".pem",
        ".key",
        ".ppk",
    } or p.name in {".env", ".global.env"}:
        forbidden.append(str(p.relative_to(ROOT)))
    elif any(
        marker in p.name.lower()
        for marker in ("speaker-notes", "speaker-script", "rehearsal", "transcript")
    ):
        forbidden.append(str(p.relative_to(ROOT)))
assert not forbidden, "Unexpected private/binary artifacts: " + repr(forbidden)
print(
    "PASS: nine layers, planes, build companion, bundled model, SVG, citation version, licensing files and public-only artifact boundary"
)
