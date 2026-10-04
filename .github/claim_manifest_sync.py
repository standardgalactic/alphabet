#!/usr/bin/env python3
"""Validate Central Theorem claim manifests against the canonical registry.

The claim registry in ``central-theorem/SPEC.md`` defines the set of
recognized ``CT-###`` identifiers. Implementation files may declare a
``MANIFEST:`` header containing the identifiers they implement,
formalize, test, or otherwise reference.

This checker enforces one invariant:

    Every CT-ID declared by a manifest must exist in the canonical
    registry.

Registry entries not referenced by a manifest are reported for
information only. A claim may exist solely in the specification or
monograph and therefore need no implementation manifest.

The checker operates on files available in the working tree. Repository
history, commit identity, timestamps, and content integrity remain the
responsibility of Git and the hosting platform.

No dependencies beyond the Python standard library.
"""

from pathlib import Path
import re
import sys


REGISTRY_PATH = Path("central-theorem/SPEC.md")

CT = re.compile(r"CT-\d{3}")

# Add implementation files here as they become part of this repository.
MANIFEST_PATHS = [
    Path("CentralTheorem.lean"),
    Path("crates/admissibility/src/lib.rs"),
    Path("docs/ADMISSIBILITY.md"),
]


def registry_ids(path):
    """Return CT-IDs declared by the SPEC Claim registry table."""
    ids = []
    in_section = False

    with path.open(encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("## "):
                in_section = "Claim registry" in line
                continue

            if in_section:
                match = re.match(r"^\|\s*(CT-\d{3})\s*\|", line)
                if match:
                    ids.append(match.group(1))

    return ids


def manifest_block(lines):
    """Return the MANIFEST header from an implementation file.

    The block begins at the first ``MANIFEST:`` line, optionally behind
    a ``//!`` documentation prefix, and continues across lines containing
    CT identifiers. Blank lines are retained only when followed by
    another CT-bearing line.
    """
    start = None

    for i, line in enumerate(lines):
        if re.match(r"^\s*(?://!\s*)?MANIFEST:", line):
            start = i
            break

    if start is None:
        return None

    block = [lines[start]]
    i = start + 1

    while i < len(lines):
        line = lines[i]

        if CT.search(line):
            block.append(line)
            i += 1
            continue

        if line.strip() == "":
            j = i
            while j < len(lines) and lines[j].strip() == "":
                j += 1

            if j < len(lines) and CT.search(lines[j]):
                block.append("")
                i = j
                continue

        break

    return block


def manifest_ids(path):
    """Return the CT-IDs declared by a file's MANIFEST header."""
    text = path.read_text(encoding="utf-8")
    block = manifest_block(text.splitlines())

    if block is None:
        return None

    ids = set()
    for line in block:
        ids.update(CT.findall(line))

    return ids


def main():
    if not REGISTRY_PATH.is_file():
        sys.exit(f"fatal: registry not found: {REGISTRY_PATH}")

    registry = set(registry_ids(REGISTRY_PATH))

    if not registry:
        sys.exit(
            f"fatal: no CT-IDs parsed from {REGISTRY_PATH}; "
            "is the Claim registry table intact?"
        )

    print(f"registry: {len(registry)} CT-IDs ({REGISTRY_PATH})")
    print()

    claimed = set()
    failures = []

    available = [path for path in MANIFEST_PATHS if path.is_file()]

    if not available:
        print("no implementation manifests found in this working tree")
        print()
    else:
        for path in available:
            ids = manifest_ids(path)

            if ids is None:
                failures.append(f"{path}: no MANIFEST header found")
                continue

            claimed |= ids
            unknown = sorted(ids - registry)

            print(path)
            print(
                "  claims: "
                + (", ".join(sorted(ids)) if ids else "none")
            )

            if unknown:
                print(
                    "  unknown: "
                    + ", ".join(unknown)
                )
                failures.append(
                    f"{path} claims unregistered IDs: "
                    + ", ".join(unknown)
                )
            else:
                print("  status: OK")

            print()

    unclaimed = sorted(registry - claimed)

    print(
        "registry IDs without a local manifest: "
        + (", ".join(unclaimed) if unclaimed else "none")
    )

    if failures:
        print("\nFAIL:")
        for failure in failures:
            print(f"  {failure}")
        return 1

    print("\nOK: every manifested CT-ID exists in the registry.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())