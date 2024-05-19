from PIL import Image
import mysql.connector


def conectar():
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123",
        database="lista_tarefas"
    )

    return con


def desconectar(con):
    con.close()

def login(usuario, senha):
    resultado = ''
    conexao = conectar()
    cursor = conexao.cursor()
    query = f"select * from usuarios where usuario = '{usuario}' and senha = '{senha}'"
    cursor.execute(query)
    resultado = cursor.fetchall()
    cursor.close()
    desconectar(conexao)

    if len(resultado) == 0:
        erro_credencial = "Algo está errado com as credenciais...tente novamente!"
        resultado = [0, erro_credencial]
        return resultado 
    else:
        resultado = [1, resultado]
        return resultado
    
def visualizar(resultado):
    conexao = conectar()
    cursor = conexao.cursor()
    query = f"""
    select t.id, t.nome, t.descricao, t.data_inicio, t.data_fim, t.status_tarefa from usuario_recebe_tarefa urt left join usuarios u on urt.id_usuario = u.id left join tarefas t on urt.id_tarefa = t.id where urt.id_usuario = '{resultado[1][0][0]}';
    """
    cursor.execute(query)
    resultado_visualizar = cursor.fetchall()
    cursor.close()
    desconectar(conexao)

    lista_tarefas = []

    for pos_linha, linha in enumerate(resultado_visualizar):
        lista_temp = []
        lista_temp.append(pos_linha+1)
        for pos_campo, campo in enumerate(linha):
            lista_temp.append(campo)
    
        lista_tarefas.append(lista_temp)

    return lista_tarefas
    

def nova_tarefa(resultado, nome_tarefa, descricao, data_inicio, data_fim, status_tarefa):
    resultado_nova_tarefa = []
    try:        
        query_tarefa = f"""
        insert into tarefas (nome, descricao, data_inicio, data_fim, status_tarefa) values ('{nome_tarefa}', '{descricao}', '{data_inicio}', '{data_fim}', '{status_tarefa}');
        """
        conexao = conectar()
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
        insert into usuario_recebe_tarefa (id_usuario, id_tarefa) values ('{resultado[1][0][0]}', '{id_tarefa_criada}');
        """
        cursor.execute(query_usuario_recebe_tarefa)
        conexao.commit()
        cursor.close()
        desconectar(conexao)
        resultado_nova_tarefa = [1, "Tarefa criada com sucesso!"]
        return resultado_nova_tarefa
    
    except:
        resultado_nova_tarefa = [0, "Erro ao criar tarefa...tente novamente!"]
        return resultado_nova_tarefa
    

def alterar(resultado, id, nome, descricao, data_inicio, data_fim, status):
    resultado_visualizar = visualizar(resultado)

    lista_ids = list()

    for linha in resultado_visualizar:
        lista_ids.append(linha[1])

    if int(id) in lista_ids:
        conexao = conectar()
        cursor = conexao.cursor()

        try:
            query_alteracao = f"""
                UPDATE tarefas
                SET nome = CASE WHEN '{nome}' != '' THEN '{nome}' ELSE nome END,
                    descricao = CASE WHEN '{descricao}' != '' THEN '{descricao}' ELSE descricao END,
                    data_inicio = CASE WHEN '{data_inicio}' != '' THEN '{data_inicio}' ELSE data_inicio END,
                    data_fim = CASE WHEN '{data_fim}' != '' THEN '{data_fim}' ELSE data_fim END,
                    status_tarefa = CASE WHEN '{status}' != '' THEN '{status}' ELSE status_tarefa END
                WHERE id = '{id}'
            """
            cursor.execute(query_alteracao)
            conexao.commit()
            cursor.close()
            desconectar(conexao)

            return [1, 'Tarefa alterada com sucesso!']

        except:
            return [0, 'Não foi possível alterar...tente novamente!']

    else:
        return [0, 'Não foi possível alterar...tente novamente!']


def deletar(resultado, id):
    resultado_visualizar = visualizar(resultado)

    lista_ids = list()

    for linha in resultado_visualizar: 
        lista_ids.append(linha[1])

    if int(id) in lista_ids:
        conexao = conectar()
        cursor = conexao.cursor()

        try:
            query_deletar_urt = f"delete from usuario_recebe_tarefa where id_tarefa = '{id}'"
            cursor.execute(query_deletar_urt)
            conexao.commit()

            query_deletar_tarefa = f"delete from tarefas where id = '{id}'"
            cursor.execute(query_deletar_tarefa)
            conexao.commit()

            cursor.close()
            desconectar(conexao)

            return [1, "Tarefa deletada com sucesso!"]
        except:
           return [0, "Erro ao deletar tarefa...tente novamente!"]
    else:
        return [0, "Erro ao deletar tarefa...tente novamente!"]