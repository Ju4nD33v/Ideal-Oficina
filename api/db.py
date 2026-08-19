from typing import Any, Iterable
from database.conexao import conectar


def fetch_all(sql: str, params: Iterable[Any] = ()):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    try:
        cursor.execute(sql, tuple(params))
        return cursor.fetchall()
    finally:
        cursor.close()
        conexao.close()


def fetch_one(sql: str, params: Iterable[Any] = ()):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    try:
        cursor.execute(sql, tuple(params))
        return cursor.fetchone()
    finally:
        cursor.close()
        conexao.close()


def execute(sql: str, params: Iterable[Any] = ()):
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(sql, tuple(params))
        conexao.commit()
        return cursor.lastrowid
    except Exception:
        conexao.rollback()
        raise
    finally:
        cursor.close()
        conexao.close()
