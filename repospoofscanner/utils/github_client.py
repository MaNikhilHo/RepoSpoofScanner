import httpx
from github import Github
from github.GithubException import GithubException

class AsyncGitHubClient:
    def __init__(self, token: str | None = None):
        self.sync_client = Github(token) if token else Github()
        self.async_client = httpx.AsyncClient()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.async_client.aclose()

    async def fetch_file_content(self, repo_url: str, filename: str) -> str | None:
        try:
            repo_path = repo_url.replace("https://github.com/", "").strip("/")
            repo = self.sync_client.get_repo(repo_path)
            file = repo.get_contents(filename)
            return file.decoded_content.decode()
        except Exception as e:
            return None