from database.conexao import conectar


def cadastrar_cliente():
    while True:
        nome = input('Informe seu Nome: ').strip()
        telefone = input('Informe o telefone para contato: ').strip()
        endereco = input('Informe seu Endereço: ').strip()

        if not nome or not telefone or not endereco:
            print('Todos os campos devem ser preenchidos.')
            continue

        print('---Suas informações estão corretas?---')
        print(f'\n{nome}\n{telefone}\n{endereco}')
        conf = input('(S/N)')

        if conf.lower() == 's':
            conexao = conectar()
            cursor = conexao.cursor()
            try:
                sql = "INSERT INTO cliente (nome, telefone, endereço) VALUES (%s, %s, %s)"
                cursor.execute(sql, (nome, telefone, endereco))
                conexao.commit()
                print('Cadastro realizado com sucesso')
                return cursor.lastrowid
            finally:
                cursor.close()
                conexao.close()

        elif conf.lower() == 'n':
            print('\nVamos preencher os dados novamente.')
        else:
            print('\nOpção inválida. Digite S ou N.')


def verificar_cliente():
    nome = input('Informe seu nome: ').strip()
    telefone = input('Informe seu telefone: ').strip()

    conexao = conectar()
    cursor = conexao.cursor()
    try:
        sql = 'SELECT id, nome, telefone, endereço FROM cliente WHERE nome = %s AND telefone = %s'
        cursor.execute(sql, (nome, telefone))
        cliente = cursor.fetchone()

        if cliente:
            print('\nCliente encontrado!')
            print(f'Nome: {cliente[1]}')
            print(f'Telefone: {cliente[2]}')
            return cliente[0]

        print('\nCliente não encontrado.')
        return None
    finally:
        cursor.close()
        conexao.close()


def consultar_clientes():
    opcao = input("Deseja buscar pelo nome do cliente ou pela placa? ").strip().lower()

    conexao = conectar()
    cursor = conexao.cursor()
    try:
        if opcao == "nome":
            nome = input("Digite o nome do cliente: ").strip()
            sql = """
                SELECT cliente.nome, cliente.telefone, cliente.endereço,
                       veiculo_cliente.modelo, veiculo_cliente.ano,
                       veiculo_cliente.placa_veiculo
                FROM cliente
                INNER JOIN veiculo_cliente
                    ON cliente.id = veiculo_cliente.dono_veiculo
                WHERE cliente.nome = %s
            """
            cursor.execute(sql, (nome,))

        elif opcao == "placa":
            placa = input("Digite a placa do veículo: ").strip()
            sql = """
                SELECT cliente.nome, cliente.telefone, cliente.endereço,
                       veiculo_cliente.modelo, veiculo_cliente.ano,
                       veiculo_cliente.placa_veiculo
                FROM cliente
                INNER JOIN veiculo_cliente
                    ON cliente.id = veiculo_cliente.dono_veiculo
                WHERE veiculo_cliente.placa_veiculo = %s
            """
            cursor.execute(sql, (placa,))
        else:
            print("Opção inválida.")
            return

        resultados = cursor.fetchall()

        if not resultados:
            print("\nNenhum cliente ou veículo encontrado.")
            return

        for resultado in resultados:
            print("\n========== CLIENTE ==========")
            print(f"Nome: {resultado[0]}")
            print(f"Telefone: {resultado[1]}")
            print(f"Endereço: {resultado[2]}")
            print("\n========== VEÍCULO ==========")
            print(f"Modelo: {resultado[3]}")
            print(f"Ano: {resultado[4]}")
            print(f"Placa: {resultado[5]}")
    finally:
        cursor.close()
        conexao.close()
def listar_clientes():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    try:
        sql = "SELECT id, nome, telefone, endereço FROM cliente"
        cursor.execute(sql)

        clientes = cursor.fetchall()

        return clientes

    finally:
        cursor.close()
        conexao.close()