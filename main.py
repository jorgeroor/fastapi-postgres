from fastapi import FastAPI
from model.user_connection import UserConnection
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from schema.user_schema import UserSchema


app = FastAPI()
conn = UserConnection()


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
def insert(user_data:UserSchema):
    data = user_data.model_dump()
    data.pop("id")
    print(data)
    conn.write(data)


@app.put("/api/update/{id}", status_code=HTTP_204_NO_CONTENT)
def update(user_data:UserSchema, id:str):
    data = user_data.model_dump()
    data["id"] = id
    conn.update(data)
 

@app.delete("/api/delete/{id}", status_code=HTTP_204_NO_CONTENT)
def delete(id:str):
    conn.delete(id)