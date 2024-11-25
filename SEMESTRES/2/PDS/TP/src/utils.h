#include <map>
#include <vector>
#include <string>
#include <utility>

//Arquivo contendo funções úteis e auxiliares ao longo da implementação do sistema de arquivos
//mas que não fazem parte da classe em si. Armazenadas aqui por uma questão de organização.

using std::map;
using std::pair;
using std::vector;
using std::string;

/**
 * @brief Separa uma string (frase) em um vetor de strings (palavras)
 * de acordo com os espaços.
 * 
 * @param s Frase (String com várias palavras)
 * 
 * @return words Vetor de palavras da frase passada como parâmetro.
*/
vector<string> split(string s) {
  vector<string> words;
  string word;
  for(int i = 0; i < s.size(); i++) {
    if(s[i] == ' ') {
      if(word == "") continue;

      words.push_back(word);
      word = "";
    } else
      word += s[i];
  } 
  if(word != "")
    words.push_back(word);
    
  return words;
}

/**
 * @brief Conversor de letras com acento para a versão sem acento, com o uso de map
 * do tipo (Intervalo(pair<int,int>), Caractere sem acento(string))
 * 
 * @param code Valor inteiro de um tipo char (caractere) na tabela ASCII.
 * 
 * @return Retorna o caractere convertido para a versão sem acento.
*/
string search_original_letter(int code) {
  map<pair<int, int>, string> accents;
  // Maiúsculas
  accents.insert({{192, 197}, "a"});
  accents.insert({{199, 199}, "c"});
  accents.insert({{200, 203}, "e"});
  accents.insert({{204, 207}, "i"});
  accents.insert({{210, 214}, "o"});
  accents.insert({{217, 220}, "u"});
  // Minúsculas
  accents.insert({{224, 229}, "a"});
  accents.insert({{231, 231}, "c"});
  accents.insert({{232, 235}, "e"});
  accents.insert({{236, 239}, "i"});
  accents.insert({{242, 246}, "o"});
  accents.insert({{249, 252}, "u"});

  for(auto interval : accents)
    if(interval.first.first <= code && code <= interval.first.second) 
      return interval.second;

  return "\0";
}

/**
 * @brief Recebe uma string como parâmetro e normaliza ela,
 * tornando-a sem caracteres especiais e acentos.
 * 
 * @param s String original.
 * 
 * @return <string> String normalizada.
*/
string normalize(string s) {
  // Transformando acentos nas suas respectivas letras originais
  for(int i = 0; i < s.size(); i++) {
    char c = s[i];
    int code = (c-'\0' > 0 ? 0 : 320 - abs(c-'\0'));

    string result = search_original_letter(code);

    if(result != "\0") {
        s.erase(i-1, 2);
        s.insert(i-1, result);
        i -= 2;
    }
  }

  // Selecionando somente caracteres entre a-z e A-Z
  string ns;
  for(int i = 0; i < s.size(); i++) {
    int code = s[i]-'\0';

    // Se a letra for maiúscula, então transforma ela em minúscula
    if(code >= 65 && code <= 90)
      ns += s[i] + 32;
    else if((code >= 97 && code <= 122) || code == 32)
      ns += s[i];
  }
  
  return ns;
}