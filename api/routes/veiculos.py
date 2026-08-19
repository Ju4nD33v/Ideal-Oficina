from fastapi import APIRouter, HTTPException
from mysql.connector import Error

from api.db import execute, fetch_all, fetch_one
from api.schemas import VeiculoCreate

router = APIRouter(prefix="/api/veiculos", tags=["Veículos"])


@router.get("")
def listar_veiculos():
    return fetch_all(
        """
        SELECT v.id, v.modelo, v.cor, v.ano, v.problema_apresentado AS problema,
               v.placa_veiculo AS placa, v.dono_veiculo,
               c.nome AS cliente_nome
        FROM veiculo_cliente v
        INNER JOIN cliente c ON c.id = v.dono_veiculo
        ORDER BY v.id DESC
        """
    )


@router.post("", status_code=201)
def criar_veiculo(dados: VeiculoCreate):
    if not fetch_one("SELECT id FROM cliente WHERE id = %s", (dados.dono_veiculo,)):
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    try:
        veiculo_id = execute(
            """
            INSERT INTO veiculo_cliente
            (modelo, cor, ano, problema_apresentado, dono_veiculo, placa_veiculo)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                dados.modelo.strip(),
                dados.cor.strip(),
                dados.ano.strip(),
                dados.problema.strip(),
                dados.dono_veiculo,
                dados.placa.strip().upper(),
            ),
        )
    except Error as exc:
        raise HTTPException(status_code=400, detail=f"Não foi possível cadastrar o veículo: {exc}") from exc

    return {"id": veiculo_id, "message": "Veículo cadastrado com sucesso."}
