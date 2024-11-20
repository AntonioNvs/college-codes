#= 

EMPACOTAMENTO

Nome: Antônio Caetano Neves Neto
Matrícula: 2022043698

=#

using JuMP
using HiGHS

# Definindo a estrutura de dados do objeto.
mutable struct ObjetoData
    id::Int
    weight::Float32
end

# Definindo a estrutura de dados do problema.
mutable struct EmpacotamentoData
    n::Int # número de objetos
    objs::Array{ObjetoData} # vetor de objetos
end

function readData(file)
    objs = []
    idx = 0
    n = 0

    for line in eachline(file)
        # Lendo o número de objetos, pois é a primeira linha.
        if idx == 0
            _, n = split(line, "\t")
            n = parse(Int, n)
            idx += 1
        else
            # Lendo os objetos.
            _, id, weight = split(line, "\t")
            push!(objs, ObjetoData(parse(Int, id), parse(Float32, weight)))
        end
    end

    return EmpacotamentoData(n, objs)
end

# Função para imprimir a solução.
function printSolution(data, x)
    sol = 0
    # Para cada local, verifica se existe algum objeto.
    for i=1:data.n
        exists = 0
        for j=1:data.n
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

# Criando o modelo.
model = Model(HiGHS.Optimizer)

# Variável para armazenar se o objeto i está no local j.
@variable(model, x[1:data.n, 1:data.n], Bin)

# A soma de todos os objetos em um local não pode ultrapassar 20.
for i=1:data.n
    @constraint(model, sum(x[i, j] * data.objs[j].weight for j=1:data.n) <= 20)
end

# Cada objeto deve estar em um local.
for j=1:data.n
    @constraint(model, sum(x[i, j] for i=1:data.n) == 1)
end

# Para minimizar o número de locais, é o mesmo que minimizar a soma das linhas
# nas quais os objetos estão.
@objective(model, Min, sum(x[i, j]*i for i=1:data.n, j=1:data.n))

# Resolvendo o modelo.
optimize!(model)

printSolution(data, value.(x))