import sys


def CarregarTabela():

	tabela = open("symboltable.txt", "r")
	listaTabela = []

	for linha in tabela:
		listaTabela.append(linha.split())

	print("Tabela carregada!")

	tabela.close()

	return listaTabela

def CarregaFinais():
	arquivo = open("estados.txt", "r")
	listaFinais = []
	for a in arquivo:
		listaFinais.append(a.split())

	return listaFinais

def CarregaPalavras(tokens):
	arquivo = open("palavras.txt", "r")
	listaPalavras = []
	for a in arquivo:
		listaPalavras.append(a.split())

	for a in listaPalavras:
		a.append(None)
		tokens.append(a)

	return tokens

def CarregaRegras():
	arquivo = open("gramatica.txt", "r")
	listaRegras = []
	for a in arquivo:
		listaRegras.append(a)

	return listaRegras

def CarregaSintatica1():
	arquivo = open("tabela sintatica 1 revisada.txt", "r")
	lista = []
	for linha in arquivo:
		lista.append(linha.split())

	arquivo.close()
	return lista

def CarregaSintatica2():
	arquivo = open("tabela sintatica 2.txt", "r")
	lista = []
	for linha in arquivo:
		lista.append(linha.split())

	arquivo.close()
	return lista

def CarregaGramatica():
	fonte = open("gramatica teste 1.txt", "r")
	coisa = open("gramatica teste 2.txt", "r")
	lista = []

	for linha in fonte:
		lista.append(linha.split())
	lala = []
	for linha in coisa:
		lala.append(linha.split())
	for a in range(len(lista)):
		lista[a].append(lala[a])

	return lista

def Analisador(palavras, finais, palavra, estado):
	for teste in palavras:
		if teste[0] == palavra:
			return teste

	if estado[0] == "ERRO":
		return None


	for state in finais:
		if estado[0] == state[0]:
			if state[1] == "#":
				print("ERRO LEXICO ", print(palavra))
				return None
			else:
				if estado[0] == 'S1':
					return [palavra, state[1], "int"]
				if estado[0] == 'S4' or estado[0] == 'S7':
					return [palavra, state[1], "double"]
				if estado[0] == 'S2':
					return [palavra, state[1], palavra]
				if estado[0] == 'S17':
					return [palavra, state[1], "=="]
				if estado[0] == 'S16' or estado[0] == 'S13':
					return [palavra, state[1], palavra]
				if estado[0] == 'S15':
					if palavra == "<>":
						return [palavra, state[1], "!="]
					else:
						return [palavra, state[1], palavra]
				if estado[0] == 'S14':
					return [palavra, state[1], '=']
			
				return [palavra, state[1], None]

def AnalisadorLexico(texto, ptr, estado, gravado, contadorlinha, tokens, teste):

	palavra = ''

	while ptr[0] < len(texto):
		caractere = texto[ptr[0]]

		if caractere.isdigit():
			auxiliar = "D"
		else:
			if caractere.isalpha() and caractere != "e" and caractere != "e":
				auxiliar = "L"
			else:
				auxiliar = caractere


		linhas = len(tabela)
		for i in range(linhas):
			if tabela[i][0] == estado[0]:
				for j in tabela[0]:
					if auxiliar == " " or auxiliar == "\t" or auxiliar == "\n" or auxiliar == "|":						

						if estado[0] == "S8":				# TRATAMENTO PARA LITERAL
							gravado = "S8"
							palavra += caractere
							break
						else:
							if estado[0] == "S11":			# TRATAMENTO PARA COMENTARIOS
								gravado = "S11"
								palavra += caractere
								break
							else:
								gravado = "S0"
					else:
						if j == auxiliar:
							gravado = tabela[i][tabela[0].index(j)]
							if gravado == "#":
								ptr[0] = ptr[0] - 1
								gravado = "S0"
							else:
								# print("Estado atual:", estado, "\tCaractere encontrado:", caractere, "\tProximo estado:", gravado, "\tPTR = ", ptr)
								palavra += caractere		

				if auxiliar not in tabela[0] and auxiliar != " " and auxiliar != "\t" and auxiliar != "\n" and auxiliar != "|":
					if estado[0] == "S8" or estado[0] == "S11":
						palavra += caractere
					else:
						print("ERRO LEXICO NA LINHA:", contadorlinha[0])
						print("Caractere inválido: ", caractere)
						sys.exit()

				if caractere == "\n":
					contadorlinha[0] += 1

		if gravado == "S0":
			if palavra != '' and palavra != '\n' and palavra != '\t' and palavra != None:
				token = Analisador(palavrasReservadas, finais, palavra, estado)
				ptr[0] += 1
				estado[0] = gravado

				for tokenTabela in tokens:
					if (token[0] == tokenTabela[0]) and (token[1] == tokenTabela[1]):
						#print("Token ja existente na tabela")
						return tokenTabela


				teste[0] = caractere
				return token
			palavra = ''


		ptr[0] += 1
		estado[0] = gravado

