class RepositorioMemoria:
    def __init__(self):
        self.acervo = {}
        self.emprestimos = {}

    def adicionar_livro_acervo(self, isbn, livro):
        self.acervo[livro.get_isbn()] = livro

    def livro_esta_emprestado(self, livro):
        return livro in self.emprestimos

    def emprestar_livro(self, livro, usuario):
        self.emprestimos[livro] = usuario

    def receber_livro_emprestado(self, livro):
        self.emprestimos.pop(livro, None)

    def livros_emprestados_usuario(self, usuario):
        return [livro for livro, u in self.emprestimos.items() if u == usuario]