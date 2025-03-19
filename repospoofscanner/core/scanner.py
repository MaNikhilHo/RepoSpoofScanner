from typing import Dict, List, Tuple
from rapidfuzz import distance as fuzz
from .registries import RegistryValidator
from .parsers import parse_package_json, parse_requirements_txt
from ..utils.github_client import AsyncGitHubClient


class RepoSpoofScanner:
    def __init__(self):
        self.validator = RegistryValidator()

    async def scan(self, repo_url: str, gh_token: str | None = None) -> Dict:
        """Scan a repository for suspicious dependencies"""
        gh_client = AsyncGitHubClient(gh_token)
        results = {
            "invalid": [],
            "typosquatted": [],
            "high_risk": []
        }

        try:
            # Scan package.json
            package_json = await gh_client.fetch_file_content(repo_url, "package.json")
            if package_json:
                npm_deps = parse_package_json(package_json)
                await self._analyze_dependencies(npm_deps, "npm", results)

            # Scan requirements.txt
            requirements_txt = await gh_client.fetch_file_content(repo_url, "requirements.txt")
            if requirements_txt:
                pypi_deps = parse_requirements_txt(requirements_txt)
                await self._analyze_dependencies(pypi_deps, "pypi", results)

        finally:
            await gh_client.close()

        return results

    async def _analyze_dependencies(self, dependencies: Dict[str, str], registry: str, results: Dict):
        """Helper method to analyze dependencies for a registry"""
        for pkg in dependencies:
            if not await self.validator.validate(pkg, registry):
                results["invalid"].append(pkg)
                similar = await self._check_typosquatting(pkg, registry)
                results["typosquatted"].extend(similar)

                # Flag if similarity score is too high
                if any(score >= 0.85 for _, score in similar):
                    results["high_risk"].append(pkg)

    async def _check_typosquatting(self, pkg: str, registry: str) -> List[Tuple[str, float]]:
        """Check for similar package names using RapidFuzz"""
        similar_packages = await self.validator.search_similar(pkg, registry)
        return [
            (name, fuzz.ratio(pkg.lower(), name.lower()) / 100)  # Normalize to 0-1 scale
            for name in similar_packages
            if fuzz.ratio(pkg.lower(), name.lower()) >= 70  # 70% similarity threshold
        ]