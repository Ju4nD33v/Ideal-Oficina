import random

from fastapi import APIRouter, HTTPException
from mysql.connector import Error

from api.db import execute, fetch_all, fetch_one
from api.schemas import MecanicoCreate

router = APIRouter(prefix="/api/mecanicos", tags=["Mecânicos"])


@router.get("")
def listar_mecanicos():
    return fetch_all(
        """
        SELECT id, nome, `endereço` AS endereco, especialidade, codigo_mecanico
        FROM equipe_mecanico
        ORDER BY nome
        """
    )


@router.post("", status_code=201)
def criar_mecanico(dados: MecanicoCreate):
    codigo = random.randint(100000, 999999)

    try:
        mecanico_id = execute(
            """
            INSERT INTO equipe_mecanico
            (nome, `endereço`, especialidade, codigo_mecanico)
            VALUES (%s, %s, %s, %s)
            """,
            (dados.nome.strip(), dados.endereco.strip(), dados.especialidade.strip(), codigo),
        )
    except Error as exc:
        raise HTTPException(status_code=400, detail=f"Não foi possível cadastrar o mecânico: {exc}") from exc

    return {
        "id": mecanico_id,
        "codigo_mecanico": codigo,
        "message": "Mecânico cadastrado com sucesso.",
    }
