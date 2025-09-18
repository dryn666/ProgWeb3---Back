from sqlalchemy.orm import Session
from . import product_models

# --- FUNÇÕES DE LEITURA (READ) ---
def get_product(db: Session, product_id: int):
    """
    Busca um único produto pelo seu ID.
    """
    return db.query(product_models.Product).filter(product_models.Product.id == product_id).first()

def get_products(db: Session):
    """
    Busca todos os produtos cadastrados no banco de dados.
    """
    return db.query(product_models.Product).all()

# --- FUNÇÃO DE CRIAÇÃO (CREATE) ---
def create_product(db: Session, product: product_models.ProductCreate):
    """
    Cria um novo produto no banco de dados.
    """
    db_product = product_models.Product(
        name=product.name,
        price=product.price,
        quantity=product.quantity,
        description=product.description,
    )

    db.add(db_product)       # Adiciona o objeto à sessão
    db.commit()              # Persiste as mudanças no banco
    db.refresh(db_product)   # Atualiza com os dados do banco (inclui ID)
    return db_product

# --- FUNÇÃO DE ATUALIZAÇÃO (UPDATE) ---
def update_product(db: Session, db_product: product_models.Product, product_in: product_models.ProductUpdate):
    """
    Atualiza os dados de um produto existente.
    """
    update_data = product_in.model_dump(exclude_unset=True)  # Apenas campos enviados
    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# --- FUNÇÃO DE DELEÇÃO (DELETE) ---
def delete_product(db: Session, db_product: product_models.Product):
    """
    Deleta um produto do banco de dados.
    """
    db.delete(db_product)
    db.commit()
    return db_product
