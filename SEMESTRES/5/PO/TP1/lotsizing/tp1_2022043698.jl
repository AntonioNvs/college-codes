#= 

LOTSIZING COM BACKLOG

Nome: Antônio Caetano Neves Neto
Matrícula: 2022043698

=#

using JuMP
using HiGHS

# Definindo a estrutura por período
mutable struct PeriodData
    prod_custo::Int
    demanda::Int
    est_custo::Int
    multa::Int
end

# Definindo a estrutura de dados do problema.
mutable struct LotsizingData
    n::Int
    arr::Array{PeriodData}
end

function readData(file)
    arr = []
    n = 0

    for line in eachline(file)
        q = split(line, "\t")

        id = 0; value = 0

        if q[1] == "n"
            n = parse(Int, q[2])

            # Adicionando por padrão todos os períodos, dado n.
            for i=1:n
                push!(arr, PeriodData(0, 0, 0, 0))
            end
        else
            # De antemão, já armazena os valores.
            id = parse(Int, q[2])
            value = parse(Int, q[3])
        end
        
        # Redireciona os valores para cada variável, de acordo com o período.
        if q[1] == "c"
            arr[id].prod_custo = value
        end

        if q[1] == "d"
            arr[id].demanda = value
        end

        if q[1] == "s"
            arr[id].est_custo = value
        end

        if q[1] == "p"
            arr[id].multa = value
        end
    end

    return LotsizingData(n, arr)
end

# Lendo o arquivo de entrada.
file = open(ARGS[1], "r")
data = readData(file)

# Criando o modelo de programação linear.
model = Model(HiGHS.Optimizer)

# Definindo as variáveis de decisão.
@variable(model, prod[1:data.n] >= 0)
@variable(model, est[1:data.n+1], Int)
@variable(model, custo[1:data.n] >= 0)

for i=1:data.n
    # O estoque tem que ser menor ou igual a quantidade de produtos existentes menos a demanda.
    @constraint(model, est[i+1] == est[i] + prod[i] - data.arr[i].demanda)

    # Aqui verificamos qual custo é menor para minirmizar a variável.
    @constraint(model, custo[i] >= data.arr[i].est_custo*est[i+1])
    @constraint(model, custo[i] >= data.arr[i].multa*est[i+1]*-1)
end

# O primeiro período não tem estoque do anterior
@constraint(model, est[1] == 0)
# Não pode atrasar ou sobrar nenhum produto no último período
@constraint(model, est[data.n+1] == 0)

# A soma de toda a produção tem que ser igual ao da demanda.
@constraint(model, sum(prod[i] for i=1:data.n) == sum(data.arr[i].demanda for i=1:data.n))

# Queremos minimizar o custo do problema.
@objective(model, Min, 
    sum(prod[i]*data.arr[i].prod_custo + custo[i] for i=1:data.n)
)

# Resolvendo o modelo.
optimize!(model)

sol = objective_value(model)
println("TP1 2022043698 = ", sol)

# function printSolution(data, prod, custo)
#     for i=1:data.n
#         println("CUSTO ", i, " - ", prod[i])
#     end
# end

# printSolution(data, value.(prod), value.(custo))