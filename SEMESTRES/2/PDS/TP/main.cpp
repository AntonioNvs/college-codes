#include <iostream>
#include <fstream>

#include "src/search_system.h"

using namespace std;

int main() {
    // Uso para teste de todas as funções
    SearchSystem search_system = SearchSystem("./documentos");
    
    string query;
    
    cout << "Digite sua query ou digite 'q' para sair." << endl;
    while(getline(cin, query)) {
        if(query == "q") break;

        int count = 1;
        for(auto file : search_system.query(query))
            cout << count << ") " << file << endl, count++;
        
        // Caso o count seja 1, então não foi retornado nenhum documento.
        if(count == 1)
            cout << "Não existe um documento com essas palavras." << endl;
            
        cout << endl;
    }
}