import os
import re
from datetime import datetime
from tabulate import tabulate
from colorama import init, Fore, Style

init(autoreset=True)

CATALOG_FILE = "catlg.txt"
COMPRAS_FILE = "compras.txt"

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def validar_nome(nome):
    return bool(re.match(r'^[A-Za-zÀ-ÿ ]+$', nome))

def validar_cpf(cpf):
    return cpf.isdigit() and len(cpf) == 11

def validar_cep(cep):
    return bool(re.match(r'^\d{5}-\d{3}$', cep))

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
        print(f"{Fore.RED}Nome inválido. Use apenas letras e espaços.{Style.RESET_ALL}")

    while True:
        cpf = input("CPF (somente números): ")
        if validar_cpf(cpf):
            break
        print(f"{Fore.RED}CPF inválido. Deve ter 11 dígitos.{Style.RESET_ALL}")

    while True:
        cep = input("CEP (formato 00000-000): ")
        if validar_cep(cep):
            break
        print(f"{Fore.RED}CEP inválido. Use o formato 00000-000.{Style.RESET_ALL}")

    while True:
        nasc = input("Data de nascimento (dd/mm/aaaa): ")
        try:
            idade = calcular_idade(nasc)
            break
        except:
            print(f"{Fore.RED}Data inválida.{Style.RESET_ALL}")

    limpar_tela()
    print("Cadastro finalizado com sucesso!")
    return {'email': email, 'nome': nome, 'cpf': cpf, 'cep': cep, 'idade': idade}

def ler_catalogo_arquivo(caminho=CATALOG_FILE):
    catalogos = {}
    sessao_atual = None

    if not os.path.exists(caminho):
        print(f"Arquivo {caminho} não encontrado.")
        return catalogos

    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            if linha.startswith('[') and linha.endswith(']'):
                sessao_atual = linha[1:-1]
                catalogos[sessao_atual] = []
            else:
                if sessao_atual is None:
                    continue
                if ';' in linha:
                    produto, preco = linha.split(';')
                    catalogos[sessao_atual].append((produto.strip(), float(preco)))
    return catalogos

def mostrar_tabela(titulo, itens):
    tabela_colorida = [[produto, f"{Fore.GREEN}R$ {preco:.2f}{Style.RESET_ALL}"] for produto, preco in itens]
    print(f"\n=== {titulo} ===")
    print(tabulate(tabela_colorida, headers=["Produto", "Preço"], tablefmt="fancy_grid"))

def adicionar_ao_carrinho(lista, carrinho, total):
    nomes_produtos = [produto.lower() for produto, _ in lista]

    while True:
        entrada = input("Adicione um produto (nome [quantidade]x) ou 'n' para sair: ").lower()
        if entrada == 'n':
            break

        # Checar código secreto
        if "dev123" in entrada:
            return "dev123", total

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

def menu_principal():
    catalogos = ler_catalogo_arquivo()
    if not catalogos:
        print("Nenhum catálogo disponível para compra.")
        return [], 0

    carrinho = []
    total = 0

    while True:
        limpar_tela()
        print(f"{Fore.BLUE}O que deseja ver? (Atendimento){Style.RESET_ALL}")
        tabela_opcoes = [[str(i+1), nome] for i, nome in enumerate(catalogos.keys())]
        print(tabulate(tabela_opcoes, headers=["Sessão", "Descrição"], tablefmt="fancy_grid"))

        escolha = input("Escolha a sessão (aperte 'n' para sair): ").lower()
        if escolha == 'n':
            break

        if escolha == "dev123":
            return "dev123", total

        try:
            idx = int(escolha) - 1
            if idx < 0 or idx >= len(catalogos):
                raise ValueError
            nome_sessao = list(catalogos.keys())[idx]
            lista_produtos = catalogos[nome_sessao]
            mostrar_tabela(nome_sessao, lista_produtos)

            resultado = adicionar_ao_carrinho(lista_produtos, carrinho, total)
            if resultado == "dev123":
                return "dev123", total
            else:
                carrinho, total = resultado

        except ValueError:
            print("Opção inválida. Tente novamente.")
            input("Pressione Enter para continuar...")

    return carrinho, total

