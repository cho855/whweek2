from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

import mysql.connector

app = FastAPI()


app.add_middleware(SessionMiddleware, secret_key="asdasdasd")


templates = Jinja2Templates(directory="templates")




def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Aaaaaaaa",  
        database="website"             
    )


# Task 1
@app.get("/")
def home(request: Request):
    member = request.session.get("member")
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "member": member}
    )


#  Task 2
@app.post("/signup") 
def signup(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM member WHERE email = %s", [email])
    result = cursor.fetchone()

    if result is not None:
        cursor.close()
        conn.close()
        return RedirectResponse(
            url="/ohoh?msg=重複的電子郵件",
            status_code=302
        )

    cursor.execute(
        "INSERT INTO member (name, email, password) VALUES (%s, %s, %s)",
        [name, email, password]
    )
    conn.commit()
    cursor.close()
    conn.close()

    return RedirectResponse(url="/", status_code=302)


#  Task 3
@app.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, email FROM member WHERE email = %s AND password = %s",
        [email, password]
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row is None:
        return RedirectResponse(
            url="/ohoh?msg=帳號或密碼輸入錯誤",
            status_code=302
        )

    member_id, name, email = row
    request.session["member"] = {
        "id": member_id,
        "name": name,
        "email": email
    }

    return RedirectResponse(url="/member", status_code=302)


# Task 4
@app.get("/logout")
def logout(request: Request):
    request.session.pop("member", None)
    return RedirectResponse(url="/", status_code=302)


# Task 5
@app.get("/member")
def member_page(request: Request):
    member = request.session.get("member")
    if member is None:
        return RedirectResponse(url="/", status_code=302)

    conn = get_connection()
    cursor = conn.cursor()

 
    cursor.execute(
        """
        SELECT message.id,
               member.name,
               message.content,
               message.member_id
        FROM message
        JOIN member ON message.member_id = member.id
        ORDER BY message.id DESC
        """
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    messages = []
    for msg_id, author_name, content, member_id in rows:
        messages.append({
            "id": msg_id,
            "author_name": author_name,
            "content": content,
            "member_id": member_id,
        })

    return templates.TemplateResponse(
        "member.html",
        {
            "request": request,
            "member": member,
            "messages": messages,
        }
    )


# Task 5
@app.post("/createMessage")
def create_message(
    request: Request,
    content: str = Form(...)
):
    member = request.session.get("member")
    if member is None:
        return RedirectResponse(url="/", status_code=302)

    content = content.strip()
    if content == "":
        return RedirectResponse(url="/member", status_code=302)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO message (member_id, content) VALUES (%s, %s)",
        [member["id"], content]
    )
    conn.commit()
    cursor.close()
    conn.close()

    return RedirectResponse(url="/member", status_code=302)


# Task 6
@app.post("/deleteMessage")
def delete_message(
    request: Request,
    message_id: int = Form(...)
):
    member = request.session.get("member")
    if member is None:
        return RedirectResponse(url="/", status_code=302)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM message WHERE id = %s AND member_id = %s",
        [message_id, member["id"]]
    )
    conn.commit()
    cursor.close()
    conn.close()

    return RedirectResponse(url="/member", status_code=302)


# error page
@app.get("/ohoh")
def error_page(request: Request, msg: str = Query("")):
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "message": msg
        }
    )
