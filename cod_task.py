import config


def pontuacao():
    print("\033[37m-=-\033[m" * 30)


def visualizar(resultado):
    pontuacao()
    conexao = config.conectar()
    cursor = conexao.cursor()
    query = f"""
    select t.id, t.nome, t.descricao, t.data_inicio, t.data_fim, t.status_tarefa from usuario_recebe_tarefa urt left join usuarios u on urt.id_usuario = u.id left join tarefas t on urt.id_tarefa = t.id where urt.id_usuario = '{resultado[0][0]}';
    """
    cursor.execute(query)
    resultado_visualizar = cursor.fetchall()
    cursor.close()
    config.desconectar(conexao)

    for pos_linha, linha in enumerate(resultado_visualizar):
        print(f"\033[1;35m\n{pos_linha+1}º Tarefa:")
        for pos_campo, campo in enumerate(linha):
            if pos_campo == 0:
                print(f"ID: {campo}")
            elif pos_campo == 1:
                print(f"Nome: {campo}")
            elif pos_campo == 2:
                print(f"Descrição: {campo}")
            elif pos_campo == 3:
                print(f"Data Início: {campo}")
            elif pos_campo == 4:
                print(f"Data Fim: {campo}")
            elif pos_campo == 5:
                print(f"Status: {campo}")

    return resultado_visualizar


def nova_tarefa(resultado):
    pontuacao()
    nome_tarefa = str(input("\033[1;35mDigite o nome da tarefa: \033[1;32m"))
    descricao = str(input("\033[1;35mDigite a descrição da tarefa: \033[1;32m"))
    data_inicio = str(input("\033[1;35mDigite a data de início no formato (ano-mes-dia): \033[1;32m"))
    data_fim = str(input("\033[1;35mDigite a data de fim no formato (ano-mes-dia): \033[1;32m"))
    status_tarefa = str(input("\033[1;35mDigite o status da tarefa (Pendente, Andamento ou Finalizado): \033[1;32m"))
    query_tarefa = f"""
    insert into tarefas (nome, descricao, data_inicio, data_fim, status_tarefa) values ('{nome_tarefa}', '{descricao}', '{data_inicio}', '{data_fim}', '{status_tarefa}');
    """
    conexao = config.conectar()
    cursor = conexao.cursor()
    cursor.execute(query_tarefa)
    conexao.commit()

    query_ultima_linha = """
    SELECT * FROM tarefas ORDER BY id DESC LIMIT 1;
    """
    cursor.execute(query_ultima_linha)
    resultado_ultima_linha = cursor.fetchall()
    id_tarefa_criada = resultado_ultima_linha[0][0]

    query_usuario_recebe_tarefa = f"""
    insert into usuario_recebe_tarefa (id_usuario, id_tarefa) values ('{resultado[0][0]}', '{id_tarefa_criada}');
    """
    cursor.execute(query_usuario_recebe_tarefa)
    conexao.commit()
    cursor.close()
    config.desconectar(conexao)
    print(f"\033[1;35m\n{resultado[0][1]} sua tarefa foi criada com sucesso!\033[m")


def alterar_tarefa(resultado):
    resultado_visualizar = visualizar(resultado)

    pontuacao()

    lista_ids = list()

    for linha in resultado_visualizar:
        lista_ids.append(linha[0])

    while True:
        tarefa_alterar = input("\033[1;35mDigite o ID da tarefa que deseja alterar: \033[1;32m")

        try:
            tarefa_alterar = int(tarefa_alterar)
        except:
            erro_conversao = "Id não foi possível converter para int"

        if tarefa_alterar not in lista_ids:
            print('\033[1;31mEssa tarefa não existe...favor digitar novamente!\033[m')

        else:
            pontuacao()
            print("\033[1;35m\nO que deseja alterar?\033[1;32m")
            novo_nome_tarefa = str(input("\033[1;35mDigite o novo nome da tarefa [0 para não alterar]: \033[1;32m"))
            novo_descricao = str(input("\033[1;35mDigite a nova descrição da tarefa [0 para não alterar]: \033[1;32m"))
            novo_data_inicio = str(input("\033[1;35mDigite a nova data de início no formato (ano-mes-dia) [0 para não alterar]: \033[1;32m"))
            novo_data_fim = str(input("\033[1;35mDigite a nova data de fim no formato (ano-mes-dia) [0 para não alterar]: \033[1;32m"))
            novo_status_tarefa = str(input("\033[1;35mDigite o novo status da tarefa (Pendente, Andamento ou Finalizado) [0 para não alterar]: \033[1;32m"))

            conexao = config.conectar()
            cursor = conexao.cursor()

            try:
                query_alteracao = f"""
                    UPDATE tarefas
                    SET nome = CASE WHEN '{novo_nome_tarefa}' != '0' THEN '{novo_nome_tarefa}' ELSE nome END,
                        descricao = CASE WHEN '{novo_descricao}' != '0' THEN '{novo_descricao}' ELSE descricao END,
                        data_inicio = CASE WHEN '{novo_data_inicio}' != '0' THEN '{novo_data_inicio}' ELSE data_inicio END,
                        data_fim = CASE WHEN '{novo_data_fim}' != '0' THEN '{novo_data_fim}' ELSE data_fim END,
                        status_tarefa = CASE WHEN '{novo_status_tarefa}' != '0' THEN '{novo_status_tarefa}' ELSE status_tarefa END
                    WHERE id = '{tarefa_alterar}'
                """
                cursor.execute(query_alteracao)
                conexao.commit()
                cursor.close()
                config.desconectar(conexao)

                print("\033[1;35mAlterações na tarefa foram realizadas com sucesso!\033[m")

            except:
                print("\033[1;31mNão foi possível realizar as alterações...por favor tente novamente!\033[m")

            break


