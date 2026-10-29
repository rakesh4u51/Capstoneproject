"""Load cached skill library."""

from pathlib import Path

SKILLS_DIR = Path("skills")


def load_skills():
    skills = []
    for skill_file in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        text = skill_file.read_text(encoding="utf-8")
        parts = text.split("---", 2)
        if len(parts) < 3:
            continue
        front_matter = parts[1]
        body = parts[2].strip()
        meta = {}
        for line in front_matter.strip().splitlines():
            key, sep, value = line.partition(":")
            if sep:
                meta[key.strip()] = value.strip()
        skills.append({"meta": meta, "body": body})
    return skills


def build_cached_system(active=None):
    skills = load_skills()
    if active:
        skills = [skill for skill in skills if skill["meta"].get("name") in active]
    library = "\n\n".join(f"## Skill: {skill['meta'].get('name')}\n{skill['body']}" for skill in skills)
    return [{"type": "text", "text": "Heritage National Bank skill library.\n\n" + library, "cache_control": {"type": "ephemeral"}}]


def get_skill(name):
    for skill in load_skills():
        if skill["meta"].get("name") == name:
            return skill
    raise KeyError(name)
