from github import Github
from github.GithubException import RateLimitExceededException
import httpx

class AsyncGitHubClient:
    def __init__(self, token: str | None = None):
        self.token = token
        self.client = Github(token) if token else Github()
        self.async_http = httpx.AsyncClient()

    async def fetch_file_content(self, repo_url: str, file_path: str) -> str | None:
        repo_name = repo_url.replace("https://github.com/", "")
        try:
            repo = self.client.get_repo(repo_name)
            file = repo.get_contents(file_path)
            return file.decoded_content.decode()
        except RateLimitExceededException:
            raise RuntimeError("GitHub API rate limit exceeded. Use a token.")
        except Exception:
            return None

    async def close(self):
        await self.async_http.aclose()