def deletar(resultado):
    resultado_visualizar = visualizar(resultado)

    pontuacao()

    lista_ids = list()

    for linha in resultado_visualizar: 
        lista_ids.append(linha[0])

    while True:
        tarefa_deletar = input("\033[1;35mDigite o ID da tarefa que deseja alterar: \033[1;32m")

        try:
            tarefa_deletar = int(tarefa_deletar)
        except:
            erro_conversao = "Id não foi possível converter para int"

        if tarefa_deletar not in lista_ids:
            print('\033[1;31mEssa tarefa não existe...favor digitar novamente!\033[m')

        else:
            pontuacao()

            conexao = config.conectar()
            cursor = conexao.cursor()

            try:
                query_deletar_urt = f"delete from usuario_recebe_tarefa where id_tarefa = '{tarefa_deletar}'"
                cursor.execute(query_deletar_urt)
                conexao.commit()

                query_deletar_tarefa = f"delete from tarefas where id = '{tarefa_deletar}'"
                cursor.execute(query_deletar_tarefa)
                conexao.commit()

                cursor.close()
                config.desconectar(conexao)

                print("\033[1;35mTarefa deletada com sucesso!\033[m")

            except:
                print("\033[1;31mNão foi possível deletar a tarefa...por favor tente novamente!\033[m")

            break


def login():
    pontuacao()
    print("\033[1;35mBem vindo(a) ao App Lista de Tarefas!\033[m")
    pontuacao()
    resultado = ''
    while True:
        usuario = str(input("\033[1;35mDigite seu usuário: \033[1;32m"))
        senha = str(input("\033[1;35mDigite sua senha: \033[1;32m"))
        conexao = config.conectar()
        cursor = conexao.cursor()
        query = f"select * from usuarios where usuario = '{usuario}' and senha = '{senha}'"
        cursor.execute(query)
        resultado = cursor.fetchall()
        cursor.close()
        config.desconectar(conexao)

        if len(resultado) == 0:
            print("\033[1;31mAlgo está errado com as credenciais...tente novamente!\033[m")
        else:
            break

    return resultado


def introducao():
    continuar = ""
    resultado = login()
    pontuacao()
    print(f"\033[1;35mOlá, {resultado[0][1]}!\033[m")
    pontuacao()
    while True:
        print("\033[1;35m[ 1 ] Visualizar minhas tarefas")
        print("[ 2 ] Criar nova tarefa")
        print("[ 3 ] Alterar uma tarefa")
        print("[ 4 ] Deletar uma tarefa\033[m")
        pontuacao()
        opcao = int(input("\033[1;35mDigite sua opção: \033[1;32m"))

        if opcao == 1:
            visualizar(resultado)

        elif opcao == 2:
            nova_tarefa(resultado)

        elif opcao == 3:
            alterar_tarefa(resultado)

        elif opcao == 4:
            deletar(resultado)

        pontuacao()
        continuar = str(input("\033[1;35mDeseja continuar? [S/N]: \033[1;32m"))
        pontuacao()

        if continuar.upper() in ["N", "NÃO", "NAO"]:
            pontuacao()
            print("\033[1;35mPrograma finalizado!!!\033[m")
            pontuacao()
            break


introducao()
