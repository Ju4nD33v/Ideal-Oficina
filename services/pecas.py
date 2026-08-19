from database.conexao import conectar


def adicionar_peca():
    nome = input('Nome da Peça: ').strip()
    garantia = input('Tempo de Garantia: ').strip()
    descricao = input('Descrição da peça: ').strip()

    try:
        valor = float(input('Valor da Peça: ').replace(',', '.'))
    except ValueError:
        print('Informe um valor válido.')
        return

    conexao = conectar()
    cursor = conexao.cursor()
    try:
        sql = """
            INSERT INTO `tabela_peças`
            (`valor_peça`, tempo_garantia, `nome_peça`, `descriçao`)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (valor, garantia, nome, descricao))
        conexao.commit()
        print('Cadastro da peça realizado com sucesso')
    finally:
        cursor.close()
        conexao.close()


def consultar_pecas():
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT `nome_peça`, `valor_peça`, tempo_garantia, `descriçao`
            FROM `tabela_peças`
            ORDER BY `nome_peça`
        """)
        pecas = cursor.fetchall()

        if not pecas:
            print('Nenhuma peça cadastrada!!')
            return

        print("\n----------- PEÇAS DISPONÍVEIS ------------")
        for peca in pecas:
            print(f"\nPeça: {peca[0]}")
            print(f"Valor: R$ {peca[1]:.2f}")
            print(f"Tempo de garantia: {peca[2]}")
            print(f"Descrição: {peca[3]}")
            print("---------------------------------------")
    finally:
        cursor.close()
        conexao.close()


def escolher_peca():
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT id, `nome_peça`, `valor_peça`, `descriçao`, tempo_garantia
            FROM `tabela_peças`
            ORDER BY `nome_peça`
        """)
        pecas = cursor.fetchall()

        if not pecas:
            print('Nenhuma peça cadastrada!!')
            return None

        print('----------Peças disponiveis----------')
        for i, peca in enumerate(pecas, start=1):
            print(
                f'{i} - {peca[1]} | Valor:{peca[2]:.2f} | '
                f'Descrição:{peca[3]} | Tempo de Garantia:{peca[4]}'
            )

        try:
            escolha = int(input('Escolha a peça: '))
        except ValueError:
            print('Digite um número válido.')
            return None

        if escolha < 1 or escolha > len(pecas):
            print('Escolha invalida!')
            return None

        return pecas[escolha - 1][0]
    finally:
        cursor.close()
        conexao.close()
