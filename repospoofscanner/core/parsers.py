import json
import re

def parse_package_json(content: str) -> dict:
    try:
        data = json.loads(content)
        return {
            **data.get("dependencies", {}),
            **data.get("devDependencies", {})
        }
    except json.JSONDecodeError:
        return {}

def parse_requirements_txt(content: str) -> dict:
    return {
        line.split("#")[0].strip().split("==")[0]
        for line in content.splitlines()
        if line.strip() and not line.startswith("-")
    }