from fastapi import APIRouter, HTTPException, Query
from mysql.connector import Error

from api.db import execute, fetch_all, fetch_one
from api.schemas import ClienteCreate

router = APIRouter(prefix="/api/clientes", tags=["Clientes"])
legacy_router = APIRouter(prefix="/clientes", tags=["Clientes (compatibilidade)"])


@router.get("")
def listar_clientes(search: str = Query(default="", max_length=80)):
    if search.strip():
        termo = f"%{search.strip()}%"
        return fetch_all(
            """
            SELECT id, nome, telefone, `endereço` AS endereco
            FROM cliente
            WHERE nome LIKE %s OR telefone LIKE %s
            ORDER BY nome
            """,
            (termo, termo),
        )

    return fetch_all(
        "SELECT id, nome, telefone, `endereço` AS endereco FROM cliente ORDER BY nome"
    )


@router.get("/{cliente_id}")
def obter_cliente(cliente_id: int):
    cliente = fetch_one(
        "SELECT id, nome, telefone, `endereço` AS endereco FROM cliente WHERE id = %s",
        (cliente_id,),
    )
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return cliente


@router.post("", status_code=201)
def criar_cliente(dados: ClienteCreate):
    try:
        cliente_id = execute(
            """
            INSERT INTO cliente (nome, telefone, `endereço`)
            VALUES (%s, %s, %s)
            """,
            (dados.nome.strip(), dados.telefone.strip(), dados.endereco.strip()),
        )
    except Error as exc:
        raise HTTPException(status_code=400, detail=f"Não foi possível cadastrar o cliente: {exc}") from exc

    return {"id": cliente_id, "message": "Cliente cadastrado com sucesso."}


@legacy_router.get("/")
def obter_clientes_legacy():
    return listar_clientes()
