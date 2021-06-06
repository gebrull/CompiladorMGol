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

def Sintatico(texto, ptr, estado, gravado, contadorlinha, tokens, teste):

	tabelaSintatica1 = CarregaSintatica1()
	tabelaSintatica2 = CarregaSintatica2()
	gramatica = CarregaGramatica()


	w = ['$']
	pilha = ['$']
	pilha.append('0')

	# ip é o primeiro elemento que esta em w
	# s é o topo da pilha
	# a é o que esta contido em ip (pedido)

	pedido = AnalisadorLexico(texto, ptr, estado, gravado, contadorlinha, tokens, teste)
	w.append(pedido[1])
	# print("W:", w)
	
	while True:
		# print("EXECUTANDO",pedido[1])
		acao = getAcao(tabelaSintatica1, pilha[len(pilha)-1], w[len(w)-1])
		# print("ACAO RESULTANTE:", acao)
		fazer = acao[0]
		t = acao[1]
		# print("PILHA: ", pilha)
		# print("VAMOS FAZER A VERIFICAÇÃO DA ACAO")
		if fazer == 's':				# SE FOR SHIFT
			print(pilha[len(pilha)-1], w[len(w)-1])
			print("SHIFT", t)
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
				print(pilha[len(pilha)-1], w[len(w)-1])
				# SE FOR REDUCE
				# print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
				print("REDUCE: regra", t)
				A = gramatica[int(t)-1][0]
				beta = gramatica[int(t)-1][1]
				# print("Regra", t, ":   ", A, "->", beta)

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
				# print(pilha)
				print("PRODUÇÃO:", A, "->", ''.join(beta))
				# print(gramatica[int(t)-1])

				##########INSIRA SUA CHAMADA AO SEMANTICO AQUI############

				# de acordo com a posição da gramática, tem um arquivo que escreve no texto



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

############TABELAS###########
finais = CarregaFinais()
tabela = CarregarTabela()
palavrasReservadas = CarregaPalavras(tokens)
##############################



############INICIO DO PROGRAMA#############################



sim = Sintatico(texto, ptr, estado, gravado, contadorlinha, tokens, teste)

if sim:
	print("CÓDIGO SINTATICAMENTE CORRETO")








