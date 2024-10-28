.data
    vetor: .word 200, 190, 340, 100
	tamanho: .word 4
    limiar: .word 200
	
    ##### START MODIFIQUE AQUI START #####
	

    ##### END MODIFIQUE AQUI END #####

.text
    jal ra, main
     
    # utilizado para correção (considerando um limiar de 200 para o vetor de exemplo após a aplicação do reajuste.
    addi a4, x0, 3
    beq a4, t0, FIM # Verifica a quantidade de salários acima do limiar.

main:
    ##### START MODIFIQUE AQUI START #####

    la a0, vetor # lendo o ponteiro onde o vetor está
	lw a1, tamanho # lendo o tamanho do vetor
    lw a2, limiar # lendo o limiar desejado

    add t0, x0, x0 # Setando como zero
    addi x22, x0, 2 # Registrador significando o número 2
    addi x23, x0, 3 # Registrador significando o número 3
    add x20, x0, x0 # Contador do o loop
    addi sp, sp, -8 # Ponteiro da pilha
    sw ra, 0(sp) # Guardando o ponto de retorno na pilha de memória
    
    jal ra, aplica_reajuste
    
    lw ra, 0(sp) # Adquirindo de volta o valor de retorno para o .text
    addi sp, sp 8 # Voltando com o ponteiro da pilha
    jalr x0, 0(ra) # Retornando para o .text
    
    ##### END MODIFIQUE AQUI END #####

##### START MODIFIQUE AQUI START #####
aplica_reajuste:   
    bne x20, a1, iteracao # Se não tiver chegado ao final do vetor, faça a próxima iteração
	jalr x0, 0(ra) # Retornando para a main
    
iteracao:
	lw x21, 0(a0) # Carregando o elemento atual do vetor
	mul x21, x21, x23 # Multiplicando por 3
    div x21, x21, x22 # Dividindo por 2
   	sw x21, 0(a0) # Salvo o novo valor na memória 
    bgt x21, a2, acima_limiar
    beqz x0, fim_iteracao
    
acima_limiar:
	addi t0, t0, 1
    beqz x0, fim_iteracao

fim_iteracao:
	addi x20, x20, 1
    addi a0, a0, 4
    beqz x0, aplica_reajuste
    
##### END MODIFIQUE AQUI END #####
    
FIM: addi x0, x0, 1