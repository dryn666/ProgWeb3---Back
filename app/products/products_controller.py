# app/products/controller.py
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, status

from app.products.products_models import ProductCreate, ProductUpdate, ProductPublic

router = APIRouter(prefix="/products", tags=["Products"])

# "Banco" em memória
fake_db: Dict[int, Dict[str, Any]] = {
    1: {"id": 1, "name": "Teclado Mecânico", "price": 299.9, "quantity": 15, "description": "Switch blue"},
    2: {"id": 2, "name": "Mouse Gamer", "price": 159.9, "quantity": 40, "description": "8000 DPI"},
}

@router.post("/", response_model=ProductPublic, status_code=status.HTTP_201_CREATED)
def create_product(prod: ProductCreate):
    new_id = (max(fake_db.keys()) + 1) if fake_db else 1
    data = prod.model_dump()
    data["id"] = new_id
    fake_db[new_id] = data
    return ProductPublic(**data)

@router.get("/", response_model=list[ProductPublic])
def list_products():
    return [ProductPublic(**p) for p in fake_db.values()]

@router.put("/{product_id}", response_model=ProductPublic)
def update_product(product_id: int, prod_update: ProductUpdate):
    if product_id not in fake_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    stored = fake_db[product_id]
    changes = prod_update.model_dump(exclude_unset=True)
    updated = {**stored, **changes}
    fake_db[product_id] = updated
    return ProductPublic(**updated)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    if product_id not in fake_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    del fake_db[product_id]
    # 204: sem corpo
