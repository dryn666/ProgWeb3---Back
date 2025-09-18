from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import product_repository, product_models

def create_new_product(db: Session, product: product_models.ProductCreate):
    """Serviço para criar um novo produto com regra de negócio."""
    # REGRA DE NEGÓCIO: não permitir nome duplicado
    existing = db.query(product_models.Product).filter(
        product_models.Product.name == product.name
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product name already registered",
        )

    return product_repository.create_product(db=db, product=product)

def get_all_products(db: Session):
    """Serviço para listar todos os produtos."""
    return product_repository.get_products(db)

def get_product_by_id(db: Session, product_id: int):
    """Serviço para buscar um produto pelo ID, com tratamento de erro."""
    db_product = product_repository.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return db_product

def update_existing_product(db: Session, product_id: int, product_in: product_models.ProductUpdate):
    """Serviço para atualizar um produto, com tratamento de erro."""
    db_product = get_product_by_id(db, product_id)  # valida existência

    # Se estiver alterando o nome, checa duplicidade
    if product_in.name is not None:
        exists = db.query(product_models.Product).filter(
            product_models.Product.name == product_in.name,
            product_models.Product.id != product_id,
        ).first()
        if exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Another product with this name already exists",
            )

    return product_repository.update_product(db=db, db_product=db_product, product_in=product_in)

def delete_product_by_id(db: Session, product_id: int):
    """Serviço para deletar um produto, com tratamento de erro."""
    db_product = get_product_by_id(db, product_id)  # valida existência
    return product_repository.delete_product(db=db, db_product=db_product)
