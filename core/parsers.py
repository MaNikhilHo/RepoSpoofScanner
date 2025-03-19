import json
import re
from typing import Dict

def parse_package_json(content: str) -> Dict[str, str]:
    try:
        data = json.loads(content)
        return {
            **data.get("dependencies", {}),
            **data.get("devDependencies", {})
        }
    except json.JSONDecodeError:
        return {}

def parse_requirements_txt(content: str) -> Dict[str, str]:
    packages = {}
    for line in content.splitlines():
        line = line.strip().split("#")[0]  # Remove comments
        if line and not line.startswith("-"):
            pkg = re.split(r"[=<>~]", line)[0].strip()
            packages[pkg] = ""
    return packages