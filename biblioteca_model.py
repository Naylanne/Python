import psycopg2

class BibliotecaModel:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname="biblioteca",
                user="postgres",
                password="3699",
                host="localhost",
                port="5432"
            )
            self.cursor = self.conn.cursor()
            print("Conexão estabelecida com sucesso!")
        except Exception as e:
            print(f"\nErro ao conectar ao banco de dados: {e}\n")

    def __del__(self):
        if hasattr(self, "cursor") and hasattr(self, "conn"):
            self.cursor.close()
            self.conn.close()
            print("Conexão encerrada.")

    def existe_id(self, tabela, id_valor):
        try:
            self.cursor.execute(f"select 1 from {tabela} where id=%s;", (id_valor,))
            return self.cursor.fetchone is not None
        except Exception as e:
            print(f"\nErro ao verificar: {e}\n")
            return False       


class AutorModel(BibliotecaModel):
    
    def cadastrar(self, nome, nacionalidade):
        try:
            self.cursor.execute("insert into autor (nome, nacionalidade) VALUES (%s, %s)", (nome, nacionalidade))
            self.conn.commit()
            print("Autor cadastrado com sucesso!")
        except Exception as e:
            print(f"\nErro ao cadastrar autor: {e}\n")
            self.conn.rollback()

    def listar(self):
        try:
            self.cursor.execute("select * from autor order by id;")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"\nErro ao listar autores: {e}\n")
            return []

    def atualizar(self, id_autor, nome, nacionalidade):
        try:
            if not self.existe_id(id_autor):
                print("\nNenhum autor encontrado com esse ID.\n")
                return False
            self.cursor.execute("update autor set nome=%s, nacionalidade=%s where id=%s", (nome, nacionalidade, id_autor))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"\nErro ao atualizar autor: {e}\n")
            self.conn.rollback()
            return False

    def excluir(self, id_autor):
        try:
            if not self.existe_id(id_autor):
                print("\nNenhum autor encontrado com esse ID.\n")
                return False
            self.cursor.execute("delete from autor where id=%s", (id_autor,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"\nErro ao excluir autor: {e}\n")
            self.conn.rollback()
            return False
        
class LivroModel(BibliotecaModel):

    def cadastrar(self, titulo, ano, autor_id):
        try:
            self.cursor.execute("insert into livro (titulo, ano_publicacao, autor_id) VALUES (%s, %s, %s)", (titulo, ano, autor_id))
            self.conn.commit()
            print("Livro cadastrado com sucesso!")
        except Exception as e:
            print(f"\nErro ao cadastrar livro: {e}\n")
            self.conn.rollback()

    def listar(self):
        try:
            self.cursor.execute("select livro.id, livro.titulo, livro.ano_publicacao, autor.nome from livro join autor on livro.autor_id = autor.id")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"\nErro ao listar livros: {e}\n")
            return []

    def atualizar(self, id_livro, titulo, ano, autor_id):
       try:
            if not self.existe_id(id_livro):
                print("\nNenhum livro encontrado com esse ID.\n")
                return False
            self.cursor.execute("update livro set titulo=%s, ano_publicacao=%s, autor_id=%s where id=%s", (titulo, ano, autor_id, id_livro))
            self.conn.commit()
            return True
       except Exception as e:
            print(f"\nErro ao atualizar livro: {e}\n")
            self.conn.rollback()
            return False

    def excluir(self, id_livro):
        try:
            if not self.existe_id(id_livro):
                print("\nNenhum livro encontrado com esse ID.\n")
                return False
            self.cursor.execute("delete from livro where id=%s", (id_livro,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"\nErro ao excluir livro: {e}\n")
            self.conn.rollback()
            return False
