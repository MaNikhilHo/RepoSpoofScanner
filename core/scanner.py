from Levenshtein import distance as levenshtein
from typing import List, Tuple
from .registries import RegistryValidator

class RepoScanner:
    def __init__(self):
        self.validator = RegistryValidator()

    async def scan_repo(self, repo_url: str) -> dict:
        # Task for future me. Implement later (combine all components)
        pass

    async def detect_typosquats(self, package: str, registry: str) -> List[Tuple[str, int]]:
        similar = await self.validator.search_similar(package, registry)
        return [
            (pkg, levenshtein(package, pkg))
            for pkg in similar
            if levenshtein(package, pkg) <= 2
        ]