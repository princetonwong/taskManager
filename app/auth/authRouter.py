from fastapi import status, HTTPException, Depends, Request, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from .supabaseAuth import supabaseClient


templates = Jinja2Templates(directory="templates")
AuthRouter = APIRouter()


@AuthRouter.get('/login', response_class=RedirectResponse, include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "id": id})


@AuthRouter.post('/signup', summary="Create new user")
async def create_user(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        res = supabaseClient.auth.sign_up(
            dict(email=form_data.username,
                 password=form_data.password
                 )
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    return RedirectResponse(url='/auth/login')


@AuthRouter.post('/login', summary="Create access and refresh tokens for user")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        res = supabaseClient.auth.sign_in_with_password(
            dict(email=form_data.username,
                 password=form_data.password
                 )
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    res = supabaseClient.auth.set_session(access_token=res.session.access_token,
                                           refresh_token=res.session.refresh_token)
    return templates.TemplateResponse(
        "loggedIn.html",
        dict(request=request, session=res.session))


@AuthRouter.post("/logout", summary="Logout user")
async def logout():
    res = supabaseClient.auth.sign_out()
    return RedirectResponse(url='/auth/login', status_code=status.HTTP_302_FOUND)
