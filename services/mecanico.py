import random
from database.conexao import conectar


def cadastrar_mecanico():
    while True:
        nome = input('Informe seu nome: ').strip()
        endereco = input('Informe seu endereço: ').strip()
        especialidade = input('Informe sua especialidade: ').strip()
        codigo = random.randint(100000, 999999)

        print('---Suas informações estão corretas?---')
        print(f'\n{nome}\n{endereco}\n{especialidade}')
        conf = input('(S/N)')

        if conf.lower() == 's':
            conexao = conectar()
            cursor = conexao.cursor()
            try:
                sql = """
                    INSERT INTO equipe_mecanico
                    (nome, endereço, especialidade, codigo_mecanico)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (nome, endereco, especialidade, codigo))
                conexao.commit()
                print('Cadastro realizado com sucesso')
                print('A oficina irá confirmar seus dados e cadastra-lo a equipe')
                print(f'\n!! ATENÇÃO SEU CODIGO É {codigo} GUARDE-O PARA PODER ACESSAR SEU USUARIO !!')
                return cursor.lastrowid
            finally:
                cursor.close()
                conexao.close()

        elif conf.lower() == 'n':
            print('\nVamos preencher os dados novamente.')
        else:
            print('\nOpção inválida. Digite S ou N.')


def verificar_mecanico():
    nome = input('Informe seu nome: ').strip()

    try:
        codigo = int(input('Informe seu codigo: '))
    except ValueError:
        print('O código deve conter apenas números!')
        return None

    conexao = conectar()
    cursor = conexao.cursor()
    try:
        sql = """
            SELECT id, nome, endereço, especialidade, codigo_mecanico
            FROM equipe_mecanico
            WHERE nome = %s AND codigo_mecanico = %s
        """
        cursor.execute(sql, (nome, codigo))
        mecanico = cursor.fetchone()

        if mecanico:
            print('\nMecânico encontrado!')
            print(f'Nome: {mecanico[1]}')
            print(f'Especialidade: {mecanico[3]}')
            return mecanico[0]

        print('\nMecânico não encontrado.')
        return None
    finally:
        cursor.close()
        conexao.close()
