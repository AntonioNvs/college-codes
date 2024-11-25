#ifndef __SEARCH_SYSTEM_H__
#define __SEARCH_SYSTEM_H__

#include <map>
#include <set>
#include <vector>
#include <string>

using std::map;
using std::set;
using std::vector;
using std::string;

//
struct Document {
    string filename;
    string content;
};

class SearchSystem {
    public:

        /**
         * @brief Construtor da classe. Utiliza as funções indexer e read.
         * 
         * @param folder Diretório contendo os arquivos que serão utilizados na criação do Sistema de Busca.
        */
        SearchSystem(const char * folder);

        /**
         * @brief Destrutor da classe.
        */
        ~SearchSystem();
        
        /**
         * @brief Acessa o método privado contendo os documentos pertencentes ao diretório.
         * 
         * @return Retorna os vetor de strings contendo os documentos.
        */

        vector<string> get_files_name() const;

        /**
         * @brief Acessa o método privado índice reverso.
         * 
         * @return Retorna o índice reverso da classe.
        */
        map<string, set<string>> get_reverse_index() const;

        /**
         * @brief Função de recuperação. Recebe uma pesquisa e retorna os arquivos que contém
         * todas as palavras da pesquisa presentes, em ordem lexicográfica caso haja mais de um.
         * 
         * @param q Frase ou palavra a ser pesquisada.
         * 
         * @return Retorna um vector<string> ordenado lexicograficamente contendo os documentos
         * em que todas as palavras do parâmetro aparecem
         */
        vector<string> query(string q);

    private:

        // Nome do diretório.
        const char * path_folder;
        // Registra o nome dos arquivos presentes no diretório passado como parâmetro para o construtor da classe.
        vector<string> files_name;
        //Índice reverso.
        map<string, set<string>> reverse_index;

        /**
         * @brief Função responsável por criar o índice reverso do sistema.
        */
        void indexer();

        /**
         * @brief Função responsável por ler o local dos arquivos e criar um vetor
         * com de strings contendo o nome de todos os arquivos naquele diretório.
        */
        void read();
};

#endif