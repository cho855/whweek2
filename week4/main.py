import requests
from urllib.parse import urlencode

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


app.add_middleware(SessionMiddleware, secret_key="change-this-secret")


VALID_EMAIL = "abc@abc.com"
VALID_PASSWORD = "abc"

URL_CH = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
URL_EN = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"


HOTELS = {}


def load_json(url):
    response = requests.get(url, timeout=15) 
    if response.status_code == 200:
        return response.json()


def load_hotels_ch_en():
    HOTELS.clear()

    data_ch = load_json(URL_CH)
    data_en = load_json(URL_EN)


    ch_map = {}
    if isinstance(data_ch, dict) and isinstance(data_ch.get("list"), list):
        for row in data_ch["list"]:
            if not isinstance(row, dict):
                continue
            _id = row.get("_id")
            name_ch = row.get("旅宿名稱", "") or ""
            tel_ch = row.get("電話或手機號碼", "") or ""
            if _id and name_ch:
                try:
                    _id_int = int(_id)
                    ch_map[_id_int] = {"ch": name_ch, "tel": tel_ch}
                except:
                    pass

    en_count = 0
    if isinstance(data_en, dict) and isinstance(data_en.get("list"), list):
        for row in data_en["list"]:
            if not isinstance(row, dict):
                continue
            _id = row.get("_id")
            name_en = row.get("hotel name", "") or ""
            tel_en = row.get("tel", "") or ""
            if not _id:
                continue
            try:
                _id_int = int(_id)
            except:
                continue

            base = ch_map.get(_id_int, {"ch": "", "tel": ""})
            ch_name = base.get("ch", "")
            tel = base.get("tel", "")
            if not tel:
                tel = tel_en

            HOTELS[_id_int] = {
                "ch": ch_name,
                "en": name_en,
                "tel": tel,
            }
            en_count += 1

    for _id_int, base in ch_map.items():
        if _id_int not in HOTELS:
            HOTELS[_id_int] = {
                "ch": base.get("ch", ""),
                "en": "",
                "tel": base.get("tel", ""),
            }

    ch_only = len(ch_map) - en_count if len(ch_map) >= en_count else 0
    print("[hotels] merged: total=", len(HOTELS), "/ ch_only=", ch_only)
    return len(HOTELS)



@app.on_event("startup")
def _startup_load_hotels():
    total = load_hotels_ch_en()
    if total == 0:
        print("[startup] 飯店資料載入失敗，HOTELS 目前為空。")



@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/login")
def login(request: Request,
          email: str = Form(...),
          password: str = Form(...),
          agree: str = Form(None)):
    if not agree:
        request.session["logged_in"] = False
        request.session.pop("email", None)
        msg = urlencode({"msg": "請勾選同意條款"})
        return RedirectResponse(url=f"/ohoh?{msg}", status_code=303)

    if email == VALID_EMAIL and password == VALID_PASSWORD:
        request.session["logged_in"] = True
        request.session["email"] = email
        return RedirectResponse(url="/member", status_code=303)

    request.session["logged_in"] = False
    request.session.pop("email", None)
    msg = urlencode({"msg": "帳號或密碼輸入錯誤"})
    return RedirectResponse(url=f"/ohoh?{msg}", status_code=303)



@app.get("/member", response_class=HTMLResponse)
def member(request: Request):
    if not request.session.get("logged_in"):
        return RedirectResponse(url="/", status_code=303)
    email = request.session.get("email", "訪客")
    return templates.TemplateResponse("member.html", {"request": request, "email": email})


@app.get("/logout")
def logout(request: Request):
    request.session["logged_in"] = False
    request.session.pop("email", None)
    return RedirectResponse(url="/", status_code=303)


@app.get("/ohoh", response_class=HTMLResponse)
def ohoh(request: Request, msg: str = "發生未知錯誤"):
    return templates.TemplateResponse("error.html", {"request": request, "msg": msg})


@app.get("/hotel/{hid}", response_class=HTMLResponse)
def hotel_page(request: Request, hid: str):

    try:
        hid_int = int(hid)
    except:
        hid_int = None

    hotel = HOTELS.get(hid_int) if hid_int is not None else None
    return templates.TemplateResponse("hotel.html", {"request": request, "hotel": hotel})
