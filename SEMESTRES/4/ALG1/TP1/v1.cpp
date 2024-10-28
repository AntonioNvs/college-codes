#include <bits/stdc++.h>

#define INF 0x3f3f3f3f
#define MAXN 100100
#define MAXM 100100
#define pb push_back
#define f first
#define s second


using namespace std;

struct point {
    double x;
    double y;
};

struct edge {
    int a;
    int b;

    bool operator<(const edge& x) const{
        return a < x.b;
    }

    bool operator==(const edge& x) const {
        return a == x.a && b == x.b;
    }
};

typedef pair<int, edge> pie;

int N, M;

point points[MAXN];
vector<int> adj[MAXN];
set<vector<int>> faces;

priority_queue<pie, vector<pie>, greater<pie>> pq;

double relative_inclination(point p, point q) {
    return atan2(q.y - p.y, q.x - p.x);
}

int father;
bool compare_by_inclination(int a, int b) {
    return relative_inclination(points[father], points[a]) < relative_inclination(points[father], points[b]);
}

double angle_between_vectors(point a, point b, point c) {
    point x = {b.x - a.x, b.y - a.y};
    point y = {b.x - c.x, b.y - c.y};

    return acos((x.x*y.x + x.y*y.y) / (sqrt(pow(x.x, 2) + pow(x.y, 2))*sqrt(pow(y.x, 2) + pow(y.y, 2))));

}

int curve_type(point a, point b, point c) {
    double v = a.x*(b.y-c.y)+b.x*(c.y-a.y)+c.x*(a.y-b.y);
    if (v < 0) return -1; // esquerda.
    if (v > 0) return +1; // direita.
    return 0; // em frente.
}

void dfs(edge e, edge initial_edge, bool first) {
    cout << e.a << " " << e.b << endl;

    if(e.a == initial_edge.a && e.b == initial_edge.b && !first) {
        cout << "Face encontrada!" << endl;
        return;
    }

    double min_a = INF;
    int min_v;

    for(auto u : adj[e.b]) {
        if(u != e.a) {
            double deg = angle_between_vectors(points[e.a], points[e.b], points[u]);
            if(deg < min_a && curve_type(points[e.a], points[e.b], points[u]) == -1) {
                min_a = deg;
                min_v = u;
            }
        }
    }

    if(min_a != INF) {
        dfs({e.b, min_v}, initial_edge, false);
    }    
}

int main() {
    cin >> N >> M;

    double x, y;
    int d, v;

    map<pair<int, int>, bool> edges;

    for(int i = 1; i <= N; i++) {
        cin >> x >> y >> d;
        points[i] = {x, y};

        while(d--) {
            cin >> v;
            pair<int, int> e = {min(i, v), max(i, v)};

            if(edges.find(e) == edges.end()) {
                edges[e] = true;
                pq.push({0, {min(i, v), max(i, v)}});
            }
            
            adj[i].pb(v);
        }
    }

    for(int i = 1; i <= N; i++)
        sort(adj[i].begin(), adj[i].end(), compare_by_inclination);

    do {
        pie e = pq.top();
        pq.pop();

        dfs({e.s.a, e.s.b}, {e.s.a, e.s.b}, true);
        
    } while(!pq.empty());
}