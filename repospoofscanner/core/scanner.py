from typing import Dict, List, Tuple
from rapidfuzz import fuzz
from .registries import RegistryValidator
from .parsers import parse_package_json, parse_requirements_txt
from ..utils.github_client import AsyncGitHubClient


class RepoSpoofScanner:
    def __init__(self):
        self.validator = RegistryValidator()

    async def scan(self, repo_url: str, gh_token: str = None) -> Dict:
        results = {
            "invalid": [],
            "typosquatted": [],
            "high_risk": []
        }

        repo_path = repo_url.replace("https://github.com/", "").strip("/")

        async with AsyncGitHubClient(gh_token) as gh_client:
            # Check NPM
            if (pkg_json := await gh_client.fetch_file_content(repo_path, "package.json")):
                npm_deps = parse_package_json(pkg_json)
                await self._analyze(npm_deps, "npm", results)

            # Check PyPI
            if (reqs_txt := await gh_client.fetch_file_content(repo_path, "requirements.txt")):
                pypi_deps = parse_requirements_txt(reqs_txt)
                await self._analyze(pypi_deps, "pypi", results)

        return results

    async def _analyze(self, deps: Dict[str, str], registry: str, results: Dict):
        for pkg in deps:
            if not await self.validator.validate(pkg, registry):
                results["invalid"].append(pkg)
                similar = [
                    (name, fuzz.ratio(pkg.lower(), name.lower()) / 100)
                    for name in await self.validator.search_similar(pkg, registry)
                    if fuzz.ratio(pkg, name) > 70
                ]
                results["typosquatted"].extend(similar)
                if any(score >= 0.85 for _, score in similar):
                    results["high_risk"].append(pkg)