.data
    vetor: .word 0 0 0 0
    length: .word 4

    ##### START MODIFIQUE AQUI START #####


    ##### END MODIFIQUE AQUI END #####

.text
    ##### START MODIFIQUE AQUI START #####

	la t2, vetor
    lw t3, length

	# Por definição abaixo, x10 conta o número de pares e x11 o número de ímpares
    add x10, x0, x0
    add x11, x0, x0
    
    ##### END MODIFIQUE AQUI END #####

    jal x1, contador
    
    addi x14, x0, 2 # utilizado para correção
    beq x14, x10, FIM # Verifica # de pares
    beq x14, x11, FIM # Verifica # de ímpares

    ##### START MODIFIQUE AQUI START #####
    contador: 
    	add x19, x10, x11 # Soma a quantidade de números pares e ímpares
        bne x19, t3, iteracao # Se não tiver chegado ao final do vetor, faça uma iteração
    	jalr x0, 0(x1) # Retornando a função
    iteracao:
    	lw t4, 0(t2) # Fazendo o load do elemento atual
    	andi t5, t4, 1 # Verificando se o número é par com a operação lógica E
        bnez t5, impar
        addi x10, x10, 1 # Adiciona 1 nos números pares
        addi t2, t2, 4
        beq x0, x0, contador
    impar:
    	addi x11, x11, 1 # Adiciona 1 nos números ímpares
        addi t2, t2, 4
        beq x0, x0, contador
    	
    ##### END MODIFIQUE AQUI END #####

    FIM: addi x0, x0, 1