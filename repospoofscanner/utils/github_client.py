import httpx
from github import Github
from github.GithubException import RateLimitExceededException

class AsyncGitHubClient:
    def __init__(self, token: str | None = None):
        self.token = token
        self.sync_client = Github(token) if token else Github()
        self.async_client = httpx.AsyncClient()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.async_client.aclose()

    async def fetch_file_content(self, repo_path: str, filename: str) -> str | None:
        try:
            repo = self.sync_client.get_repo(repo_path)
            file = repo.get_contents(filename)
            return file.decoded_content.decode()
        except RateLimitExceededException:
            raise RuntimeError("GitHub API rate limit exceeded. Use a token.")
        except Exception as e:
            print(f"Error fetching {filename}: {str(e)}")
            return None