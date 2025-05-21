
# Trabalho da faculdade
# Gustavo Eidi, Vitoria A, Maria Eduarda
# "Site de farmacia" 
# 
# app de compras calculos

import os
from tabulate import tabulate
import re
from datetime import datetime
from colorama import init, Fore, Style
#import aiosqlite

#nome arquivo aiosqlite = farme_app.db

init(autoreset=True)

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def validar_nome(nome):
    return bool(re.match(r'^[A-Za-zÀ-ÿ ]+$', nome))

def validar_cpf(cpf):
    return cpf.isdigit() and len(cpf) == 11

def formatar_cpf(cpf):
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

def validar_cep(cep):
    return bool(re.match(r'^\d{6}-\d{3}$', cep))

def calcular_idade(nasc):
    hoje = datetime.today()
    nasc_dt = datetime.strptime(nasc, '%d/%m/%Y')
    idade = hoje.year - nasc_dt.year - ((hoje.month, hoje.day) < (nasc_dt.month, nasc_dt.day))
    return idade

def cadastro_cliente():
    print("=== Cadastro de Cliente ===")
    email = input("Email: ")

    while True:
        nome = input("Nome: ")
        if validar_nome(nome):
            break
        print(f"{Fore.RED}Nome inválido. Use apenas letras e espaços: .{Style.RESET_ALL}")

    while True:
        cpf = input("CPF: ")
        if validar_cpf(cpf):
            break
        print(f"{Fore.RED}CPF inválido.{Style.RESET_ALL}")

    while True:
        cep = input("CEP: ")
        if validar_cep(cep):
            break
        print(f"{Fore.RED}CEP inválido.{Style.RESET_ALL}")

    while True:
        nasc = input("Data de nascimento: ")
        try:
            idade = calcular_idade(nasc)
            break
        except:
            print(f"{Fore.RED}Data inválida.{Style.RESET_ALL}")

    limpar_tela()
    print("Cadastro finalizado com sucesso!")
    return {'email': email, 'nome': nome, 'cpf': cpf, 'cep': cep, 'idade': idade}

def mostrar_tabela(titulo, itens):
    tabela_colorida = [[produto, f"{Fore.GREEN}R$ {preco:.2f}{Style.RESET_ALL}"] for produto, preco in itens]
    print(f"\n=== {titulo} ===")
    print(tabulate(tabela_colorida, headers=["Produto", "Preço"], tablefmt="fancy_grid"))

def adicionar_ao_carrinho(lista, carrinho, total):
    nomes_produtos = [produto.lower() for produto, _ in lista]

    while True:
        entrada = input("Adicione um produto ou aperte 'n' para sair: ").lower()
        if entrada == 'n':
            break

        padrao = r'(.*?)\s*(\d+)x$'
        match = re.match(padrao, entrada)

        if match:
            nome_prod = match.group(1).strip()
            qtd = int(match.group(2))
            if nome_prod in nomes_produtos:
                idx = nomes_produtos.index(nome_prod)
                produto, preco = lista[idx]
                carrinho.append((produto, qtd, preco))
                total += preco * qtd
                print(f"{produto} {qtd}x adicionado no carrinho.")
            else:
                print("Produto não encontrado. Verifique o nome e tente novamente.")
        else:
            nome_prod = entrada.strip()
            if nome_prod in nomes_produtos:
                idx = nomes_produtos.index(nome_prod)
                produto, preco = lista[idx]
                carrinho.append((produto, 1, preco))
                total += preco
                print(f"{produto} 1x adicionado no carrinho.")
            else:
                print("Produto não encontrado. Verifique o nome e tente novamente.")

    return carrinho, total

