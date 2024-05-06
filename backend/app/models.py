from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

# Shared properties
# TODO replace email str with EmailStr when sqlmodel supports it
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# TODO replace email str with EmailStr when sqlmodel supports it
class UserRegister(SQLModel):
    email: str
    password: str
    full_name: str | None = None


# Properties to receive via API on update, all are optional
# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdate(UserBase):
    email: str | None = None  # type: ignore
    password: str | None = None


# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdateMe(SQLModel):
    full_name: str | None = None
    email: str | None = None


class UpdatePassword(SQLModel):
    current_password: str
    new_password: str


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner")


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str
    description: str | None = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str
    wholesale_price: int = 0
    retail_price: int = 0


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = None  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    wholesale_price: int = 0
    retail_price: int = 0
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="items")

    warehouses: list["WareHouseItems"] = Relationship(back_populates="item")

# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: int
    owner_id: int


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str

# Properties to receive via API on creation
class WareHouseAddItems(SQLModel):
    quantity: int = 0
    

class WareHouseItemsBase(SQLModel):
    id: int
    quantity: int     

class WareHouseItems(WareHouseAddItems, table=True):
    id: int | None = Field(default=None, primary_key=True)

    item_id: int | None = Field(default=None, foreign_key="item.id", nullable=False)
    item: Item | None = Relationship(back_populates="warehouses")
    

# Properties to receive on item update
class WareHouseItemsUpdate(WareHouseItemsBase):
    title: str | None = None  # type: ignore    

# Properties to return via API, id is always required
class WareHousePublic(SQLModel):
    id: int
    quantity: int

class WareHousePublicList(SQLModel):
    id: int
    quantity: int
    # item_name: str

class WareHouseItemsPublic(SQLModel):
    data: list[WareHousePublicList]
    count: int

# class StoreAdd(SQLModel):
#     location: str = ""

# class Store(StoreAdd, table=True):
#     id: int | None = Field(default=None, primary_key=True)

# class StoreItems(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     store_id: int | None = Field(default=None, foreign_key="store.id", nullable=False)
#     store: Store | None = Relationship(back_populates="items")

#     item_id: int | None = Field(default=None, foreign_key="item.id", nullable=False)
#     item: Item | None = Relationship(back_populates="items")

#     quantity: int = 0

    


# class Purchase(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)

#     item_id: int | None = Field(default=None, foreign_key="item.id", nullable=False)
#     item: Item | None = Relationship(back_populates="items")

#     quantity: int = 0
#     purchased_at: datetime = datetime.now()
