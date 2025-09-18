from sqlalchemy import Column, Integer, String, Float
from pydantic import BaseModel, Field
from database import Base  # Importa a Base que criamos no projeto

# ==================================
# MODELO DA TABELA (SQLAlchemy)
# ==================================
# Esta classe define a estrutura da tabela 'products' no banco de dados.
class Product(Base):
    __tablename__ = "products"  # Nome da tabela no banco

    # Colunas da tabela
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), index=True, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    description = Column(String(500), nullable=True)

# ==================================
# SCHEMAS (Pydantic) - O CONTRATO DA API
# ==================================
# Estes schemas definem como os dados são recebidos e enviados pela API.

# Schema para os dados que o cliente envia ao CRIAR um produto
class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    price: float = Field(ge=0)
    quantity: int = Field(ge=0, description="Quantidade em estoque")
    description: str | None = Field(default=None, max_length=500)

# Schema para os dados que o cliente envia ao ATUALIZAR um produto
class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    price: float | None = Field(default=None, ge=0)
    quantity: int | None = Field(default=None, ge=0)
    description: str | None = Field(default=None, max_length=500)

# Schema para os dados que a API RETORNA ao cliente (público)
class ProductPublic(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    description: str | None = None
