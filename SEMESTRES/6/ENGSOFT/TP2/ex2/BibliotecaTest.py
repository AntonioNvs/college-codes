import unittest

from Livro import Livro
from Usuario import Usuario
from Biblioteca import Biblioteca
from RepositorioMemoria import RepositorioMemoria
from ExcecaoLivroEmprestado import ExcecaoLivroEmprestado

class BibliotecaTest(unittest.TestCase):
    def setUp(self):
        self.bib = Biblioteca(RepositorioMemoria())
        self.livro1 = Livro("isbn1", "ESM")
        self.livro2 = Livro("isbn2", "GoF")
        self.livro3 = Livro("isbn3", "XP")
        self.usuario1 = Usuario("usu1", "Joao")
        self.usuario2 = Usuario("usu2", "Maria")
        self.bib.adicionar_livro_acervo(self.livro1)
        self.bib.adicionar_livro_acervo(self.livro2)
        self.bib.adicionar_livro_acervo(self.livro3)

    def test_emprestimo(self):
        self.bib.emprestar_livro(self.livro1, self.usuario1)
        self.bib.emprestar_livro(self.livro2, self.usuario1)
        emprestados = self.bib.livros_emprestados_usuario(self.usuario1)
        self.assertEqual(len(emprestados), 2)
        self.assertIn(self.livro1, emprestados)
        self.assertIn(self.livro2, emprestados)

    def test_emprestimo_vazio(self):
        emprestados = self.bib.livros_emprestados_usuario(self.usuario1)
        self.assertEqual(len(emprestados), 0)

    def test_emprestimo_e_devolucao(self):
        self.bib.emprestar_livro(self.livro1, self.usuario1)
        self.bib.emprestar_livro(self.livro2, self.usuario1)
        self.bib.receber_livro_emprestado(self.livro1)
        emprestados = self.bib.livros_emprestados_usuario(self.usuario1)
        self.assertEqual(len(emprestados), 1)
        self.assertNotIn(self.livro1, emprestados)
        self.assertIn(self.livro2, emprestados)

    def test_emprestar_livro_ja_emprestado(self):
        self.bib.emprestar_livro(self.livro1, self.usuario1)
        with self.assertRaises(ExcecaoLivroEmprestado):
            self.bib.emprestar_livro(self.livro1, self.usuario2)

if __name__ == "__main__":
    unittest.main()
