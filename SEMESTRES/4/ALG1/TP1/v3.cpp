#include <bits/stdc++.h>

#define f first
#define s second
#define pb push_back

using namespace std;

struct point {
    double x;
    double y;
};

typedef pair<int, int> pii;

int N, M;

// Armazena a informação da coordenada do vértice i
vector<point> points;

// Dado uma aresta, informa a próxima mais horária a ela
map<pii, int> nexts;

// Lista de adjacência com uma condicional na aresta, indicando
// se ela já foi visitada
vector<vector<pair<int, bool>>> adj;

// Inclinação de um ponto em relação a outro
double rel_inc(point p, point q) {
    return atan2(q.y - p.y, q.x - p.x);
}

// Encontra a face em que a respectiva aresta participa
vector<int> face;
void find_face(int v, int i) {
    // Se eu já visitei essa aresta, então ela foi o ponto
    // de partida da face
    if(adj[v][i].s) return;

    face.pb(v);

    adj[v][i].s = true;

    find_face(adj[v][i].f, nexts[{v, adj[v][i].f}]);
}

int main() {
    cin >> N >> M;

    double x, y;
    int d, v;
    
    // Como os vértices são 1-index, adiciona elementos vazios
    adj.pb({});
    points.pb({});

    for(int i = 1; i <= N; i++) {
        cin >> x >> y >> d;

        points.pb({x, y});

        vector<pair<int, bool>> arr;

        while(d--) {
            cin >> v;
            
            // Seta como falso o indicador de visita da aresta
            arr.pb({v, false});
        }
        adj.pb(arr);
    }

    for(int i = 1; i <= N; i++) {
        // Realiza o sort dos vértices adjacentes a partir da inclinação relativa
        sort(adj[i].begin(), adj[i].end(), [&](pair<int, bool> pa, pair<int, bool> pb) {
            point a = points[pa.f];
            point b = points[pb.f];

            point c = points[i];

            return rel_inc(c, a) < rel_inc(c, b);
        });
    }
    
    // Para evitar fazer uma busca na função de determinação das faces,
    // é salvo em um map qual o próximo vértice mais a esquerda, 
    // dado que vim de certa aresta
    for(int i = 1; i <= N; i++) {
        for(int j = 0; j < adj[i].size(); j++) {
            nexts[{adj[i][j].f, i}] = (j+1)%adj[i].size();
        }  
    }

    // Percorre todas as arestas para encontrar todas as faces
    vector<vector<int>> faces;
    for(int i = 1; i <= N; i++) {
        for(int j = 0; j < adj[i].size(); j++) {
            if(adj[i][j].s) continue;
            face.clear();

            find_face(i, j);

            face.pb(i);
            faces.pb(face);
        }
    }
    
    // Imprime o resultado
    cout << faces.size() << endl;
    for(auto f : faces) {
        cout << f.size() << " ";
        for(auto v : f) 
            cout << v << " ";
        cout << endl;
    }
}