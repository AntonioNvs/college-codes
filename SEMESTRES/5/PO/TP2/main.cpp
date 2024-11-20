#include <string>
#include <vector>
#include <fstream>
#include <iostream>
#include <cmath>
#include <iomanip>

#define PB push_back
#define MAXF 0x3f3f3f3f3f3f
#define VECTOR_TYPE vector<double>
#define MATRIX_TYPE vector<vector<double>>

using namespace std;

int N; // Número de restrições
int M; // Número de variáveis

const double EPSILON = 1e-8;

struct StandardException {};

struct SimplexReturn {
    double vo;
    string state;
    VECTOR_TYPE solution;
    VECTOR_TYPE certificate;
};

struct AuxiliarReturn {
    bool viable;
    VECTOR_TYPE base_columns;
};

void print_tableau(VECTOR_TYPE &VERO_COST, MATRIX_TYPE &VERO_MATRIX, VECTOR_TYPE &c, MATRIX_TYPE &A, VECTOR_TYPE &b, double vo) {
    ofstream outfile("tableu.txt");

    int width = 10;
    //for (int i = 0; i < VERO_COST.size(); i++) outfile << setw(width) << VERO_COST[i];
    outfile << " | ";
    for(int i = 0; i < c.size(); i++) outfile << setw(width) << c[i];

    outfile << setw(width) << vo;
    outfile << endl;

    for(int i = 0; i <= VERO_COST.size() + c.size(); i++) outfile << setw(width) << "------";
    outfile << endl;
    
    for(int i = 0; i < VERO_MATRIX.size(); i++) {
        //for(int j = 0; j < VERO_MATRIX.size(); j++) outfile << setw(width) << VERO_MATRIX[i][j];
        outfile << " | ";

        for(int j = 0; j < A[i].size(); j++) outfile << setw(width) << A[i][j];

        outfile << " | ";
        outfile << setw(width) << b[i] << endl;
    }
    outfile << endl;

    outfile.close();
}

void multiply_row_by_constant(VECTOR_TYPE &row, double v) {
    for(int j = 0; j < row.size(); j++) {
        row[j] *= v;
        if(fabs(row[j]) < EPSILON) row[j] = 0;
    }
}

void add_row_and_other_row(VECTOR_TYPE &A, VECTOR_TYPE &B, double factor) {
    if (A.size() != B.size())
        throw StandardException();

    for(int i = 0; i < A.size(); i++) {
        A[i] += factor*B[i];
        if(fabs(A[i]) < EPSILON) A[i] = 0;
    }
}

SimplexReturn solve_simplex(
    VECTOR_TYPE c, 
    MATRIX_TYPE A, 
    VECTOR_TYPE b, 
    VECTOR_TYPE base_columns, 
    VECTOR_TYPE VERO_COST, 
    MATRIX_TYPE VERO_MATRIX,
    bool auxiliar = false
) {
    int n_rows = A.size();
    int n_cols = A[0].size();

    multiply_row_by_constant(c, -1);

    double vo = 0;

    // Zerando os custos da matrix básica.
    while(true) {
        for(int k = 0; k < base_columns.size(); k++) {
            double factor = -c[base_columns[k]] / A[k][base_columns[k]];

            if(fabs(factor) < EPSILON) continue;

            add_row_and_other_row(VERO_COST, VERO_MATRIX[k], factor);
            add_row_and_other_row(c, A[k], factor);
            vo += factor*b[k];
        }

        //print_tableau(VERO_COST, VERO_MATRIX, c, A, b, vo);
        
        int index = -1;
        for(int j = 0; j < n_cols; j++) if(c[j] < -EPSILON) {
            index = j;
            break;
        }

        // Chegou em estado máximo
        if(index < 0) {
            VECTOR_TYPE solution(n_cols, 0);

            if(vo < -EPSILON && auxiliar) {
                return SimplexReturn{vo, "inviavel", solution, VERO_COST};
            }
            else {
                for(int k = 0; k < base_columns.size(); k++)
                    solution[base_columns[k]] = b[k];
                return SimplexReturn{vo, "otima", solution, auxiliar ? base_columns : VERO_COST};
            }
        }

        // Ainda tem iteração
        pair<int, double> less_index (-1, MAXF);

        for(int k = 0; k < n_rows; k++)
            if(b[k]/A[k][index] < less_index.second && A[k][index] > 0)
                less_index = {k, b[k]/A[k][index]};
        
        // Ilimitado
        if(less_index.first < 0) {
            VECTOR_TYPE certificate (n_cols, 0);
            certificate[index] = 1;
            for(int k = 0; k < base_columns.size(); k++)
                certificate[base_columns[k]] = -A[k][index];    

            return SimplexReturn{vo, "ilimitada", {}, certificate};    
        }
        
        double factor = 1/A[less_index.first][index];
        multiply_row_by_constant(A[less_index.first], factor);
        multiply_row_by_constant(VERO_MATRIX[less_index.first], factor);
        b[less_index.first] *= factor;

        for(int k = 0; k < n_rows; k++) {
            if (less_index.first == k) continue;

            double factor = -A[k][index];
            add_row_and_other_row(A[k], A[less_index.first], factor);
            add_row_and_other_row(VERO_MATRIX[k], VERO_MATRIX[less_index.first], factor);
            b[k] += factor*b[less_index.first];
        }
        base_columns[less_index.first] = index;
    }
}

