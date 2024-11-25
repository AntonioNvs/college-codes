#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN

#include <vector>
#include <algorithm>

#include "doctest.h"
#include "../src/utils.h"

TEST_CASE("Split a string by spaces") {
    string test = "Meu nome é A N T Ô N I O, e testo vários espaços     .";
    
    vector<string> compare = {"Meu", "nome", "é", "A", "N", "T", "Ô", "N", "I", "O,", "e", "testo", "vários", "espaços", "."};
    
    CHECK(compare.size() == split(test).size());

    int i = 0;
    for(string word : split(test)) {
        CHECK(word == compare[i]);
        i++;
    }
}

TEST_CASE("Search original letters based on int code.") {
    map<int, char> tests;
    tests.insert({197, 'a'});
    tests.insert({199, 'c'});
    tests.insert({203, 'e'});
    tests.insert({210, 'o'});
    tests.insert({227, 'a'});
    tests.insert({239, 'i'});
    tests.insert({245, 'o'});
    tests.insert({252, 'u'});

    for(auto tuple : tests)
        CHECK(tuple.second == search_original_letter(tuple.first)[0]);
}

TEST_CASE("Normalize a UTF-8 string to a-z and A-Z characters") {
    map<string, string> tests;
    tests.insert({"!@##$#%$%$28747824", ""});
    tests.insert({"THIAGO", "thiago"});
    tests.insert({"gÚaRdA-ChúVá", "guardachuva"});
    tests.insert({"RAPHINHA Çäåëü.-- 347347843#243", "raphinha caaeu "});
    
    for(auto tuple : tests)
        CHECK(tuple.second == normalize(tuple.first));
}