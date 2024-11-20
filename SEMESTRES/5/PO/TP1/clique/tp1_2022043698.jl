#= 

CLIQUE

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

# Lendo o arquivo de entrada.
file = open(ARGS[1], "r")
data = readData(file)

# Criando o modelo de programação linear.
model = Model(HiGHS.Optimizer)

# Definindo as variáveis de decisão.
@variable(model, x[1:data.n], Bin)

# Queremos maximizar o número de vértices selecionados.
@objective(model, Max, sum(x[i] for i=1:data.n))

# Construindo as restrições para garantir que os vértices selecionados formem um clique.
for i=1:data.n
    for j=(i+1):data.n
        @constraint(model, x[i] + x[j] <= 1 + data.edges[i][j])
    end
end

# Resolvendo o modelo.
optimize!(model)

sol = objective_value(model)
println("TP1 2022043698 = ", sol)