### colocara isso no txt ###
def menu_principal():
    catalogos = {
        '1': ('Medicamentos', [["Paracetamol", 10], ["Ibuprofeno", 15]]),
        '2': ('Cuidados pessoais', [["Shampoo", 20], ["Condicionador", 25]]),
        '3': ('Produtos naturais', [["Whey", 129], ["Vitamina C", 35]]),
        '4': ('Estoque infantil', [["Shampoo Infantil", 18], ["Condicionador Infantil", 20], ["Papinha Maçã", 8], ["Papinha Banana", 9], ["Fralda P", 40], ["Fralda M", 45]]),
        '5': ('Consultas', [["Teste Viral", 100], ["Colocação de Brincos", 80]])
    }

    carrinho = []
    total = 0

    while True:
        limpar_tela()
        print(f"{Fore.BLUE}O que deseja ver? (Atendimento){Style.RESET_ALL}")
        tabela_opcoes = [[chave, nome] for chave, (nome, _) in catalogos.items()]
        print(tabulate(tabela_opcoes, headers=["Sessão", "Descrição"], tablefmt="fancy_grid"))

        escolha = input("Escolha a sessão (aperte n para sair): ")

        if escolha.lower() == 'n':
            break

        if escolha in catalogos:
            nome, lista = catalogos[escolha]
            mostrar_tabela(nome, lista)

            if escolha == '5':  # Consultas (agendamento)
                escolha_cons = input("Deseja agendar qual consulta? (1-Teste viral / 2-Colocação de brincos / n): ")
                if escolha_cons == '1':
                    dia = input("Escolha um dia para agendamento (dd/mm): ")
                    carrinho.append((f"Consulta Teste Viral - Dia {Fore.YELLOW}{dia}{Style.RESET_ALL}", 1, 100))
                    total += 100
                    print(f"Consulta Teste Viral agendada para {dia} e adicionada no carrinho.")
                elif escolha_cons == '2':
                    dia = input("Escolha um dia para agendamento (dd/mm): ")
                    carrinho.append((f"Consulta Brincos - Dia {Fore.YELLOW}{dia}{Style.RESET_ALL}", 1, 80))
                    total += 80
                    print(f"Consulta Brincos agendada para {dia} e adicionada no carrinho.")
            else:
                carrinho, total = adicionar_ao_carrinho(lista, carrinho, total)

    return carrinho, total

def revisar_carrinho(carrinho, total):
    while True:
        limpar_tela()
        print("=== Seu Carrinho ===")
        tabela_carrinho = [[idx+1, produto, qtd, f"{Fore.GREEN}R$ {preco:.2f}{Style.RESET_ALL}", f"{Fore.GREEN}R$ {preco*qtd:.2f}{Style.RESET_ALL}"] for idx, (produto, qtd, preco) in enumerate(carrinho)]
        print(tabulate(tabela_carrinho, headers=["Nº", "Produto", "Qtd", "Preço unit", "Subtotal"], tablefmt="fancy_grid"))

        resp = input("Deseja remover algum item? (s/n): ").lower()
        if resp == 'n':
            break

        try:
            num = int(input("Digite o número do item a remover: "))
            if 1 <= num <= len(carrinho):
                produto, qtd, preco = carrinho[num-1]
                print(f"Produto: {produto} | Quantidade no carrinho: {qtd}")
                remover_qtd = int(input(f"Quantas unidades deseja remover? (1-{qtd}): "))
                if 1 <= remover_qtd < qtd:
                    carrinho[num-1] = (produto, qtd - remover_qtd, preco)
                    total -= preco * remover_qtd
                    print(f"{remover_qtd}x '{produto}' removido do carrinho.")
                elif remover_qtd == qtd:
                    total -= preco * qtd
                    carrinho.pop(num-1)
                    print(f"'{produto}' removido totalmente do carrinho.")
                else:
                    print("Quantidade inválida.")
                input("Pressione Enter para continuar...")
            else:
                print("Número inválido.")
                input("Pressione Enter para continuar...")
        except:
            print("Entrada inválida.")
            input("Pressione Enter para continuar...")

    return carrinho, total