def getAcao(tabela, state, token):	#tabela = tabela sintaxica1, state = estado do LR, token = token do pedido(pedido[1])
	token = token
	estado = state
	coluna = 0
	linha = 0

	for consulta in tabela:
		if estado == consulta[0]:
			linha = tabela.index(consulta)
	for teste in tabela[0]:
		if token == teste:
			coluna = tabela[0].index(teste)

	palavra = tabela[linha][coluna]
	acao = []
	acao.append(palavra[0:1])
	acao.append(palavra[1:])

	return acao

def GOTO(tabela, state, nTerm):		#tabela = tabela sintatica2, state = estado do LR, nTerm = Não terminal(acao[1])
	estado = state
	token = nTerm

	coluna = 0
	linha = 0

	for consulta in tabela:
		if estado == consulta[0]:
			linha = tabela.index(consulta)
	for teste in tabela[0]:
		if token == teste:
			coluna = tabela[0].index(teste)

	palavra = tabela[linha][coluna]

	return palavra

def Transforma(lexema):
	ajuda = [lexema, lexema, None]
	return ajuda

def InicializaTemp():
	b = open("INTERMEDIARIO.c", "w")
	b.close()

def InicializaObjeto():
	a = open("PROGRAMA.c", "w")
	a.write("#include <stdio.h>\ntypedef char literal[256];\nvoid main(void)\n{")
	a.write("\n\t/*----Variaveis temporarias----*/\n")

def FinalizaObjeto():
	a = open("PROGRAMA.c", "a")
	arq = open("INTERMEDIARIO.c", "r")
	a.write(arq.read())
	a.write("\n}")

def DeclaraTemporarias(quantVarAux):
	arq = open("PROGRAMA.c", "a")
	for a in range(quantVarAux):
		arq.write("\tint T"+str(a)+";\n")
	arq.write("\t/*-----------------------------*/\n")
	arq.close()

