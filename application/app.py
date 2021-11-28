from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from returns.result import Result
from returns.pipeline import is_successful

from .helpers import flash, get_flashed_messages
from .views import AllProjects, FolderSummaryView
from .forms import URLRequest
from .representers import ReposRepresenter, FolderSummaryRepresenter
from .services import AddProject
from config import get_settings
from infrastructure import ApiGateway


config = get_settings()
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=config.SESSION_SECRET)

app.mount("/static", StaticFiles(directory="presentation/static"), name="static")

templates = Jinja2Templates(directory="presentation/views")
templates.env.globals["get_flashed_messages"] = get_flashed_messages


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    repos_json: str = ApiGateway().all_repos()
    all_repos: ReposRepresenter = ReposRepresenter.parse_raw(repos_json)
    projects = AllProjects(all_repos)

    if projects.none:
        flash(request, "Add a Github project to get started", "notice")

    # Ref: https://fastapi.tiangolo.com/advanced/templates/
    # `request` must be passed as part of the key-value pairs in the context for Jinja2
    return templates.TemplateResponse(
        "home.html", {"request": request, "projects": projects}
    )


@app.post("/repo/")
def create_repo(request: Request, create_request: URLRequest = Depends()):
    result: Result = AddProject()(create_request)

    if is_successful(result):
        flash(request, "New project added!", "notice")
    else:
        flash(request, result.failure(), "error")

    return RedirectResponse("/", status_code=303)


@app.get("/repo/{ownername}/{reponame}")
def summary_for_entire_repo(ownername: str, reponame: str, request: Request):
    summary_json: str = ApiGateway().folder_summary(ownername, reponame, "")
    summary: FolderSummaryRepresenter = FolderSummaryRepresenter.parse_raw(summary_json)
    folder_summary = FolderSummaryView(summary, request.url.path)

    return templates.TemplateResponse(
        "folder_summary.html", {"request": request, "folder": folder_summary}
    )


@app.get("/repo/{ownername}/{reponame}/{folder:path}")
def summary_for_specific_folder(
    ownername: str, reponame: str, folder: str, request: Request
):
    summary_json: str = ApiGateway().folder_summary(ownername, reponame, folder)
    summary: FolderSummaryRepresenter = FolderSummaryRepresenter.parse_raw(summary_json)
    folder_summary = FolderSummaryView(summary, request.url.path)

    return templates.TemplateResponse(
        "folder_summary.html", {"request": request, "folder": folder_summary}
    )
