from datetime import date, datetime
from database.conexao import conectar


def ler_data():
    while True:
        data = input('Informe a data para a conclusão (Ex: 00/00/0000): ').strip()
        try:
            return datetime.strptime(data, '%d/%m/%Y').date()
        except ValueError:
            print('Data inválida. Use o formato DD/MM/AAAA.')


def criar_ordem_servico(id_veiculo, id_mecanico, valor_pecas):
    status = input('Informe o status atual da ordem de serviço: ').strip()
    data_conclusao = ler_data()
    mao_de_obra = input('Informe qual será o serviço realizado: ').strip()

    try:
        valor_mao_de_obra = float(input('Informe qual o valor da mão de obra: ').replace(',', '.'))
    except ValueError:
        print('Informe um valor válido.')
        return

    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            'INSERT INTO mao_de_obra (valor, descricao) VALUES (%s, %s)',
            (valor_mao_de_obra, mao_de_obra)
        )

        id_mao_de_obra = cursor.lastrowid
        valor_os = valor_mao_de_obra + float(valor_pecas)

        sql = """
            INSERT INTO ordem_de_servico
            (data_emissao, valor, status, data_conclusao,
             ordem_veiculo, ordem_mecanico, ordem_mao_de_obra)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            sql,
            (
                date.today(),
                valor_os,
                status,
                data_conclusao,
                id_veiculo,
                id_mecanico,
                id_mao_de_obra
            )
        )

        conexao.commit()
        id_os = cursor.lastrowid

        print('Ordem de serviço cadastrada com sucesso!!')
        print('----------Ordem de Serviço----------')
        print(f'    Data da Emissão: {date.today()}')
        print(f'    Data de Conclusão: {data_conclusao}')
        print(f'    Status atual da OS: {status}')
        print(f'    Valor da OS: R$ {valor_os:.2f}')
        print(f'    Id do veiculo: {id_veiculo} | Id mecanico: {id_mecanico}')
        print(f'    Codigo da OS: {id_os}')
    except Exception:
        conexao.rollback()
        raise
    finally:
        cursor.close()
        conexao.close()


def escolher_os():
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT id, data_emissao, valor, status, data_conclusao, ordem_veiculo
            FROM ordem_de_servico
            ORDER BY id
        """)
        ordens = cursor.fetchall()

        if not ordens:
            print('Nenhuma Ordem de Serviço cadastrada!!')
            return None

        print('-----Ordens de Serviço-----')
        for i, ordem in enumerate(ordens, start=1):
            print(
                f'{i} - id:{ordem[0]} | data de emissão:{ordem[1]} | '
                f'Valor:R$ {ordem[2]:.2f} | status:{ordem[3]} | '
                f'Veiculo Associado a OS: {ordem[5]}'
            )

        try:
            escolha = int(input('Qual Ordem deseja atualizar: '))
        except ValueError:
            print('Digite um número válido.')
            return None

        if escolha < 1 or escolha > len(ordens):
            print('Escolha invalida!')
            return None

        return ordens[escolha - 1][0]
    finally:
        cursor.close()
        conexao.close()


def atualizar_os(id_os):
    novo_status = input('Atualização do status da Ordem de Serviço: ').strip()

    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            'UPDATE ordem_de_servico SET status = %s WHERE id = %s',
            (novo_status, id_os)
        )
        conexao.commit()

        if cursor.rowcount:
            print('Ordem de Serviço atualizada com sucesso!!')
        else:
            print('Ordem de Serviço não encontrada.')
    finally:
        cursor.close()
        conexao.close()


def consultar_status():
    placa = input("Digite a placa do veículo: ").strip()

    conexao = conectar()
    cursor = conexao.cursor()
    try:
        sql = """
            SELECT vc.placa_veiculo, vc.modelo, vc.ano, vc.cor,
                   os.id, os.data_emissao, os.data_conclusao,
                   os.valor, os.status
            FROM veiculo_cliente vc
            INNER JOIN ordem_de_servico os
                ON vc.id = os.ordem_veiculo
            WHERE vc.placa_veiculo = %s
            ORDER BY os.id DESC
            LIMIT 1
        """
        cursor.execute(sql, (placa,))
        resultado = cursor.fetchone()

        if resultado:
            print("\n========== ORDEM DE SERVIÇO ==========")
            print(f"Veículo: {resultado[1]}")
            print(f"Placa: {resultado[0]}")
            print(f"Ano: {resultado[2]}")
            print(f"Cor: {resultado[3]}")
            print(f"OS: {resultado[4]}")
            print(f"Data de emissão: {resultado[5]}")
            print(f"Data de conclusão: {resultado[6]}")
            print(f"Valor: R$ {resultado[7]:.2f}")
            print(f"Status: {resultado[8]}")

            if resultado[8].strip().lower() in ('concluída', 'concluida', 'finalizada', 'finalizado'):
                print("\n>>> Seu veículo já pode ser retirado.")
            else:
                print("\n>>> Seu veículo ainda está em manutenção.")
        else:
            print("\nNenhuma ordem de serviço encontrada para essa placa.")
    finally:
        cursor.close()
        conexao.close()
