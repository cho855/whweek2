from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
from datetime import datetime 

import mysql.connector

app = FastAPI()


app.add_middleware(SessionMiddleware, secret_key="asdasdasd")


templates = Jinja2Templates(directory="templates")




def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="aaaaaaaa",  
        database="website"             
    )


# week6 Task 1
@app.get("/")
def home(request: Request):
    member = request.session.get("member")
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "member": member}
    )


#  week6 Task 2
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


# week6 Task 3
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


# week6 Task 4
@app.get("/logout")
def logout(request: Request):
    request.session.pop("member", None)
    return RedirectResponse(url="/", status_code=302)


# week6 Task 5
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


# week6 Task 5
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


# week6 Task 6
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


# week6 error page
@app.get("/ohoh")
def error_page(request: Request, msg: str = Query("")):
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "message": msg
        }
    )




# week7 Task 4 
@app.get("/api/member/query-log")
def get_query_log(request: Request):
    """
    回傳目前登入會員「被誰查過」的紀錄（最多 10 筆）。
    回傳格式：
      未登入：{"data": null}
      有登入：
        {
          "data": [
            {"searcher_name": "某某", "query_time": "2025-11-28 14:22:33"},
            ...
          ]
        }
    """

  
    member = request.session.get("member")
    if member is None:
        return {"data": None}

    my_id = member["id"]

 
    conn = get_connection()
    cursor = conn.cursor()  


    cursor.execute(
        """
        SELECT 
            m.name AS searcher_name,
            q.query_time
        FROM member_query_log AS q
        JOIN member AS m ON q.searcher_id = m.id
        WHERE q.target_id = %s
        ORDER BY q.query_time DESC
        LIMIT 10
        """,
        [my_id]
    )

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

 
    logs = []
    for searcher_name, query_time in rows:

        if isinstance(query_time, datetime):
            time_str = query_time.strftime("%Y-%m-%d %H:%M:%S")
        else:

            time_str = str(query_time)

        logs.append({
            "searcher_name": searcher_name,
            "query_time": time_str
        })

    return {"data": logs}



# week7 Task 1 
@app.get("/api/member/{member_id}")
def get_member(member_id: int, request: Request):

   
    member = request.session.get("member")
    if member is None:
        return {"data": None}

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        "SELECT id, name, email FROM member WHERE id = %s",
        [member_id]
    )
    row = cursor.fetchone()


    if row is None:
        cursor.close()
        conn.close()
        return {"data": None}

    found_id, name, email = row


    if member["id"] != member_id:
        cursor.execute(
            "INSERT INTO member_query_log (searcher_id, target_id) VALUES (%s, %s)",
            [member["id"], member_id]
        )
        conn.commit()


    cursor.close()
    conn.close()


    return {
        "data": {
            "id": found_id,
            "name": name,
            "email": email
        }
    }



# week7 Task 3 

class NameUpdate(BaseModel):
    name: str


@app.patch("/api/member")
def update_member_name(data: NameUpdate, request: Request):
    """
    更新目前登入會員的姓名。
    接收 JSON：{"name": "新的使用者姓名"}
    成功 → 回傳 {"ok": true}
    失敗 → 回傳 {"error": true}
    """

    member = request.session.get("member")
    if member is None:
        return {"error": True}

    new_name = data.name.strip()


    if new_name == "":
        return {"error": True}

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE member SET name = %s WHERE id = %s",
        [new_name, member["id"]]
    )
    conn.commit()
    updated_rows = cursor.rowcount  

    cursor.close()
    conn.close()


    if updated_rows == 0:
        return {"error": True}


    member["name"] = new_name
    request.session["member"] = member

    return {"ok": True}