def Semantico(regra, pilhaSemantico, simbolo, quantVarAux):
	# print("CHAMEI O SEMANTICO COM", simbolo)
	# kkk = input()
	# print("LISTA DAS TX:", varAux)
	# print("QUANT das TX", quantVarAux)
	# kkk = input()
	if regra == 5:
		arq = open("INTERMEDIARIO.c", "a")
		arq.write("\n\n\n")
		arq.close()
	
	elif regra == 6:
		# for a in pilhaSemantico:
		# 	print(a)
		tipo = pilhaSemantico.pop()
		ide = pilhaSemantico.pop()
		ide[2] = tipo[2]
		pilhaSemantico.append(ide)
		arq = open("INTERMEDIARIO.c", "a")
		arq.write("\t"+tipo[2]+" "+ide[0]+";\n")
		arq.close()
	
	elif regra == 7:
		simbolo[2] = "int"
		pilhaSemantico.append(simbolo)
	
	elif regra == 8:
		simbolo[2] = "double"
		pilhaSemantico.append(simbolo)
	
	elif regra == 9:
		simbolo[2] = "literal"
		pilhaSemantico.append(simbolo)

	elif regra == 11:
		aux = pilhaSemantico.pop()
		if aux[2] != None:
			arq = open("INTERMEDIARIO.c", "a")
			if aux[2] == "literal":
				arq.write("\tscanf(\"%s\", "+aux[0]+");\n")
			elif aux[2] == "int":
				arq.write("\tscanf(\"%d\", &"+aux[0]+");\n")
			elif aux[2] == "double":
				arq.write("\tscanf(\"%lf\", &"+aux[0]+");\n")
		else:
			print("Erro: Variavel nao declarada")	
			sys.exit()

	elif regra == 12:
		arq = open("INTERMEDIARIO.c", "a")
		aux = pilhaSemantico.pop()
		if aux[2] == 'int':
			arq.write("\nprintf(\"%d\","+aux[0]+");\n")
		elif aux[2] == 'double':
			arq.write("\nprintf(\"%lf\","+aux[0]+");\n")
		elif aux[2] == 'literal':
			arq.write("\nprintf(\"%s\","+aux[0]+");\n")
		else:
			arq.write("\nprintf("+aux[0]+");\n")
		arq.close()

	elif regra == 13:
		aux = pilhaSemantico.pop()
		simbolo[0] = aux[0]
		simbolo[1] = aux[1]
		simbolo[2] = aux[2]
		pilhaSemantico.append(simbolo)
	
	elif regra == 14:
		aux = pilhaSemantico.pop()
		simbolo[0] = aux[0]
		simbolo[1] = aux[1]
		simbolo[2] = aux[2]
		pilhaSemantico.append(simbolo)

	elif regra == 15:
		# print("REGRA 15")
		aux = pilhaSemantico.pop()
		if aux[2] != None:
			simbolo[0] = aux[0]
			simbolo[1] = aux[1]
			simbolo[2] = aux[2]
			pilhaSemantico.append(simbolo)
		else:
			print("Erro: Variavel nao declarada")	
			sys.exit()

	elif regra == 17:
		auxOPR2 = pilhaSemantico.pop()
		auxOPRD = pilhaSemantico.pop()
		auxOPR1 = pilhaSemantico.pop()	#id
		if auxOPR1[2] != None:
			if auxOPR1[2] == auxOPR2[2]:
				arq = open("INTERMEDIARIO.c", "a")
				arq.write(auxOPR1[0]+" "+auxOPRD[2]+" "+auxOPR2[0]+";\n")
				arq.close()
			else:
				print("Erro: Tipos diferentes para atribuicao")
				sys.exit()

		else:
			print("Erro: Variavel nao declarada")
			sys.exit()

	elif regra == 18:
		# print("REGRA 18")
		auxOPR2 = pilhaSemantico.pop()
		auxOPRD = pilhaSemantico.pop()
		auxOPR1 = pilhaSemantico.pop()

		if (auxOPR2[2] == auxOPR1[2]) and (auxOPR1[2] != "literal" and auxOPR2 != "literal"):
			quantVarAux[0] += 1
			t = "T"+str(quantVarAux[0]-1)
			simbolo[0] = "T"+str(quantVarAux[0]-1)
			simbolo[2] = auxOPR1[2]					##################		TESTE
			arq = open("INTERMEDIARIO.c", "a")

			arq.write(t+" = "+auxOPR1[0]+" "+auxOPRD[2]+" "+auxOPR2[0]+";\n")
			arq.close()
			pilhaSemantico.append(simbolo)
			# kkk = input()
		else:
			print("Erro: Operandos com tipos incompativeis")
			sys.exit()

	elif regra == 19:
		# print("REGRA 19")
		# print("SIMBOLO", simbolo)
		aux = pilhaSemantico.pop()
		# print("aux", aux)
		simbolo[0] = aux[0]
		simbolo[1] = aux[1]
		simbolo[2] = aux[2]
		pilhaSemantico.append(simbolo)

	elif regra == 20:
		# print("REGRA 20")
		aux2 = pilhaSemantico.pop()
		aux1 = pilhaSemantico.pop()
		# print(aux2)
		# print(aux1)

		if aux1[1] == 'id':
			# print("AAAAAAAAAAAA", simbolo)
			if aux1[2] != None:
				# print("AAAAAAA", simbolo)
				# print("SIMBOLO: ", simbolo[0], "AUX1:", aux1[0])
				simbolo[0] = aux1[0]
				# print("SIMBOLO: ", simbolo[1], "AUX1:", aux1[1])
				simbolo[1] = aux1[1]
				# print("SIMBOLO: ", simbolo[2], "AUX1:", aux1[2])
				simbolo[2] = aux1[2]
				pilhaSemantico.append(simbolo)			
			else:
				print("Erro: Variavel nao declarada")	
				sys.exit()
		else:
			# print("AAAAAAAAAAAA", simbolo)
			if aux2[2] != None:
				# print("AAAAAAA", simbolo)
				# print("SIMBOLO: ", simbolo[0], "AUX1:", aux2[0])
				simbolo[0] = aux2[0]
				# print("SIMBOLO: ", simbolo[1], "AUX1:", aux2[1])
				simbolo[1] = aux2[1]
				# print("SIMBOLO: ", simbolo[2], "AUX1:", aux2[2])
				simbolo[2] = aux2[2]
				pilhaSemantico.append(aux1)
				pilhaSemantico.append(simbolo)			
			else:
				print("Erro: Variavel nao declarada")	
				sys.exit()

	elif regra == 21:
		# print("REGRA 21")
		aux = pilhaSemantico.pop()
		simbolo[0] = aux[0]
		simbolo[1] = aux[1]
		simbolo[2] = aux[2]
		pilhaSemantico.append(simbolo)
		# kkk = input()

	elif regra == 23:
		arq = open("INTERMEDIARIO.c", "a")
		arq.write("}\n")
		arq.close()

	elif regra == 24:
		# print("REGRA 24")
		aux = pilhaSemantico.pop()
		arq = open("INTERMEDIARIO.c", "a")
		arq.write(" if("+aux[0]+"){\n")
		arq.close()

	elif regra == 25:
		# print("REGRA 25")
		auxOPR2 = pilhaSemantico.pop()
		auxOPRD = pilhaSemantico.pop()
		auxOPR1 = pilhaSemantico.pop()
		if auxOPR1[2] == auxOPR2[2]:
			quantVarAux[0] += 1
			t = "T"+str(quantVarAux[0]-1)
			simbolo[0] = "T"+str(quantVarAux[0]-1)
			arq = open("INTERMEDIARIO.c", "a")
			# print(t)
			arq.write(t+" = "+auxOPR1[0]+" "+auxOPRD[2]+" "+auxOPR2[0]+";\n")
			arq.close()
			pilhaSemantico.append(simbolo)
		else:
			print("Erro: Operandos com tipos incompativeis")
			sys.exit()

	else:
		kkk = 1
		# print("NAO PASSOU REGRA:", regra)

