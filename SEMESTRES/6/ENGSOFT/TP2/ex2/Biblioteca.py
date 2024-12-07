from ExcecaoLivroEmprestado import ExcecaoLivroEmprestado

class Biblioteca:
    def __init__(self, repo):
        self.repo = repo

    def adicionar_livro_acervo(self, livro):
        self.repo.adicionar_livro_acervo(livro.get_isbn(), livro)

    def emprestar_livro(self, livro, usuario):
        if self.repo.livro_esta_emprestado(livro):
            raise ExcecaoLivroEmprestado()
        
        self.repo.emprestar_livro(livro, usuario)

    def receber_livro_emprestado(self, livro):
        self.repo.receber_livro_emprestado(livro)

    def livros_emprestados_usuario(self, usuario):
        return self.repo.livros_emprestados_usuario(usuario)
