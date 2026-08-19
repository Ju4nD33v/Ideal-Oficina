from fastapi import APIRouter, HTTPException
from mysql.connector import Error

from api.schemas import OrdemServicoCreate, StatusUpdate
from database.conexao import conectar

router = APIRouter(prefix="/api/ordens-servico", tags=["Ordens de serviço"])


@router.get("")
def listar_ordens():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT
                os.id,
                os.data_emissao,
                os.valor,
                os.status,
                os.data_conclusao,
                os.ordem_veiculo AS veiculo_id,
                v.modelo AS veiculo_modelo,
                v.placa_veiculo AS placa,
                os.ordem_mecanico AS mecanico_id,
                m.nome AS mecanico_nome,
                s.serviços_solicitados AS servico,
                mo.descriçao AS mao_de_obra,
                mo.valor AS valor_mao_de_obra
            FROM `ordem_de_serviço` os
            INNER JOIN veiculo_cliente v ON v.id = os.ordem_veiculo
            INNER JOIN equipe_mecanico m ON m.id = os.ordem_mecanico
            LEFT JOIN `serviços_os` so ON so.id_ordem = os.id
            LEFT JOIN `serviços` s ON s.id = so.id_serviços
            LEFT JOIN mao_de_obra mo ON mo.id = s.mao_de_obra_do_serviço
            ORDER BY os.id DESC
            """
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conexao.close()


@router.post("", status_code=201)
def criar_ordem(dados: OrdemServicoCreate):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id FROM veiculo_cliente WHERE id = %s", (dados.veiculo_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Veículo não encontrado.")

        cursor.execute("SELECT id FROM equipe_mecanico WHERE id = %s", (dados.mecanico_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Mecânico não encontrado.")

        cursor.execute(
            "SELECT id, `valor_peça` FROM `tabela_peças` WHERE id = %s",
            (dados.peca_id,),
        )
        peca = cursor.fetchone()
        if not peca:
            raise HTTPException(status_code=404, detail="Peça não encontrada.")

        # O seu banco relaciona mão de obra -> serviço -> ordem de serviço.
        cursor.execute(
            """
            INSERT INTO mao_de_obra (`valor`, `descriçao`)
            VALUES (%s, %s)
            """,
            (dados.valor_mao_de_obra, dados.mao_de_obra.strip()),
        )
        id_mao_de_obra = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO `serviços` (`serviços_solicitados`, `mao_de_obra_do_serviço`)
            VALUES (%s, %s)
            """,
            (dados.mao_de_obra.strip(), id_mao_de_obra),
        )
        id_servico = cursor.lastrowid

        valor_total = float(dados.valor_mao_de_obra) + float(peca["valor_peça"])

        cursor.execute(
            """
            INSERT INTO `ordem_de_serviço`
            (data_emissao, valor, status, data_conclusao, ordem_veiculo, ordem_mecanico)
            VALUES (CURDATE(), %s, %s, %s, %s, %s)
            """,
            (
                valor_total,
                dados.status.strip(),
                dados.data_conclusao,
                dados.veiculo_id,
                dados.mecanico_id,
            ),
        )
        os_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO `serviços_os` (id_serviços, id_ordem) VALUES (%s, %s)",
            (id_servico, os_id),
        )
        cursor.execute(
            "INSERT INTO `peças_na_os` (id_peças, id_ordem) VALUES (%s, %s)",
            (dados.peca_id, os_id),
        )

        conexao.commit()

        return {
            "id": os_id,
            "valor": valor_total,
            "message": "Ordem de serviço criada com sucesso.",
        }
    except HTTPException:
        conexao.rollback()
        raise
    except Error as exc:
        conexao.rollback()
        raise HTTPException(status_code=400, detail=f"Não foi possível criar a OS: {exc}") from exc
    finally:
        cursor.close()
        conexao.close()


@router.patch("/{os_id}/status")
def atualizar_status(os_id: int, dados: StatusUpdate):
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "UPDATE `ordem_de_serviço` SET status = %s WHERE id = %s",
            (dados.status.strip(), os_id),
        )
        if cursor.rowcount == 0:
            conexao.rollback()
            raise HTTPException(status_code=404, detail="Ordem de serviço não encontrada.")
        conexao.commit()
        return {"message": "Status atualizado com sucesso."}
    except HTTPException:
        raise
    except Error as exc:
        conexao.rollback()
        raise HTTPException(status_code=400, detail=f"Não foi possível atualizar o status: {exc}") from exc
    finally:
        cursor.close()
        conexao.close()
