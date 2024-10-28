#include <bits/stdc++.h>

#define MAXS 101
#define MAXC 1025
#define pb push_back
#define INF 0x3f3f3f3f

using namespace std;

int N, K;

struct SectionInfo {
    int bonus;
    int time;
};

struct TrickInfo {
    int pont;
    int time;
};

struct DPInfo {
    int info;
    int crr_state;
};

TrickInfo memo[MAXC][MAXC];
DPInfo dp[MAXS][MAXC];

vector<SectionInfo> sections;
vector<TrickInfo> tricks;

vector<int> decimal_to_tricks(int dec) {
    vector<int> bin (K, 0);
    int idx = 0;

    while(dec > 0) {
        bin[idx++] = dec % 2;
        dec /= 2;
    }

    return bin;
}

DPInfo maximum_radical(int crr_sec, int prev_tricks) {
    // Se estou na última seção, retorna a combinação máxima dado os tricks anteriores
    if(dp[crr_sec][prev_tricks].info != -INF) return dp[crr_sec][prev_tricks];
    if(crr_sec == N) {
        int maxi = 0;
        int i_state = 0;
        for(int i = 0; i < pow(2, K); i++) {
            if(memo[prev_tricks][i].pont > maxi && memo[prev_tricks][i].time <= sections[crr_sec].time) {
                if(memo[prev_tricks][i].pont > maxi)
                    maxi = memo[prev_tricks][i].pont;
                    i_state = i;
            }
        }
        
        return dp[crr_sec][prev_tricks] = {sections[crr_sec].bonus*maxi, i_state};
    }

    int maxi = 0;
    for(int i = 0; i < pow(2, K); i++)
        if(memo[prev_tricks][i].time <= sections[crr_sec].time) {
            DPInfo attempt = maximum_radical(crr_sec+1, i);
            int total = attempt.info + sections[crr_sec].bonus*memo[prev_tricks][i].pont;

            if(total > maxi) {
                maxi = total;
                dp[crr_sec][prev_tricks] = {
                    total,
                    i
                };
            }
        }
            
    
    return dp[crr_sec][prev_tricks];
}

int main() {
    cin >> N >> K;

    sections.pb({});
    tricks.pb({});

    for(int i = 0; i < MAXS; i++) 
        for(int j = 0; j < MAXC; j++) 
            dp[i][j] = {-INF, -1};

    int c, t;
    for(int i = 1; i <= N; i++) {
        cin >> c >> t;
        sections.pb({c, t});
    }

    for(int i = 1; i <= K; i++) {
        cin >> c >> t;

        tricks.pb({c, t});
    }

    // Preencher o pré-processamento de combinações
    for(int i = 0; i < pow(2, K); i++) {
        vector<int> previous = decimal_to_tricks(i);

        for(int j = 0; j < pow(2, K); j++) {
            vector<int> current = decimal_to_tricks(j);

            int qtd = 0;
            int pont = 0;
            int time = 0;

            for(int i = 0; i < K; i++)
                if(current[i]) {
                    qtd++;
                    pont += (previous[i]) ? (int)(tricks[i+1].pont/2) : tricks[i+1].pont;
                    time += tricks[i+1].time;
                }

            memo[i][j] = {pont*qtd, time};
        }
    }

    // Executando para a primeira seção e vendo se deu certo
    DPInfo dp_info = maximum_radical(1, 0);
    cout << dp_info.info << endl;

    for(int i = 1; i <= N; i++) {
        int crr = dp_info.crr_state;

        vector<int> section_tricks = decimal_to_tricks(crr);

        int qtd = 0;
        for(int i = 0; i < K; i++) if(section_tricks[i] > 0) qtd++;

        cout << qtd << " ";
        for(int i = 0; i < K; i++) 
            if(section_tricks[i] > 0)
                cout << i+1 << " ";
        
        if(i < N)
            dp_info = dp[i+1][dp_info.crr_state];

        cout << endl;
    }
}