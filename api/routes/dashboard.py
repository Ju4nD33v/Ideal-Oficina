from fastapi import APIRouter

from api.db import fetch_all

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("")
def dashboard():
    counts = fetch_all(
        """
        SELECT
            (SELECT COUNT(*) FROM cliente) AS clientes,
            (SELECT COUNT(*) FROM veiculo_cliente) AS veiculos,
            (SELECT COUNT(*) FROM equipe_mecanico) AS mecanicos,
            (SELECT COUNT(*) FROM `ordem_de_serviço`) AS ordens,
            (SELECT COUNT(*) FROM `tabela_peças`) AS pecas
        """
    )[0]

    status = fetch_all(
        """
        SELECT status, COUNT(*) AS quantidade
        FROM `ordem_de_serviço`
        GROUP BY status
        ORDER BY quantidade DESC
        """
    )

    recentes = fetch_all(
        """
        SELECT os.id, os.status, os.valor, os.data_emissao,
               v.modelo AS veiculo, v.placa_veiculo AS placa,
               c.nome AS cliente
        FROM `ordem_de_serviço` os
        INNER JOIN veiculo_cliente v ON v.id = os.ordem_veiculo
        INNER JOIN cliente c ON c.id = v.dono_veiculo
        ORDER BY os.id DESC
        LIMIT 6
        """
    )

    return {"totais": counts, "status": status, "recentes": recentes}
