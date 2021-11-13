from typing import List, Tuple

from databases import Database
from fastapi import Depends, FastAPI, HTTPException, Query, status

from database import get_database, sqlalchemy_engine

from models import (
    metadata,
    employees,
    managers,
    roles,
    PostDB,
    EmployeeCreate,
    ManagerCreate,
    RoleCreate,
    PostPartialUpdate,
)

app = FastAPI()

#! Create and start db
@app.on_event("startup")
async def startup():
    await get_database().connect()
    metadata.create_all(sqlalchemy_engine)


#! Shutdown db
@app.on_event("shutdown")
async def shutdown():
    await get_database().disconnect()

#& Not in use
async def pagination(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0),
) -> Tuple[int, int]:
    capped_limit = min(100, limit)
    return (skip, capped_limit)


#& Not in use
async def get_post_or_404(
    id: int, database: Database = Depends(get_database)
) -> PostDB:
    select_query = posts.select().where(posts.c.id == id)
    raw_post = await database.fetch_one(select_query)

    if raw_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return PostDB(**raw_post)


#& Not in use
@app.get("/posts")
async def list_posts(
    pagination: Tuple[int, int] = Depends(pagination),
    database: Database = Depends(get_database),
) -> List[PostDB]:
    skip, limit = pagination
    select_query = posts.select().offset(skip).limit(limit)
    rows = await database.fetch_all(select_query)
    results = [PostDB(**row) for row in rows]

    return results







#& Not in use
@app.get("/posts/{id}", response_model=PostDB)
async def get_post(post: PostDB = Depends(get_post_or_404)) -> PostDB:
    return post

#! List the roles
@app.get("/roles")
async def list_roles(database: Database = Depends(get_database),):
    '''
    This function will lists all of the roles in the database
    '''
    select_query = roles.select()
    rows = await database.fetch_all(select_query)
    return rows


#! Create Records
#! Create Records
@app.post("/employee", status_code=status.HTTP_201_CREATED)
async def create_employee(employee: EmployeeCreate, database: Database = Depends(get_database)):
    '''
    This function will create an employee
    '''
    insert_query = employees.insert().values(employee.dict())
    await database.execute(insert_query) 
    #! put in an error message in here
    if True:
        message = "Employee added"
    else:
        message = "Try again"
    return message


@app.post("/managers", status_code=status.HTTP_201_CREATED)
async def create_manager(manager: ManagerCreate, database: Database = Depends(get_database)):
    '''
    This function will create a manager group
    '''
    print(manager.dict())
    insert_query = managers.insert().values(manager.dict())
    await database.execute(insert_query)
    #! put in an error message in here
    if True:
        message = "Manager added"
    else:
        message = "Try again"
    return message


@app.post("/roles", status_code=status.HTTP_201_CREATED)
async def create_roles(role: RoleCreate, database: Database = Depends(get_database)):
    '''
    This function will create a role
    '''
    print(role.dict())
    insert_query = roles.insert().values(role.dict())
    await database.execute(insert_query)
    #! put in an error message in here
    if True:
        message = "Role added"
    else:
        message = "Try again"
    return message




#! Change Records
#! Change Records
#& Not in use
@app.patch("/posts/{id}", response_model=PostDB)
async def update_post(
    post_update: PostPartialUpdate,
    post: PostDB = Depends(get_post_or_404),
    database: Database = Depends(get_database),
) -> PostDB:
    update_query = (
        posts.update()
        .where(posts.c.id == post.id)
        .values(post_update.dict(exclude_unset=True))
    )
    post_id = await database.execute(update_query)

    post_db = await get_post_or_404(post_id, database)

    return post_db

#! Delete Records
#! Delete Records
#& Not in use
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post: PostDB = Depends(get_post_or_404), database: Database = Depends(get_database)
):
    delete_query = posts.delete().where(posts.c.id == post.id)
    await database.execute(delete_query)
