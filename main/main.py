from services.cliente import verificar_cliente, cadastrar_cliente
from services.mecanico import verificar_mecanico, cadastrar_mecanico
from services.veiculo import cadastrar_veiculo, escolher_veiculo
from services.pecas import adicionar_peca, consultar_pecas, escolher_peca
from services.ordem_servico import criar_ordem_servico, escolher_os, atualizar_os, consultar_status
from services.cliente import consultar_clientes


def menu_principal():
    print('+--------Menu--------+')
    print('|      Bem Vindo     |')
    print('|         a          |')
    print('|   Ideal Oficina    |')
    print('|                    |')
    print('| (1)Cliente         |')
    print('| (2)Mecanico        |')
    print('| (3)Sair            |')
    print('+--------------------+')


def menu_cliente():
    print('+----------Menu---------+')
    print('|                       |')
    print('| (1)Cliente Novo       |')
    print('| (2)Cliente Cadastrado |')
    print('| (3)Voltar             |')
    print('|                       |')
    print('+-----------------------+')


def menu_mecanico():
    print('+----------Menu----------+')
    print('|                        |')
    print('| (1)Mecanico Novo       |')
    print('| (2)Mecanico Cadastrado |')
    print('| (3)Voltar              |')
    print('|                        |')
    print('+------------------------+')



if __name__ == '__main__':
    while True:
        menu_principal()
        try:
            escolha_pessoa = int(input(''))
        except ValueError:
            print('Opção inválida.')
            continue
        if escolha_pessoa == 1:
            while True:
                menu_cliente()
                try:
                    escolha_cliente = int(input(''))
                except ValueError:
                    print('Opção inválida.')
                    continue
                if escolha_cliente == 1:
                    id_cliente = cadastrar_cliente()
                elif escolha_cliente == 2:
                    id_cliente = verificar_cliente()
                    if id_cliente is not None:
                        while True:
                            print('+--------------Menu---------------+')
                            print('|                                 |')
                            print('|       Qual sua solicitação      |')
                            print('|                                 |')
                            print('| (1)Cadastrar Veiculo            |')
                            print('| (2)Consultar status do veiculo  |')
                            print('| (3)Consultar Peças              |')
                            print('| (4)Voltar                       |')
                            print('+---------------------------------+')
                            try:
                                escolha = int(input(''))
                            except ValueError:
                                print('Opção inválida.')
                                continue
                            if escolha == 1:
                                cadastrar_veiculo(id_cliente)
                            elif escolha == 2:
                                consultar_status()
                            elif escolha == 3:
                                consultar_pecas()
                            elif escolha == 4:
                                break
                            else:
                                print('Opção inválida.')
                elif escolha_cliente == 3:
                    break
                else:
                    print('Opção inválida.')
        elif escolha_pessoa == 2:
            while True:
                menu_mecanico()
                try:
                    escolha_mecanico = int(input(''))
                except ValueError:
                    print('Opção inválida.')
                    continue
            
                if escolha_mecanico == 1:
                    cadastrar_mecanico()
            
                elif escolha_mecanico == 2:
                    id_mecanico = verificar_mecanico()
                    if id_mecanico is not None:
                        while True:
                            print('+-------------------Menu------------------+')
                            print('|                                         |')
                            print('| (1)Criar Ordem de Serviço               |')
                            print('| (2)Atualizar status da Ordem de Serviço |')
                            print('| (3)Consultar Peças                      |')
                            print('| (4)Adicionar Peças                      |')
                            print('| (5)Buscar contatos dos clientes         |')
                            print('| (6)Voltar                               |')
                            print('+-----------------------------------------+')

                            escolha = input('')
                            if escolha == '1':
                                id_veiculo = escolher_veiculo()
                
                                if id_veiculo is not None:
                                    valor_pecas = escolher_peca()
                                    if valor_pecas is not None:
                                        criar_ordem_servico(id_veiculo, id_mecanico, valor_pecas)
                
                            elif escolha == '2':
                                id_os = escolher_os()
                                if id_os is not None:
                                    atualizar_os(id_os)
                
                            elif escolha == '3':
                                consultar_pecas()
                
                            elif escolha == '4':
                                adicionar_peca()
                
                            elif escolha == '5':
                                consultar_clientes()

                            elif escolha == '6':
                                break
                            else:
                                print('Opção inválida.')
                elif escolha_mecanico == 3:
                    break
                else:
                    print('Opção inválida.')
        elif escolha_pessoa == 3:
            print('Volte Sempre, Ideal Mecanica Agradeçe a Preferencia !!')
            break
        else:
            print('Opção inválida.')