def Sintatico(texto, ptr, estado, gravado, contadorlinha, tokens, teste, pilhaSemantico, quantVariaveisAux):

	tabelaSintatica1 = CarregaSintatica1()
	tabelaSintatica2 = CarregaSintatica2()
	gramatica = CarregaGramatica()
	InicializaTemp()

	w = ['$']
	pilha = ['$']
	pilha.append('0')

	# ip é o primeiro elemento que esta em w
	# s é o topo da pilha
	# a é o que esta contido em ip (pedido)

	pedido = AnalisadorLexico(texto, ptr, estado, gravado, contadorlinha, tokens, teste)
	###############
	###############
	w.append(pedido[1])
	# print("W:", w)
	
	while True:
		# print("pilha Semantico")
		# for a in pilhaSemantico:
		# 	print(a)
		# if pedido != None:
		# 	print("\nEXECUTANDO",pedido[0], pedido[1])
		# kkk = input()
		if pedido != None:
			testePilha = 0
			for a in pilhaSemantico:
				if a[0] == pedido[0]:
					pedido = a

	###################################	ANALISA TERMINAIS QUE ENTRAM	#################
			if pedido[1] == "id" or pedido[1] == "literal" or pedido[1] == "num" or pedido[1] == "opr" or pedido[1] == "opm" or pedido[1] == "rcb":
				pilhaSemantico.append(pedido)
		acao = getAcao(tabelaSintatica1, pilha[len(pilha)-1], w[len(w)-1])
		# print("ACAO RESULTANTE:", acao)
		fazer = acao[0]
		t = acao[1]
		# print("PILHA: ", pilha)
		# print("VAMOS FAZER A VERIFICAÇÃO DA ACAO")
		if fazer == 's':				# SE FOR SHIFT
			# print(pilha[len(pilha)-1], w[len(w)-1])
			# print("SHIFT", t)
			# print("s", fazer, "\t\ta", t)
			pilha.append(pedido[1])
			pilha.append(t)
			# print("CADEIA",w)
			w.pop()
			pedido = AnalisadorLexico(texto, ptr, estado, gravado, contadorlinha, tokens, teste)
			# print(pedido)
			if pedido != None:
				w.append(pedido[1])
			# print("W:", w)
		else:
			# TAMANHO DO BETA DA REGRA = len(gramatica[int(acao[1])-1][1])
			if fazer == 'r':
				# print(pilha[len(pilha)-1], w[len(w)-1])
				# SE FOR REDUCE
				# print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
				# print("REDUCE: regra", t)
				
				A = gramatica[int(t)-1][0]
				beta = gramatica[int(t)-1][1]
				regra = gramatica[int(t)-1]
				print("Regra", t, ":   ", A, "->", beta)

				count = 0
				while count < len(beta)*2:
					# print("PILHA:", pilha)
					pilha.pop()
					count+=1


				# print("PILHA:", pilha)
				topo = pilha[len(pilha)-1][:]
				# print("TOPO:",topo)
				pilha.append(A)
				novo = GOTO(tabelaSintatica2, topo, A)
				pilha.append(novo)


				#  INDICA REGRA
				numRegra = gramatica.index(regra)+1
				# print("Regra numero", numRegra)
				

		##########INSIRA SUA CHAMADA AO SEMANTICO AQUI############






				if pedido != None:
					if pedido[1] == "id":
						# print("ACHEI UM ID")
						pilhaSemantico.pop()
						# for a in pilhaSemantico:
						# 	print(a)
						# pilhaSemantico.append(pedido)
						# print(pilhaSemantico)
						Semantico(numRegra, pilhaSemantico, pedido, quantVariaveisAux)
					else:
						# print("NAO E UM ID", A)
						amigo = Transforma(A)
						Semantico(numRegra, pilhaSemantico, amigo, quantVariaveisAux)
						






				# aux = input()


		##########################################################



				
			else:
				if fazer == 'a':
					print(pilha[len(pilha)-1], w[len(w)-1])
					print("ACEITOU")
					return True
				else:
					print("ERRO SINTATICO NA LINHA", contadorlinha[0])
					# print(pilha[len(pilha)-1], w[len(w)-1])
					return False


		# if pedido == None:
		# 	print("ERRO LEXICO NA LINHA", contadorlinha[0], "Nenhuma palavra pode começar com:", teste[0], "<-")
		# 	sys.exit()
		# else:
		# 	if pedido not in tokens:
		# 		if pedido[1] == "id":
		# 			tokens.append(pedido)

		# print(pedido)		
		# aux = input()



#############################################
####	VARIAVEIS COMUNS AO CODIGO	#########
#############################################

fonte = open("fonte.txt", "r")
texto = fonte.read()
fonte.close()
texto += "|"
estado = ["S0"]
gravado = estado[0]
teste = [0]
tokens = []
ptr = [0]
contadorlinha = [1]
pilhaSemantico = []
quantVariaveisAux = [0]

############TABELAS###########
finais = CarregaFinais()
tabela = CarregarTabela()
palavrasReservadas = CarregaPalavras(tokens)
##############################


############INICIO DO PROGRAMA#############################
InicializaTemp()
InicializaObjeto()

sim = Sintatico(texto, ptr, estado, gravado, contadorlinha, tokens, teste, pilhaSemantico, quantVariaveisAux)

DeclaraTemporarias(quantVariaveisAux[0])

if sim:
	print("CÓDIGO SINTATICAMENTE CORRETO")


FinalizaObjeto()





# print("TABELA DE TOKENS")
# for a in tokens:
# 	print(a)


