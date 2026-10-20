"""Build deterministic release archives from the validated file set. MIT."""

import argparse
import hashlib
import zipfile
from pathlib import Path

try:
    from .validate_release import ROOT, validate_release
except ImportError:
    from validate_release import ROOT, validate_release

ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def build_archives(output, root=ROOT):
    root = Path(root).resolve()
    output = Path(output).resolve()
    if output == root or root in output.parents:
        raise ValueError("Archive output must be outside the checkout")
    files = validate_release(root)
    payloads = {p.relative_to(root).as_posix(): p.read_bytes() for p in files}
    names = ("ai-layer-model-publication-package.zip", "map-ai-stack-skill.zip")
    if any((output / n).exists() for n in (*names, "sha256sums.txt")):
        raise FileExistsError("Release outputs already exist")
    output.mkdir(parents=True, exist_ok=True)
    for name in names:
        skill_only = name == names[1]
        with zipfile.ZipFile(
            output / name, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9
        ) as archive:
            for relative, data in sorted(payloads.items()):
                if skill_only:
                    if not relative.startswith("skills/map-ai-stack/"):
                        continue
                    entry = relative.removeprefix("skills/")
                else:
                    entry = "ai-layer-model/" + relative
                info = zipfile.ZipInfo(entry, date_time=ZIP_TIMESTAMP)
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(
                    info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9
                )
    checksums = "".join(
        hashlib.sha256((output / name).read_bytes()).hexdigest() + "  " + name + "\n"
        for name in names
    )
    with (output / "sha256sums.txt").open(
        "x", encoding="utf-8", newline="\n"
    ) as stream:
        stream.write(checksums)
    return tuple(output / name for name in (*names, "sha256sums.txt"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    for path in build_archives(args.output):
        print(path.name)
