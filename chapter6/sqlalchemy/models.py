from datetime import datetime
from typing import Optional

import sqlalchemy
from pydantic import BaseModel, Field


class EmployeeBase(BaseModel):
    lastName: str
    firstName: str
    groupId: int
    roleId: int
    directReports: bool
class ManagerBase(BaseModel):
    groupId: int
    managerId: int
class RoleBase(BaseModel):
    roleId: int
    roleName: str




class PostPartialUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    pass
class ManagerCreate(ManagerBase):
    pass
class RoleCreate(RoleBase):
    pass


class PostDB(EmployeeBase):
    id: int


metadata = sqlalchemy.MetaData()


employees = sqlalchemy.Table(
    "employees",
    metadata,
    sqlalchemy.Column("employeeId", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("lastName", sqlalchemy.String(length=45), nullable=False),
    sqlalchemy.Column("firstName", sqlalchemy.String(length=45), nullable=False),
    sqlalchemy.Column("groupId", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("roleId", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("directReports", sqlalchemy.Boolean(), nullable=False),
)

managers = sqlalchemy.Table(
    "managers",
    metadata,
    sqlalchemy.Column("groupId", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("managerId", sqlalchemy.Integer),
)

roles = sqlalchemy.Table(
    "roles",
    metadata,
    sqlalchemy.Column("roleId", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("roleName", sqlalchemy.String(length=45), nullable=False),
)

