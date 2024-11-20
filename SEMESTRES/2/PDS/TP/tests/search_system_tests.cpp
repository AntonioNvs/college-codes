#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN

#include <map>
#include <vector>
#include <algorithm>

#include "doctest.h"
#include "../src/search_system.h"

const char * path = "./tests/test_documents";

TEST_CASE("Get name files.") {
    SearchSystem search_system(path);
    
    int i = 0;
    vector<string> result = search_system.get_files_name();
    sort(result.begin(), result.end());

    for(string name : {"d1.txt", "d2.txt", "d3.txt"}) {
        CHECK(name == result[i]);
        i++;
    }
}

TEST_CASE("Construct a rervese index of test files.") {
    SearchSystem search_system(path);
    map<string, set<string>> compare;
    compare.insert({"apartamento", {"d1.txt", "d3.txt"}});
    compare.insert({"casa", {"d1.txt", "d2.txt"}});
    compare.insert({"em", {"d2.txt"}});
    compare.insert({"entrar", {"d2.txt"}});
    compare.insert({"esta", {"d3.txt"}});
    compare.insert({"ninguem", {"d1.txt", "d2.txt", "d3.txt"}});
    compare.insert({"todos", {"d2.txt", "d3.txt"}});
    compare.insert({"no",{"d3.txt"}});
    compare.insert({"porem",{"d1.txt"}});
    compare.insert({"quem",{"d1.txt", "d2.txt", "d3.txt"}});
    compare.insert({"quer",{"d1.txt", "d2.txt"}});
    compare.insert({"sairam",{"d2.txt", "d3.txt"}});
    compare.insert({"tambem",{"d1.txt"}});

    map<string, set<string>> original = search_system.get_reverse_index();

    for(auto tuple : compare) {
        auto compare_set = tuple.second;
        auto original_set = original[tuple.first];

        CHECK(compare_set.size() == original_set.size());

        for(auto it = compare_set.begin(); it != compare_set.end(); it++)
            CHECK(original_set.find((*it)) != original_set.end());
    }
}

TEST_CASE("Test the return of search querys.") {
    SearchSystem search_system(path);
    map<string, vector<string>> compare;
    compare.insert({"ApArTáMênTô1873 NíNguêm Qùér898*7#4-", {"d1.txt"}});
    compare.insert({"ApArTáMênTô1873 NíNguêm Qùém898*7#4-", {"d1.txt", "d3.txt"}});

    for(auto tuple : compare) {
        int i = 0;
        for(string s : search_system.query(tuple.first)) {
            CHECK(tuple.second[i] == s);
            i++;
        }
    }
}
