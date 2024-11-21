import secrets
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from model.user_connection import UserConnection
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from schema.user_schema import UserSchema


app = FastAPI()
conn = UserConnection()
security = HTTPBasic()
correct_username_bytes = b"admin"
correct_password_bytes = b"okn947V*"

def get_current_username(credentials: Annotated[HTTPBasicCredentials, Depends(security)],):
    current_username_bytes = credentials.username.encode("utf8")
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True


@app.get("/api", status_code=HTTP_200_OK)
def banner():
    return "Cloud Security and FastApi rock's"


@app.get("/api/users", status_code=HTTP_200_OK)
def root():
    items = []
    for data in conn.read_all():
        dictionary = {}
        dictionary["id"] = data[0]
        dictionary["name"] = data[1]
        dictionary["phone"] = data[2]
        items.append(dictionary)
    return items


@app.get("/api/users/{id}", status_code=HTTP_200_OK)
def get_one(id:str):
     dictionary = {}
     data = conn.read_one(id)
     dictionary["id"] = data[0]
     dictionary["name"] = data[1]
     dictionary["phone"] = data[2]
     return dictionary


@app.post("/api/insert", status_code=HTTP_201_CREATED)
def insert(user_data:UserSchema, authenticated: Annotated[str, Depends(get_current_username)]):
    data = user_data.model_dump()
    data.pop("id")
    print(data)
    conn.write(data)


@app.put("/api/update/{id}", status_code=HTTP_204_NO_CONTENT)
def update(user_data:UserSchema, id:str, authenticated: Annotated[str, Depends(get_current_username)]):
    data = user_data.model_dump()
    data["id"] = id
    conn.update(data)
 

@app.delete("/api/delete/{id}", status_code=HTTP_204_NO_CONTENT)
def delete(id:str, authenticated: Annotated[str, Depends(get_current_username)]):
    conn.delete(id)