from pydantic import BaseModel, HttpUrl
from typing import Optional


class ProductBase(BaseModel):
    sku: str
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    active: Optional[bool] = None


class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True


class WebhookBase(BaseModel):
    url: HttpUrl
    event_type: str = "import.completed"
    enabled: bool = True


class WebhookCreate(WebhookBase):
    pass


class WebhookOut(WebhookBase):
    id: int

    class Config:
        orm_mode = True
