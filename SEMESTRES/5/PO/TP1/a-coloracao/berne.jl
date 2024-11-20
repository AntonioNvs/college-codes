using JuMP
using HiGHS

mutable struct CliqueData
    n::Int #numero de vertices
    ng::Array{Array{Int}} #vizinhancas
end

function readData(file)
	n = 0
	ng = [[]]
	for l in eachline(file)
		q = split(l, "\t")

		if q[1] == "n"
			n = parse(Int64, q[2])
			ng = [[] for i=1:n]
		elseif q[1] == "e"
			v = parse(Int64, q[2])
			u = parse(Int64, q[3])
			push!(ng[v], u)
			push!(ng[u], v)
		end
	end
	return CliqueData(n,ng)
end



function printSolution(data, y, x)
	for i in 1:data.n
		if y[i] >= 1
			print("Cor ", i, ": ")
			for j=1:data.n
				if x[i,j] >= 1
					print(j, " ")
				end
			end
			println()
		end
	end
end

model = Model(HiGHS.Optimizer)

file = open(ARGS[1], "r")

data = readData(file)


@variable(model, y[i=1:data.n],Bin)
@variable(model, x[i=1:data.n,j=1:data.n], Bin) # Cada linha representa uma cor e cada coluna um vertice
@variable(model, z[i=1:data.n,j=(i+1):data.n,k=1:data.n,l=1:data.n], Bin) 

# Inicio coloração


#Cada vertice pode ter apenas uma cor
for j=1:data.n
	@constraint(model, sum(x[i,j] for i=1:data.n) == 1)
end


# Para cada par de vertices adjacentes, eles nao podem ter a mesma cor ativa
# A matriz x na posição i,j representa a cor i no vertice j
for i = 1:data.n
	for j in data.ng[i]
		for k = 1:data.n
			@constraint(model, x[k,i] + x[k,j] <= y[k]) # Caso a cor z esteja ativa, os vertices i e j nao podem ter a mesma cor, caso contrario, a soma sera menor igual a 0
		end
    end
end

for k=1:data.n
	@constraint(model, sum(x[k,j] for j=1:data.n) >= y[k]) # Se a cor k esta ativa, entao existe pelo menos um vertice com a cor k
end

# FIM COLORAÇÃO

for i=1:data.n # cor 1
	for j=(i+1):data.n # cor 2
		for k=1:data.n # vertice 1
			for l=1:data.n # vertice 2
				if l in data.ng[k] # garante que so havera conexao entre i e j se k e l forem adjacentes e l tiver cor j e k tiver cor i
					@constraint(model, z[i,j,k,l] <= x[i,k]) 
					@constraint(model, z[i,j,k,l] <= x[j,l]) 
				else
					@constraint(model, z[i,j,k,l] <= 0)
				end
				# garante que so havera arestas entre cores ativas
				@constraint(model, z[i,j,k,l] <= y[j])
				@constraint(model, z[i,j,k,l] <= y[i])
			end
		end
		# Qualquer valor na matriz k,l que seja 1, implica que existe uma aresta entre a cor i e a cor j
		@constraint(model, sum(z[i,j,k,l] for k=1:data.n, l=1:data.n) >= y[i]+y[j]-1) # se a cor i e j estao ativas, entao existe uma aresta entre a cor i e a cor j
	end
end



@objective(model, Max, sum(y[i] for i=1:data.n))

print(model)

optimize!(model)

sol = objective_value(model)
println("TP1 2022043949 = ", sol)

# for i=1:data.n
# 	println("y[",i,"] = ", value.(y)[i])
# end


# printSolution(data, value.(y), value.(x))