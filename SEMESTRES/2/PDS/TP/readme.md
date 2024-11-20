# Máquina de Busca

📜 Sistema de busca em arquivos pré-selecionados, baseado em indexadores, em que, com uma interface por linha de comando, é possível selecionar quais documentos são devidamente interessantes com base na frase dada.

## 🛠 Instalação

OS X & Linux:

```sh
git clone https://github.com/AntonioNvs/tp-pds.git tp-pds
```

## 📈 Exemplo de uso

Antes de tudo, é necessário preencher a pasta *./documents* com arquivos *.txt*, que serão as fontes da busca do programa.

Para uso do sistema, temos duas possibilidades. A primeira é o uso do sistema em sí, a partir de uma simples interface de comando. Para executar, basta digitar o comando:

```sh
make
```

Após isso, basta digitar a frase de busca desejada e o programa irá retornar ou os nomes dos documentos que possuem todas as palavras digitadas, ou um aviso alertando que nenhum documento às possuem.

```sh
Digite sua query ou digite 'q' para sair.
APARTAMENTO NINGUÉM QUEM
1) d1.txt
2) d3.txt

apartamento ninguém quer
1) d1.txt

antonio
Não existe um documento com essas palavras.

q
```
A segunda possibilidade é testar os programas. Para isso, basta digitar o comando abaixo que será compilado e executado os códigos de teste das funcionalidades criadas.

```sh
make test
```

## 💻 Configuração para Desenvolvimento

Nosso programa foi feito e testado em **Linux**, na versão **g++ 9.4.0** do compilador para *C++*.
