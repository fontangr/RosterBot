"""
Controlador de Queries para o SQLite : Uso como base para futuros cogs.
    Cria a conexão -- Connection
    Cria o controlador -- QueriesControler 
    Cria funções para que sejam importadas por métodos nas extensões [NotImplemented]
"""

import sqlite3
from pathlib import Path
from typing import Optional
class Connection:
    
    def __init__(self) -> None:
        base_dir = Path(__file__).resolve().parent
        self.__db_path: Path = base_dir.parent / "db" / "vagas.db"
        self.__conn = sqlite3.connect(str(self.__db_path))

# funcoes a serem implementadas
class QueriesController(Connection):
    def __init__(self) -> None:
        super().__init__()
        self.__cursor = self.__conn.cursor()
        
    def set_vaga(self, *args, **kwargs) -> None:
        raise NotImplementedError()
    def get_vaga(self, *args, **kwargs):
        raise NotImplementedError()

    def drop_vaga(self, *args, **kwargs) -> None:
        raise NotImplementedError()

    def replace_vaga(self, *args, **kwargs) -> None:
        raise NotImplementedError()

    def vaga_verifier(self, *args, **kwargs) -> bool:
        raise NotImplementedError()

    def listar_vagas(self, *args, **kwargs):
        raise NotImplementedError()
