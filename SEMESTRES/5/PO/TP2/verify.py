import numpy as np

example_path = "testes/ENTRADA_example_04"

with open(example_path, "r") as src:
    lines = src.read().split("\n")
    N, M = [int(s) for s in lines[0].split(" ") if s != ""]
    
    cost = np.fromstring(lines[1], dtype=np.float64, sep=" ")
    matrix = []
    for i in range(N):
        matrix.append(np.fromstring(lines[2+i], dtype=np.float64, sep=" "))

    matrix = np.array(matrix)
    A = matrix[:, :-1]
    b = matrix[:, -1]

EPLISON = 1e-1

with open("output.txt", "r") as src:
    lines = src.read().split("\n")
    situation = lines[0]

    if situation == "ilimitada":
        solution = np.fromstring(lines[1], dtype=np.float64, sep=" ")
        certificate = np.fromstring(lines[2], dtype=np.float64, sep=" ")

        print("Ilimitada.")
        print(f"Solução dada é {'válida' if np.all(np.dot(A, solution) == b) else 'não válida'}")
        print(f"""Certificado dado é {
            'válida' if np.all(np.abs(np.dot(A, certificate)) < EPLISON) and np.all(certificate >= 0) and np.dot(cost, certificate) >= -EPLISON else 'não válida'
            }""")
        print()    

    elif situation == "inviavel":
        certificate = np.fromstring(lines[1], dtype=np.float64, sep=" ")
        
        print("Inviável.")
        print(f"Certificado é {'válido' if np.dot(certificate, b) < 0 and np.all(np.dot(certificate, A)+EPLISON > 0) else 'não válido'}")
    else:
        vo = float(lines[1])
        solution = np.fromstring(lines[2], dtype=np.float64, sep=" ")
        certificate = np.fromstring(lines[3], dtype=np.float64, sep=" ")

        print("Ótimo.")
        print(f"Solução dada é {'válida' if np.all(np.abs(np.dot(A, solution)-b) < EPLISON) else 'não válida'}")
        print(f"Certificado é {'válido' if np.all(np.dot(certificate, A)-cost >= -EPLISON) and abs(np.dot(certificate, b)-vo) < EPLISON else 'não válido'}")