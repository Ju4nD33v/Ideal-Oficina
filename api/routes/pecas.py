from fastapi import APIRouter, HTTPException
from mysql.connector import Error

from api.db import execute, fetch_all
from api.schemas import PecaCreate

router = APIRouter(prefix="/api/pecas", tags=["Peças"])


@router.get("")
def listar_pecas():
    return fetch_all(
        """
        SELECT
            id,
            `nome_peça` AS nome,
            `valor_peça` AS valor,
            tempo_garantia AS garantia,
            `descriçao` AS descricao
        FROM `tabela_peças`
        ORDER BY `nome_peça`
        """
    )


@router.post("", status_code=201)
def criar_peca(dados: PecaCreate):
    try:
        peca_id = execute(
            """
            INSERT INTO `tabela_peças`
            (`valor_peça`, tempo_garantia, `nome_peça`, `descriçao`)
            VALUES (%s, %s, %s, %s)
            """,
            (dados.valor, dados.garantia.strip(), dados.nome.strip(), dados.descricao.strip()),
        )
    except Error as exc:
        raise HTTPException(status_code=400, detail=f"Não foi possível cadastrar a peça: {exc}") from exc

    return {"id": peca_id, "message": "Peça cadastrada com sucesso."}
