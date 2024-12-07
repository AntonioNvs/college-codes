class Livro:
    def __init__(self, isbn, nome):
        self.__isbn = isbn
        self.nome = nome

    def get_isbn(self):
        return self.__isbn