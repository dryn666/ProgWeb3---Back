from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    price: float = Field(ge=0)
    quantity: int = Field(ge=0, description="Quantidade em estoque")
    description: str | None = Field(default=None, max_length=500)

class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    price: float | None = Field(default=None, ge=0)
    quantity: int | None = Field(default=None, ge=0)
    description: str | None = Field(default=None, max_length=500)

class ProductPublic(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    description: str | None = None
