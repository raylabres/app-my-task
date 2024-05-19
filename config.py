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