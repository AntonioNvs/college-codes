#include <iostream>
#include <fstream>

#include "utils.h"
#include "dirent.h"
#include "search_system.h"

using namespace std;

SearchSystem::SearchSystem(const char * folder) {
  path_folder = folder;
  read();
  indexer();
}

SearchSystem::~SearchSystem() {
  this->reverse_index.clear();
  this->files_name.clear();
}

void SearchSystem::read(){
  DIR *dir;
  struct dirent *ent;

  if ((dir = opendir(path_folder)) != NULL) {
    // Registra o nome dos arquivos no vetor.
    while ((ent = readdir (dir)) != NULL) 
      if(ent->d_name[0] != '.')
        (this->files_name).push_back(ent->d_name);
    
    closedir (dir);

  } else {
    // Caso haja algum problema em encontrar o diretório mencionado, retorna um erro.
    perror ("");
    return exit(1);
  }
}

vector<string> SearchSystem::get_files_name() const {
  return files_name;
}

map<string, set<string>> SearchSystem::get_reverse_index() const {
  return reverse_index;
}

void SearchSystem::indexer() {
  for(auto filename : files_name) {
    fstream src;
    
    src.open((string)path_folder + '/' + filename, ios::in);

    string line;
    while(getline(src, line)) {
      line = normalize(line);
      for(string word : split(line)) {
        reverse_index[word].insert(filename);
      }
    }
    src.close();
  }
}

vector<string> SearchSystem::query(string q) {
  q = normalize(q);
  
  vector<string> words = split(q);
  map<string, int> counter;

  // Para cada palavra, verifica os arquivos que à possuem e adiciona no counter
  for(auto word : words)
    for(auto it = reverse_index[word].begin(); it != reverse_index[word].end(); it++)
      counter[*it]++;

  // É adicionado o documento se o número de aparições for igual ao número de palavras
  vector<string> result;
  for(auto file : counter) {
    if(file.second == words.size())
      result.push_back(file.first);
  }

  return result;
}
