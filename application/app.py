from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from infrastructure import ApiGateway

from .representers import ReposRepresenter


app = FastAPI()

app.mount("/static", StaticFiles(directory="presentation/static"), name="static")

templates = Jinja2Templates(directory="presentation/views")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    repos_json: str = ApiGateway().all_repos()
    all_repos: ReposRepresenter = ReposRepresenter.parse_raw(repos_json)

    # Ref: https://fastapi.tiangolo.com/advanced/templates/
    # `request` must be passed as part of the key-value pairs in the context for Jinja2
    return templates.TemplateResponse(
        "home.html", {"request": request, "repos": all_repos.repos}
    )


@app.post("/repo/")
def create_repo(github_url: str = Form(...)):
    gh_url = github_url.lower()

    if "github.com" not in gh_url or len(gh_url.split("/")) < 3:
        raise HTTPException(status_code=400)

    ownername, reponame = gh_url.split("/")[-2:]
    return ApiGateway().create_repo(ownername, reponame)
