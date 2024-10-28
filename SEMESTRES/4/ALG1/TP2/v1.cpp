#include <bits/stdc++.h>

#define INF 0x3f3f3f3f
#define LINF 0x3f3f3f3f3f3f
#define pb push_back
#define f first
#define s second
#define pii pair<int, int>
#define t_pq tuple<long long int, long long int, int>

using namespace std;

struct data {
    long long int year;
    long long int time;
    long long int cost;
};

int N, M;

vector<vector<pair<int, data>>> adj;
vector<pair<data, pii>> edges;

void dijkstra() {
    int visiteds[N+1];
    long long int distance[N+1], time_construct[N+1];

    for(int i = 1; i <= N; i++) {
        visiteds[i] = 0;
        distance[i] = LINF;
        time_construct[i] = 0LL;
    }

    distance[1] = 0LL;

    priority_queue<t_pq, vector<t_pq>, greater<t_pq>> pq;
    pq.push({0LL, 0LL, 1});

    while(!pq.empty()) {
        long long dist = get<0>(pq.top());
        long long max_year = get<1>(pq.top());
        int u = get<2>(pq.top());

        pq.pop();

        if(visiteds[u]) continue;
        visiteds[u] = 1;

        for(auto info : adj[u]) {
            int v = info.f;
            long long time = info.s.time;
            if(distance[v] > dist + time) {
                distance[v] = dist + time;
                time_construct[v] = info.s.year;

                pq.push({distance[v], max(time_construct[v], max_year), v});
            }
        }
    }

    long long maxi = -1;
    for(int i = 1; i <= N; i++) {
        cout << distance[i] << endl;
        maxi = max(maxi, time_construct[i]);
    }
    cout << maxi << endl;   
}

// Parte dos conjuntos disjuntos
vector<int> level;
vector<int> parent;

int find(int u) {
    if(u != parent[u])
        parent[u] = find(parent[u]);
    return parent[u];
}

void join(int u, int v) {
    int x = find(u);
    int y = find(v);

    if(level[x] > level[y])
        parent[y] = x;
    else
        parent[x] = y;

    if(level[x] == level[y])
        level[y]++;
}

bool compare_year(pair<data, pii> a, pair<data, pii> b) {
    return a.f.year < b.f.year;
}

bool compare_cost(pair<data, pii> a, pair<data, pii> b) {
    return a.f.cost < b.f.cost;
}

void kruskal(string type) {
    for(int i = 1; i <= N; i++) {
        level[i] = 1;
        parent[i] = i;
    }

    sort(edges.begin(), edges.end(), type == "year" ? compare_year : compare_cost);

    long long int ans = 0;
    for(auto edge : edges) {
        int u = edge.s.f;
        int v = edge.s.s;
        
        long long value = type == "year" ? edge.f.year : edge.f.cost;

        if(find(u) != find(v)) {
            ans = type == "year" ? max<long long>(ans, value) : ans + value;
            join(u, v);
        }
    }

    cout << ans << endl;
}

int main() {
    scanf("%d %d", &N, &M);

    int u, v;
    long long int a, l, c;

    for(int i = 0; i <= N; i++) {
        adj.pb({});
        level.pb({});
        parent.pb({});
    }       

    for(int i = 1; i <= M; i++) {
        scanf("%d %d %lld %lld %lld", &u , &v , &a , &l , &c);
        adj[u].pb({v, {a, l, c}});
        adj[v].pb({u, {a, l, c}});
        edges.pb({{a, l, c}, {u, v}});
    }

    dijkstra();
    kruskal("year");
    kruskal("cost");
}