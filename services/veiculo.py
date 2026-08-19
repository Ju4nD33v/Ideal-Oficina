from database.conexao import conectar


def cadastrar_veiculo(dono_veiculo):
    modelo = input('Informe o modelo e a marca do veiculo: ').strip()
    cor = input('Informe a cor do veiculo: ').strip()
    ano = input('Informe o ano do veiculo: ').strip()
    placa = input('Informe a placa do veiculo: ').strip()
    problema = input('Qual o problema apresentado: ').strip()

    if not all([modelo, cor, ano, placa, problema]):
        print('Todos os campos devem ser preenchidos.')
        return

    conexao = conectar()
    cursor = conexao.cursor()
    try:
        sql = """
            INSERT INTO veiculo_cliente
            (modelo, cor, ano, problema_apresentado, dono_veiculo, placa_veiculo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (modelo, cor, ano, problema, dono_veiculo, placa))
        conexao.commit()
        print('Serviço solicitado!!')
    finally:
        cursor.close()
        conexao.close()


def escolher_veiculo():
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT id, modelo, ano, problema_apresentado, placa_veiculo
            FROM veiculo_cliente
        """)
        veiculos = cursor.fetchall()

        if not veiculos:
            print('Nenhum veiculo cadastrado!!')
            return None

        print('----------Veiculos disponiveis----------')
        for i, veiculo in enumerate(veiculos, start=1):
            print(
                f'{i} - {veiculo[1]} | Ano:{veiculo[2]} | '
                f'Placa:{veiculo[4]} | Problema Apresentado: {veiculo[3]}'
            )

        try:
            escolha = int(input('Escolha um veiculo: '))
        except ValueError:
            print('Digite um número válido.')
            return None

        if escolha < 1 or escolha > len(veiculos):
            print('Escolha invalida!')
            return None

        veiculo_escolhido = veiculos[escolha - 1]
        print(f"\nVeículo selecionado: {veiculo_escolhido[1]}")
        print(f"Placa: {veiculo_escolhido[4]}")
        print(f"ID do veículo: {veiculo_escolhido[0]}")
        return veiculo_escolhido[0]
    finally:
        cursor.close()
        conexao.close()