AuxiliarReturn get_auxiliar_pl(VECTOR_TYPE c, MATRIX_TYPE A, VECTOR_TYPE b, VECTOR_TYPE VERO_COST, MATRIX_TYPE VERO_MATRIX) {
    int n_rows = A.size();

    for(int i = 0; i < c.size(); i++) c[i] = 0;

    for(int k = 0; k < n_rows; k++) {
        c.PB(-1);
        for(int j = 0; j < n_rows; j++) {
            if(k == j) A[k].PB(1);
            else A[k].PB(0);
        }
    }

    VECTOR_TYPE base_columns(n_rows, 0);

    for(int i = n_rows-1; i >= 0; i--)
        base_columns[n_rows-i-1] = c.size()-i-1;

    SimplexReturn ans = solve_simplex(c, A, b, base_columns, VERO_COST, VERO_MATRIX, true);
    
    return {ans.state == "otima", ans.certificate};
}

int main(int argc, char** argv) {
    cout << fixed << setprecision(3);

    if (argc < 2) {
        cerr << "Inform the filepath on command line" << endl;
        return 1;
    }

    ifstream file(argv[1]);

    if(!file.is_open()) {
        cerr << "Error opening the file!" << endl;
        return 1;
    }

    file >> N >> M;

    VECTOR_TYPE c(M);

    for(int i=0; i<M; i++) {
        file >> c[i];
    }   

    MATRIX_TYPE A(N, VECTOR_TYPE(M, 0));
    VECTOR_TYPE b(N);

    for(int i=0; i<N; i++) {
        for(int j=0; j<M; j++) {
            file >> A[i][j];
        }
        file >> b[i];
    }

    // Fazendo TABLEAU inicial com registro extendido
    int n_rows = A.size();
    int n_cols = A[0].size();

    VECTOR_TYPE VERO_COST (n_rows);
    MATRIX_TYPE VERO_MATRIX (n_rows, VECTOR_TYPE(n_rows, 0));
    for(int i = 0; i < n_rows; i++) VERO_MATRIX[i][i] = 1;
    
    // Transformando restrições negativas em positivas
    for(int i = 0; i < A.size(); i++) {
        if(b[i] < 0) {
            multiply_row_by_constant(A[i], -1);
            multiply_row_by_constant(VERO_MATRIX[i], -1);
            b[i] *= -1;
        }
    }

    AuxiliarReturn auxiliar_answer = get_auxiliar_pl(c, A, b, VERO_COST, VERO_MATRIX);
    
    if(!auxiliar_answer.viable) {
        cout << "inviavel" << endl;
        for(int i = 0; i < auxiliar_answer.base_columns.size(); i++)
            cout << auxiliar_answer.base_columns[i] << " ";
        cout << endl;
        return 0;
    }

    VECTOR_TYPE base_columns;
    for(int i = 0; i < auxiliar_answer.base_columns.size(); i++)
        if (auxiliar_answer.base_columns[i] < n_cols)
            base_columns.PB(auxiliar_answer.base_columns[i]);

    //print_tableau(VERO_COST, VERO_MATRIX, c, A, b, 0);

    while(true) {
        for(int k = 0; k < base_columns.size(); k++) {
            if(A[k][base_columns[k]] == 0) {
                for(int j = 0; j < base_columns.size(); j++) {
                    if(A[k][base_columns[j]] != 0) {
                        swap(base_columns[k], base_columns[j]);
                        break;
                    }
                }
            }
        }
        bool all_available = true;
        for(int i = 0; i < base_columns.size(); i++) all_available &= A[i][base_columns[i]] != 0;
        if(all_available) break;
    }

    // Transformando a matriz em FPI
    for(int k = 0; k < base_columns.size(); k++) {
        int col = base_columns[k];
        
        double factor = A[k][col];
        
        multiply_row_by_constant(A[k], 1/factor);
        multiply_row_by_constant(VERO_MATRIX[k], 1/factor);
        b[k] /= factor;

        for(int l = 0; l < n_rows; l++) {
            if (k == l) continue;
            factor = -A[l][col];
            add_row_and_other_row(A[l], A[k], factor);
            add_row_and_other_row(VERO_MATRIX[l], VERO_MATRIX[k], factor);
            b[l] += factor*b[k];
        }
    }

    SimplexReturn res = solve_simplex(c, A, b, base_columns, VERO_COST, VERO_MATRIX);
    cout << res.state << endl;

    if(res.state == "otima") {
        cout << res.vo << endl;
        
        for(int k = 0; k < res.solution.size(); k++)
            cout << res.solution[k] << " ";
        cout << endl;
    } else {
        for(int k = 0; k < n_cols; k++) {
            bool is_not_base = true;
            int j;

            for(j = 0; j < base_columns.size(); j++)
                if(base_columns[j] == k) {
                    is_not_base = false;
                    break;
                }
            
            if(is_not_base) cout << 0 << " ";
            else cout << b[j] << " ";
        }
        cout << endl;
    }

    for(int k = 0; k < res.certificate.size(); k++)
        cout << res.certificate[k] << " ";
    cout << endl;
}