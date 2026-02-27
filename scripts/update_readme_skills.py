#!/usr/bin/env python3
"""
Update README.md Skills section from skills/*/SKILL.md frontmatter.
Overwrites only content between <!-- SKILLS:START --> and <!-- SKILLS:END -->.
"""
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
README_PATH = REPO_ROOT / "README.md"
START_MARKER = "<!-- SKILLS:START -->"
END_MARKER = "<!-- SKILLS:END -->"


def parse_frontmatter(path: Path) -> dict:
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    block = parts[1].strip()
    out = {}
    for line in block.split("\n"):
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1].replace('""', '"')
        elif value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
        out[key] = value
    return out


def skill_display_name(slug: str) -> str:
    return slug.replace("-", " ").replace("_", " ").title()


def collect_skills() -> list[tuple[str, str, str]]:
    if not SKILLS_DIR.is_dir():
        return []
    result = []
    for path in sorted(SKILLS_DIR.iterdir()):
        if not path.is_dir():
            continue
        slug = path.name
        skill_md = path / "SKILL.md"
        if not skill_md.is_file():
            continue
        fm = parse_frontmatter(skill_md)
        name = fm.get("name", slug)
        description = fm.get("description", "")
        result.append((slug, name, description))
    return result


def generate_bullets(skills: list[tuple[str, str, str]]) -> str:
    lines = []
    for slug, name, description in skills:
        display = skill_display_name(name)
        link = f"skills/{slug}/SKILL.md"
        line = f"- **[{display}]({link})** — {description}"
        lines.append(line)
    return "\n".join(lines) if lines else ""


def update_readme(new_content: str) -> bool:
    text = README_PATH.read_text(encoding="utf-8")
    if START_MARKER not in text or END_MARKER not in text:
        print("README.md must contain both <!-- SKILLS:START --> and <!-- SKILLS:END -->", file=sys.stderr)
        sys.exit(1)
    pattern = re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER)
    new_section = f"{START_MARKER}\n{new_content}\n{END_MARKER}"
    new_text, n = re.subn(pattern, new_section, text, count=1, flags=re.DOTALL)
    if n != 1:
        sys.exit(1)
    if new_text == text:
        return False
    README_PATH.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    os.chdir(REPO_ROOT)
    skills = collect_skills()
    bullets = generate_bullets(skills)
    changed = update_readme(bullets)
    if changed:
        print("README.md updated.")
    else:
        print("README.md unchanged.")


if __name__ == "__main__":
    main()
