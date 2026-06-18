import sqlite3

def conectar():
    return sqlite3.connect("./BancoDados/campeonatoBrasileiro2026DB.db")  # banco no mesmo diretório