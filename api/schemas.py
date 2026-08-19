from datetime import date

from pydantic import BaseModel, Field


class ClienteCreate(BaseModel):
    nome: str = Field(min_length=2, max_length=45)
    telefone: str = Field(min_length=8, max_length=45)
    endereco: str = Field(min_length=2, max_length=45)


class VeiculoCreate(BaseModel):
    modelo: str = Field(min_length=2, max_length=45)
    cor: str = Field(min_length=2, max_length=45)
    ano: str = Field(min_length=4, max_length=45)
    problema: str = Field(min_length=2, max_length=150)
    dono_veiculo: int = Field(gt=0)
    placa: str = Field(min_length=2, max_length=45)


class MecanicoCreate(BaseModel):
    nome: str = Field(min_length=2, max_length=45)
    endereco: str = Field(min_length=2, max_length=45)
    especialidade: str = Field(min_length=2, max_length=45)


class PecaCreate(BaseModel):
    nome: str = Field(min_length=2, max_length=45)
    valor: float = Field(ge=0)
    garantia: str = Field(min_length=1, max_length=45)
    descricao: str = Field(min_length=2, max_length=45)


class OrdemServicoCreate(BaseModel):
    veiculo_id: int = Field(gt=0)
    mecanico_id: int = Field(gt=0)
    peca_id: int = Field(gt=0)
    status: str = Field(min_length=2, max_length=45)
    data_conclusao: date
    mao_de_obra: str = Field(min_length=2, max_length=45)
    valor_mao_de_obra: float = Field(ge=0)


class StatusUpdate(BaseModel):
    status: str = Field(min_length=2, max_length=45)