def pagamento(total):
    limpar_tela()
    print("=== Forma de Pagamento ===")
    print("1 - Débito")
    print("2 - Crédito (até 5x sem juros)")

    while True:
        opcao = input("Escolha a forma de pagamento: ")
        if opcao == '1':
            print("Você selecionou pagamento no Débito.")
            parcelas = 1
            break
        elif opcao == '2':
            while True:
                parcelas = int(input("Escolha o número de parcelas (1 a 5): "))
                if 1 <= parcelas <= 5:
                    print(f"Você selecionou pagamento no Crédito em {parcelas}x sem juros.")
                    break
            break
        else:
            print("Opção inválida.")

    return opcao, parcelas

def resumo_compra(cliente, carrinho, total, forma_pagamento, parcelas):
    desconto = 0
    if cliente:
        desconto = 0.05

        if cliente['idade'] > 55:
            desconto = 0.15

    valor_final = total * (1 - desconto)

    print("\n=== Resumo da Compra ===")

    dados = [
        ["Nome", f"{Fore.BLUE}{cliente['nome'] if cliente else 'Não cadastrado'}{Style.RESET_ALL}"],
        ["Email", f"{Fore.BLUE}{cliente['email'] if cliente else '---'}{Style.RESET_ALL}"],
        ["Idade", f"{Fore.BLUE}{cliente['idade'] if cliente else '---'}{Style.RESET_ALL}"],
        ["CEP", f"{Fore.BLUE}{cliente['cep'] if cliente else '---'}{Style.RESET_ALL}"],
        ["CPF", f"{Fore.BLUE}{formatar_cpf(cliente['cpf']) if cliente else '---'}{Style.RESET_ALL}"]
    ]
    print(tabulate(dados, headers=["Informação", "Valor"], tablefmt="fancy_grid"))

    print("\nProdutos comprados:")
    tabela_resumo = [[produto, qtd, f"{Fore.GREEN}R$ {preco:.2f}{Style.RESET_ALL}", f"{Fore.GREEN}R$ {preco*qtd:.2f}{Style.RESET_ALL}"] for produto, qtd, preco in carrinho]
    print(tabulate(tabela_resumo, headers=["Produto", "Qtd", "Preço unit", "Subtotal"], tablefmt="fancy_grid"))

    totais = [
        ["Valor total", f"{Fore.GREEN}R$ {total:.2f}{Style.RESET_ALL}"],
        ["Desconto aplicado", f"{Fore.GREEN}{desconto*100:.0f}%{Style.RESET_ALL}"],
        ["Valor final", f"{Fore.GREEN}R$ {valor_final:.2f}{Style.RESET_ALL}"]
    ]

    if forma_pagamento == '2' and parcelas > 1:
        parcela_valor = valor_final / parcelas
        totais.append([f"Pagamento em {parcelas}x", f"{Fore.GREEN}R$ {parcela_valor:.2f} / parcela{Style.RESET_ALL}"])

    print(tabulate(totais, tablefmt="fancy_grid"))

    pagamento_str = "Débito" if forma_pagamento == '1' else f"Crédito ({parcelas}x)"
    print(f"\nForma de pagamento escolhida: {Fore.YELLOW}{pagamento_str}{Style.RESET_ALL}")

def main():
    limpar_tela()
    cadastro = None
    print(f"\nAperte {Fore.YELLOW}S{Style.RESET_ALL} para efetuar o cadastro ou {Fore.YELLOW}N{Style.RESET_ALL} para continuar sem")
    resp = input("Deseja efetuar um cadastro? ")
    if resp.lower() == 's':
        cadastro = cadastro_cliente()

    carrinho, total = menu_principal()
    carrinho, total = revisar_carrinho(carrinho, total)

    forma_pagamento, parcelas = pagamento(total)

    resumo_compra(cadastro, carrinho, total, forma_pagamento, parcelas)

if __name__ == "__main__":
    main()
