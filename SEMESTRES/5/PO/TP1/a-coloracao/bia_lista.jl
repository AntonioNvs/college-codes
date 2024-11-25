using JuMP
using HiGHS

@time begin

mutable struct Grafo
    n::Int # número de arestas
    e::Array{Tuple{Int, Int}} # arestas
    M::Array{Int} # matriz de adjacência
    viz::Vector{Any} # vetor de vizinhos
end

# cálculo da quantidade de arestas, baseado no arquivo de entrada
function count_lines(filename::AbstractString)
    num_lines = 0
    open(filename) do file
        num_lines = countlines(file)
    end
    return num_lines
end

# definição da matriz de adjacência
function toMatrix(v1, v2, n)
    m = zeros(Int, n, n)
    for i = 1:size
        m[v1[i], v2[i]] = 1
        m[v2[i], v1[i]] = 1
    end
    for i = 1:n
        m[i, i] = 1
    end
    return m
end

function readData(file)
	n = 0
    e = []
    v1 = []
    v2 = []
    viz = Vector{Any}[]
    idx = 0
	for l in eachline(file)
		q = split(l, "\t")
		if q[1] == "n"
			n = parse(Int64, q[2]) # define qt vértices
            e = [(0, 0) for i=1:size] # inicializa vetor de arestas
            v1 = [0 for i=1:size]
            v2 = [0 for i=1:size]
            viz = [Vector{Any}() for i=1:n]
		elseif q[1] == "e"
            idx += 1
            v1[idx] = parse(Int, q[2])
            v2[idx] = parse(Int, q[3])
            e[idx] = (parse(Int, q[2]), parse(Int, q[3]))
            push!(viz[v1[idx]], v2[idx])
            push!(viz[v2[idx]], v1[idx])
		end
	end
    M = toMatrix(v1, v2, n)
	return Grafo(n,e, M,viz)
end

model = Model(HiGHS.Optimizer)
# set_silent(model)

file = open(ARGS[1], "r")

size = count_lines(ARGS[1]) - 1 # quantidade de arestas

data = readData(file)


@variable(model, y[1:data.n], Bin) # define a variável: cor i utilizada ou não
@variable(model, m[1:data.n, 1:data.n], Bin) # define matriz de variáveis: cor i atribuída ao vértice j
@variable(model, z[i=1:data.n, j=(i+1):data.n, u=1:data.n, v=1:data.n], Bin) # define a variável: aresta uv, com cores i e j

for j=1:data.n
    @constraint(model, sum(m[i, j] for i=1:data.n) == 1)
end

# @constraint(model, [j=1:data.n], sum(m[i,j] for i=1:data.n) == 1) # define a restrição de que todo vértice deve ter uma cor

for i=1:data.n
    for j in data.viz[i]
        for k in 1:data.n
            @constraint(model, m[k,i] + m[k,j] <= 1) # define a restrição de que vértices adjacentes não podem ter a mesma cor
        end
    end
end

for i=1:data.n 
    for j=(i+1):data.n 
            for u=1:data.n
                for v in data.viz[u] 
                        @constraint(model, z[i,j,u,v] <= m[i,u])
                        @constraint(model, z[i,j,u,v] <= m[j,v])
            end
        end
        @constraint(model, sum(z[i,j,u,v] for u=1:data.n, v in data.viz[u]) >= y[i] + y[j] - 1) 
    end
end

@objective(model, Max, sum(y[i] for i=1:data.n)) # define a função objetivo: maximizar a quantidade de cores utilizadas

optimize!(model)
println("TP1 2022043922 = ", objective_value(model))

end