"""
Controlador de Queries para o SQLite : Uso como base para futuros cogs.
"""
import sqlite3
import aiosql
from pathlib import Path
from typing import Optional

 
class QueriesController:
    def __init__(self) -> None:
        super().__init__()
        BASE_DIR = Path(__file__).resolve().parents[1]
        self.__DB_PATH: Path = BASE_DIR / "Database" / "rpg.sqlite3"
        self.__QUERIES_PATH: Path = BASE_DIR / "Queries" / "management.sql"
        # Carrega as queries do arquivo .sql como métodos deste objeto
        self.queries = aiosql.from_path(
            self.__QUERIES_PATH, 
            "sqlite3",
            mandatory_parameters=False
            )

    def __connect(self) -> sqlite3.Connection:
        """
        Cria uma conexão nova já garantindo o modo WAL ativado.
        """
        conexao = sqlite3.connect(self.__DB_PATH)
        conexao.row_factory = sqlite3.Row
        conexao.execute("PRAGMA journal_mode=WAL;")
        return conexao

    def set_vaga(self, vaga: str, discord_user: str, discord_user_id: str, discord_guild_id: str, universo:str) -> int:
        """
        Define uma vaga a um usuário. Retorna 0 se conseguir executar a query,
        1 se a vaga já existir, 2 se ocorrer um erro interno.
        """
        vaga = vaga.strip().title()
        universo = universo.strip().title()
        if len(vaga.split()) > 2:
            return 3
        conexao = self.__connect()
        try:
            self.queries.set_vaga(
                conexao,
                vaga=vaga,
                discord_user=discord_user,
                discord_user_id=discord_user_id,
                discord_guild_id=discord_guild_id,
                universo=universo
            )
            conexao.commit()
            return 0
        except sqlite3.IntegrityError:
            return 1
        except sqlite3.Error as e:
            print(e)
            return 2 
        finally:
            conexao.close()

    def get_vaga(self, discord_guild_id: str, vaga: str) -> Optional[tuple]:
        """
        Busca uma vaga específica dentro de uma guild.
        Retorna a linha (id, vaga, discord_user, discord_user_id, discord_guild_id) se existir, ou None.
        """
        conexao = self.__connect()
        try:
            resultado = self.queries.get_vaga(
                conexao,
                discord_guild_id=discord_guild_id,
                vaga=vaga,
            )
            return dict(resultado) if resultado else None
        except sqlite3.Error as e:
            print(e)
            return None
        finally:
            conexao.close()

    def drop_vaga(self, discord_guild_id: str, vaga: str) -> int:
        """
        Apaga uma vaga específica de uma guild. Retorna 0 se sucesso, 1 se erro.
        """
        conexao = self.__connect()
        try:
            self.queries.drop_vaga(
                conexao,
                discord_guild_id=discord_guild_id,
                vaga=vaga,
            )
            conexao.commit()
            return 0
        except sqlite3.Error as e:
            print(e)
            return 1
        finally:
            conexao.close()

    def replace_vaga(self, discord_user_id: str, discord_guild_id: str, vaga_substituicao: str, universo: str) -> int:
        """
        Substitui a vaga de um usuário por outra, com base no discord_user_id e discord_guild_id.
        Retorna 0 se sucesso, 1 se erro.
        """
        conexao = self.__connect()
        try:
            self.queries.replace_vaga(
                conexao,
                discord_user_id=discord_user_id,
                discord_guild_id=discord_guild_id,
                vaga_substituicao=vaga_substituicao,
                universo=universo
            )
            conexao.commit()
            return 0
        except sqlite3.Error as e:
            print(e)
            return 1
        finally:
            conexao.close()

    def listar_vagas(self, discord_guild_id: str) -> list:
        """
        Lista todas as vagas ocupadas de uma guild.
        """
        conexao = self.__connect()
        try:
            resultado = self.queries.listar_vagas(
                conexao,
                discord_guild_id=discord_guild_id,
            )
            return [dict(row) for row in resultado]
        except sqlite3.Error as e:
            print(e)
            return []
        finally:
            conexao.close()
    def verificar_pessoa(self, discord_guild_id: str, discord_user_id: str) -> Optional[list]:
        """
        verifica se a pessoa está registrada no servidor
        0 -> existe
        1 -> nao existe
        2 -> erro
        """
        conexao = self.__connect()
        conexao.row_factory = None
        try:
            resultado = self.queries.verificar_pessoa(
                conexao,
                discord_user_id=discord_user_id,
                discord_guild_id=discord_guild_id
            )
            return list(resultado) if resultado else False
        except sqlite3.Error as e:
            print(e)
            return None
        finally: 
            conexao.close()
# INSTÂNCIA PARA DEBUG
if __name__ == '__main__':
   t = QueriesController()
   print(t.set_vaga("Janaina", "rootspy", "667", "893"))
   print(t.get_vaga("893", "Janaina"))
   print(t.listar_vagas("893"))
   print(t.verificar_pessoa("893", "667"))
   print(t.drop_vaga("893", "Janaina"))