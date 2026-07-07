import sqlite3
from pathlib import Path
from typing import Optional


class Connection:
    """Gerencia conexão com o banco de dados sqlite local.

    Usa `self.db_path` (Path) e cria `self.conn`.
    """
    def __init__(self) -> None:
        base_dir = Path(__file__).resolve().parent
        self.__db_path: Path = base_dir.parent / "db" / "vagas.db"
        self.__conn = sqlite3.connect(str(self.__db_path))


class QueriesController(Connection):
    """Controller para operações de consulta no banco de vagas.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__cursor = self.__conn.cursor()

    def set_vaga(self, *args, **kwargs) -> None:
        """Define uma vaga para um usuário (a implementar)."""
        raise NotImplementedError()

    def get_vaga(self, *args, **kwargs):
        """Retorna a quem pertence uma vaga (a implementar)."""
        raise NotImplementedError()

    def drop_vaga(self, *args, **kwargs) -> None:
        """Remove uma vaga de um usuário (a implementar)."""
        raise NotImplementedError()

    def replace_vaga(self, *args, **kwargs) -> None:
        """Substitui uma vaga por outra (a implementar)."""
        raise NotImplementedError()

    def vaga_verifier(self, *args, **kwargs) -> bool:
        """Verifica se existe uma vaga — deve retornar bool."""
        raise NotImplementedError()

    def listar_vagas(self, *args, **kwargs):
        """Lista vagas baseadas na guild (a implementar)."""
        raise NotImplementedError()

    

if __name__ == '__main__':
    test = QueriesController()