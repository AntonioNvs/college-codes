#= 

COLORAÇÃO
Nome: Antônio Caetano Neves Neto
Matrícula: 2022043698

=#

using JuMP
using HiGHS

# Definindo a estrutura de dados do problema.
mutable struct ProblemData
    n::Int
    edges::Array{Array{Int}}
end

function readData(file)
    n = 0
    edges = []

    for line in eachline(file)
        q = split(line, "\t")

        if q[1] == "n"
            n = parse(Int, q[2])

            # Criando a matriz de adjacência nula para ser preenchida posteriormente.
            for i=1:n
                push!(edges, [])
                for j=1:n
                    push!(edges[i], 0)
                end
            end
        else
            # Preenchendo a matriz de adjacência.
            edges[parse(Int, q[2])][parse(Int, q[3])] = 1
            edges[parse(Int, q[3])][parse(Int, q[2])] = 1
        end
    end

    return ProblemData(n, edges)
end

# Função para imprimir a solução.
function printSolution(data, x)
    sol = 0
    # Para cada cor, verifica se existe algum vértice
    for j = 1: data.n
        exists = 0
        for i = 1: data.n
            aux = round(Int, x[i, j])
            if aux == 1
                exists = 1
                break
            end
        end

        sol += exists
    end
    
    println("TP1 2022043698 = ", sol)
end

# Lendo o arquivo de entrada.
file = open(ARGS[1], "r")
data = readData(file)

# Criando o modelo de programação linear.
model = Model(HiGHS.Optimizer)

# A variável é uma matriz que informa se o vértice i é da cor j
@variable(model, x[1:data.n, 1:data.n], Bin)

# Nenhum vértice pode ter mais de uma cor.
for i=1:data.n
    @constraint(model, sum(x[i, j] for j=1:data.n) == 1)
end

# Vértices adjacentes não podem ter a mesma cor
for i=1:data.n
    for j=1:data.n
        if i != j
            for k=1:data.n
                @constraint(model, x[i, k] + x[j, k] - 1 <= 1 - data.edges[i][j])
            end
        end
    end
end

# Queremos minimizar o número de cores, logo, a soma de todas as colunas que tem vértice
@objective(model, Min, sum(x[i, j]*j for i=1:data.n, j=1:data.n))

# Resolvendo o modelo.
optimize!(model)

printSolution(data, value.(x))