def revisar_carrinho(carrinho, total):
    while True:
        limpar_tela()
        print("=== Seu Carrinho ===")
        if not carrinho:
            print("Carrinho vazio.")
            input("Pressione Enter para continuar...")
            break

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
                try:
                    parcelas = int(input("Escolha o número de parcelas (1 a 5): "))
                    if 1 <= parcelas <= 5:
                        print(f"Você selecionou pagamento no Crédito em {parcelas}x sem juros.")
                        break
                except:
                    pass
                print("Número inválido, tente novamente.")
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
        ["Email", f"{Fore.BLUE}{cliente['email'] if cliente else 'Não cadastrado'}{Style.RESET_ALL}"],
        ["Total antes do desconto", f"R$ {total:.2f}"],
        ["Desconto aplicado", f"{int(desconto*100)}%"],
        ["Total a pagar", f"{Fore.GREEN}R$ {valor_final:.2f}{Style.RESET_ALL}"],
        ["Forma de pagamento", "Débito" if forma_pagamento == '1' else f"Crédito em {parcelas}x"],
    ]

    print(tabulate(dados, tablefmt="fancy_grid"))

    print("\nItens comprados:")
    tabela_itens = [[produto, qtd, f"R$ {preco:.2f}", f"R$ {preco*qtd:.2f}"] for produto, qtd, preco in carrinho]
    print(tabulate(tabela_itens, headers=["Produto", "Qtd", "Preço unit", "Subtotal"], tablefmt="fancy_grid"))

    return valor_final

def salvar_compra(cliente, carrinho, total, forma_pagamento, parcelas):
    datahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    carrinho_texto = "; ".join([f"{produto}({qtd})" for produto, qtd, _ in carrinho])
    linha = f"{datahora} | {cliente['email'] if cliente else 'Sem cadastro'} | {cliente['nome'] if cliente else 'Sem cadastro'} | {cliente['cpf'] if cliente else 'Sem cadastro'} | {cliente['cep'] if cliente else 'Sem cadastro'} | {cliente['idade'] if cliente else 'Sem cadastro'} | {carrinho_texto} | {total:.2f} | {'Débito' if forma_pagamento == '1' else 'Crédito'} em {parcelas}x\n"

    with open(COMPRAS_FILE, "a", encoding="utf-8") as f:
        f.write(linha)

def mostrar_compras():
    if not os.path.exists(COMPRAS_FILE):
        print("Nenhuma compra registrada.")
        return

    print("\n=== Histórico de Compras ===")
    with open(COMPRAS_FILE, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    if not linhas:
        print("Nenhuma compra registrada.")
        return

    for linha in linhas[::-1]:
        print(linha.strip())

def main():
    cliente = None
    limpar_tela()
    print("=== Bem vindo à Farmácia Virtual ===\n")

    resp = input("Deseja fazer cadastro? (s/n): ").lower()
    if resp == 's':
        cliente = cadastro_cliente()

    while True:
        carrinho, total = menu_principal()

        if carrinho == "dev123":
            print(f"\n{Fore.MAGENTA}*** CÓDIGO SECRETO ATIVADO ***{Style.RESET_ALL}\n")
            mostrar_compras()
            input("Pressione Enter para voltar ao menu principal...")
            continue

        if not carrinho:
            print("Carrinho vazio. Finalizando programa.")
            break

        carrinho, total = revisar_carrinho(carrinho, total)

        if not carrinho:
            print("Carrinho vazio. Finalizando programa.")
            break

        forma_pagamento, parcelas = pagamento(total)
        valor_final = resumo_compra(cliente, carrinho, total, forma_pagamento, parcelas)

        resp = input("Confirmar compra? (s/n): ").lower() 
        if resp == 's':
            salvar_compra(cliente, carrinho, valor_final, forma_pagamento, parcelas)
            print(f"{Fore.GREEN}Compra realizada com sucesso!{Style.RESET_ALL}")
        else:
            print("Compra cancelada.")

        input("Pressione Enter para continuar...")

if __name__ == "__main__":
    main()
