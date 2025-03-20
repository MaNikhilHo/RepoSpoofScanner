import httpx

class RegistryValidator:
    REGISTRY_ENDPOINTS = {
        "npm": "https://registry.npmjs.org/{}",
        "pypi": "https://pypi.org/pypi/{}/json"
    }

    def __init__(self):
        self.client = httpx.AsyncClient()

    async def validate(self, package: str, registry: str) -> bool:
        url = self.REGISTRY_ENDPOINTS[registry].format(package)
        resp = await self.client.get(url)
        return resp.status_code == 200

    async def search_similar(self, package: str, registry: str) -> list[str]:
        if registry == "npm":
            resp = await self.client.get(
                "https://registry.npmjs.org/-/v1/search",
                params={"text": package}
            )
            return [p["package"]["name"] for p in resp.json().get("objects", [])]
        # Task for future me. Add PyPI/RubyGems later
        return []