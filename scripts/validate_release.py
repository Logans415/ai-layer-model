"""Validate the model and the explicit release-file set. MIT."""

import json
import os

# Parsing is limited to the checked-in SVG fixture.
import xml.etree.ElementTree as ET  # nosec B405
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FILES = frozenset(
    [
        ".github/ISSUE_TEMPLATE/mapping.md",
        ".github/workflows/validate.yml",
        ".gitignore",
        "CHANGELOG.md",
        "CITATION.cff",
        "CODE_OF_CONDUCT.md",
        "CONTRIBUTING.md",
        "LICENSE",
        "LICENSES/CC-BY-4.0.txt",
        "LICENSES/MIT.txt",
        "PROVENANCE.md",
        "README.md",
        "SECURITY.md",
        "assets/ai-layer-model.svg",
        "docs/model.md",
        "docs/related-work.md",
        "examples/mcp.md",
        "examples/meeting-assistant.md",
        "examples/ollama.md",
        "model/layers.json",
        "prompts/map-an-item.md",
        "ruff.toml",
        "scripts/package_release.py",
        "scripts/validate_release.py",
        "skills/map-ai-stack/LICENSE-MIT.txt",
        "skills/map-ai-stack/LICENSE-REFERENCE-CC-BY-4.0.txt",
        "skills/map-ai-stack/SKILL.md",
        "skills/map-ai-stack/agents/openai.yaml",
        "skills/map-ai-stack/references/layers.json",
        "tests/test_release_tools.py",
    ]
)


def release_paths(root=ROOT):
    """Reject missing, additional or linked paths before reading their contents."""
    root = Path(root).resolve()
    found = set()
    unexpected = []
    for current, directories, filenames in os.walk(root, followlinks=False):
        current = Path(current)
        for name in list(directories):
            path = current / name
            relative = path.relative_to(root).as_posix()
            if relative == ".git":
                directories.remove(name)
            elif path.is_symlink() or path.is_junction():
                raise ValueError("Release paths must be regular files and directories")
            elif name in {"__pycache__", ".ruff_cache"}:
                directories.remove(name)
            elif not any(p.startswith(relative + "/") for p in PUBLIC_FILES):
                unexpected.append(relative + "/")
                directories.remove(name)
        for name in filenames:
            path = current / name
            relative = path.relative_to(root).as_posix()
            if relative == ".git":
                continue
            if path.is_symlink() or path.is_junction():
                raise ValueError("Release paths must be regular files and directories")
            found.add(relative)
    unexpected.extend(sorted(found - PUBLIC_FILES))
    if unexpected:
        raise ValueError("Unexpected release paths: " + repr(sorted(unexpected)))
    missing = PUBLIC_FILES - found
    if missing:
        raise ValueError("Missing release paths: " + repr(sorted(missing)))
    return tuple(root / name for name in sorted(PUBLIC_FILES))


def validate_release(root=ROOT):
    """Check model invariants after the file boundary is established."""
    if not __debug__:
        raise RuntimeError("Run release validation without Python optimization")
    root = Path(root).resolve()
    paths = release_paths(root)
    model = json.loads((root / "model/layers.json").read_text(encoding="utf-8"))
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
    assert (root / "model/layers.json").read_bytes() == (
        root / "skills/map-ai-stack/references/layers.json"
    ).read_bytes(), "Bundled skill definitions drifted"
    assert len(model["cross_cutting"]) >= 5
    ET.parse(root / "assets/ai-layer-model.svg")  # nosec B314
    assert model["version"] in (root / "CITATION.cff").read_text(encoding="utf-8")
    return paths


if __name__ == "__main__":
    validate_release()
    print("PASS: model consistency, citation version and explicit release-file set")
