#include <bits/stdc++.h>

#define f first
#define s second
#define pb push_back
#define INF 0x3f3f3f3f

using namespace std;

struct point {
    double x;
    double y;

    point operator-(const point &p) const {
        return {x - p.x, y - p.y};
    }
};

typedef pair<int, int> pii;

int N, M;

vector<point> points;
vector<vector<pair<int, bool>>> adj;

double rel_inclination(point p, point q) {
    return atan2(q.y - p.y, q.x - p.x);
}

double angle(point p, point q, point r) {
    point u = p - q;
    point v = r - q;

    return acos((u.x*v.x + u.y*v.y) / (sqrt(u.x*u.x + u.y*u.y) * sqrt(v.x*v.x + v.y*v.y)));
}

int curve_type(point a, point b, point c) {
    double v = a.x*(b.y-c.y)+b.x*(c.y-a.y)+c.x*(a.y-b.y);
    if (v > 0) return -1; // esquerda.
    if (v < 0) return +1; // direita.
    return 0; // em frente.
}

vector<int> face;
bool dfs(int v, int i, int end) {
    if(adj[v][i].s) return v == end;

    face.pb(v);

    adj[v][i].s = true;
    
    int u = adj[v][i].f;

    point p = points[v];
    point q = points[u];

    sort(adj[u].begin(), adj[u].end(), [&](pair<int, bool> pa, pair<int, bool> pb) {
        int a = pa.f;
        int b = pb.f;

        point r = points[a];
        point s = points[b];

        double dr = angle(p, q, r);
        double ds = angle(p, q, s);

        if(curve_type(p, q, r) == -1)
            dr = M_PI - dr;

        if(curve_type(p, q, s) == -1)
            ds = M_PI - ds;

        return dr*curve_type(p, q, r) < ds*curve_type(p, q, s);
    });

    bool cond;
    if(adj[u][0].f == v && adj[u].size() > 1)
        cond = dfs(u, 1, end);
    else
        cond = dfs(u, 0, end);

    if(!cond) adj[v][i].s = false;
    return cond;
}

int main() {
    cin >> N >> M;

    double x, y;
    int d, v;
    
    adj.pb({});
    points.pb({});

    for(int i = 1; i <= N; i++) {
        cin >> x >> y >> d;

        points.pb({x, y});

        vector<pair<int, bool>> arr;

        while(d--) {
            cin >> v;
            
            arr.pb({v, false});
        }
        adj.pb(arr);
    }

    vector<vector<int>> faces;

    for(int i = 1; i <= N; i++) {
        for(int j = 0; j < adj[i].size(); j++) {
            if(adj[i][j].s) continue;
            face.clear();

            if(dfs(i, j, i)) {
                face.pb(i);
                faces.pb(face);
            }
        }
    }

    for(int i = 1; i <= N; i++) {
        bool found = false;

        for(int j = 0; j < adj[i].size(); j++) {
            if(adj[i][j].s) continue;

            face.clear();
            face.pb(i);

            int u = adj[i][j].f;

            while(u != i) {
                face.pb(u);
                int copy = u;

                for(int k = 0; k < adj[u].size(); k++)
                    if(!adj[u][k].s) {
                        u = adj[u][k].f;
                        adj[u][k].s = true;
                        break;
                    }

                if(u == copy) break;
            }
            
            if(u == i) {
                found = true;
                face.pb(i);
                faces.pb(face);
            }  
        }

        if(found) break;
    }

    cout << faces.size() << endl;
    for(auto f : faces) {
        cout << f.size() << " ";
        for(auto v : f)
            cout << v << " ";
        cout << endl;
    }
}