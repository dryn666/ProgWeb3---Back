# products/product_controller.py

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from typing import List
from database import SessionLocal
from . import product_service, product_model

router = APIRouter(prefix="/products", tags=["products"])

# Esta função é a nossa "Injeção de Dependência".
# O FastAPI vai chamá-la para cada requisição que precisar de uma sessão com o banco.
# A palavra 'yield' entrega a sessão para a rota e, quando a rota termina,
# o código após o 'yield' (db.close()) é executado, garantindo que a conexão seja fechada.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=product_model.UserPublic, status_code=status.HTTP_201_CREATED)
def create_product(product: product_model.UserCreate, db: Session = Depends(get_db)):
    """Endpoint para criar um novo usuário. Recebe os dados validados (product)
    e a sessão do banco (db) através da injeção de dependência."""
    return product_service.create_new_product(db=db, product=product)

@router.get("/", response_model=List[product_model.UserPublic])
def read_products(db: Session = Depends(get_db)):
    """Endpoint para listar todos os usuários."""
    return product_service.get_all_products(db)

@router.get("/{product_id}", response_model=product_model.UserPublic)
def read_product(product_id: int, db: Session = Depends(get_db)):
    """Endpoint para buscar um usuário pelo ID."""
    return product_service.get_product_by_id(db, product_id=product_id)

@router.put("/{product_id}", response_model=product_model.UserPublic)
def update_product(product_id: int, product: product_model.UserUpdate, db: Session = Depends(get_db)):
    """Endpoint para atualizar um usuário."""
    return product_service.update_existing_product(db=db, product_id=product_id, product_in=product)

@router.delete("/{product_id}", response_model=product_model.UserPublic)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Endpoint para deletar um usuário."""
    return product_service.delete_product_by_id(db=db, product_id=product_id)
