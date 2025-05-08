
# esse é o modelo completo do "new1cmr.py"
# o codigo ainda não está pronto
# esse modelo/projeto, é meu trabalho pessoal que fiz por diversão
# projeto de banco para incrementar dentro de um site web
# futuramente pretento colocar o tkinter e deixar mais "bonito"
# coloquei varios comentarios para que não fique perido durante a leitura do codigo


import os
from tabulate import tabulate
from colorama import Fore, init
import re

# Inicializa o colorama
init(autoreset=True)

# Função para calcular o salário líquido
def calcular_salario_liquido(salario_bruto):
    desconto = salario_bruto * 0.20
    salario_liquido = salario_bruto - desconto
    return salario_liquido

# Função para converter para outras moedas
def converter_para_moeda(salario_liquido, cotacao):
    return salario_liquido / cotacao

# Função para calcular o investimento com base em 10% de rendimento mensal
def calcular_investimento_mensal(salario_liquido, meses):
    saldo_final = salario_liquido * (1 + 0.10)**meses
    return saldo_final

# Função para calcular o investimento com base em 0.4% de rendimento diário
def calcular_investimento_diario(salario_liquido, dias):
    saldo_final = salario_liquido * (1 + 0.004)**dias
    return saldo_final

# Função para converter meses em anos e meses
def converter_em_anos_meses(meses):
    anos = meses // 12
    meses_restantes = meses % 12
    return anos, meses_restantes

# Limpar a tela
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

# Função para exibir a tabela de forma bonita
def exibir_tabela(dados, cabeçalhos):
    print(tabulate(dados, headers=cabeçalhos, tablefmt="grid"))

# Função para validar CPF
def validar_cpf(cpf):
    cpf = cpf.replace(".", "").replace("-", "")
    if len(cpf) != 11 or not cpf.isdigit():
        return False
    return True

# Função para formatar CPF
def formatar_cpf(cpf):
    cpf = cpf.replace(".", "").replace("-", "")
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

# Função para exibir o título "BANCO GTX" em ASCII
def exibir_titulo():
    titulo = """
  ____    __    __    _  ______  _____
 |  _ )  /  \  |\ \  | |/  ____)/  _  \\
 |  _ \ / -- \ | \ \ | || /    |  | | |
 | |_) ) ____ \|  \ \| || \____|  |_| |
 |____/_/    \_|__|\___|\______)\_____/ 
    """
    print(Fore.GREEN + titulo + Fore.RESET)

# Limpar a tela e exibir o título do banco
limpar_tela()
exibir_titulo()

# Entrada do nome do cliente
nome_cliente = input(f"{Fore.BLUE}Digite seu nome completo: {Fore.RESET}")

# Validar CPF
while True:
    cpf = input(f"{Fore.BLUE}Digite seu CPF: {Fore.RESET}")
    if validar_cpf(cpf):
        cpf_formatado = formatar_cpf(cpf)  # Formatar o CPF
        break
    else:
        limpar_tela()
        exibir_titulo()
        print(f"{Fore.RED}Ops! O CPF está incorreto. Clique Enter para refazer.{Fore.RESET}")
        input()  # Espera o usuário pressionar Enter para refazer a entrada

# Entrada do valor do salário bruto
# Entrada do valor do salário bruto
while True:
    try:
        salario_bruto = float(input("Digite o valor do seu salário bruto (R$): "))
        if salario_bruto < 0:
            print("Número inválido! Por favor, insira um valor não negativo.")
        else:
            break
    except ValueError:
        print("Entrada inválida! Por favor, insira um número válido.")

# Calcular o salário líquido
salario_liquido = calcular_salario_liquido(salario_bruto)

# Exibir o salário líquido
print(f"\n{Fore.GREEN}Salário líquido: R${salario_liquido:.2f}{Fore.RESET}\n")

# Opção de escolha de moeda
moedas = {
    "dolar": ("USD$", 6.18),
    "euro": ("EUR$", 6.68),
    "iene": ("¥", 0.0412),
    "renminbi": ("C¥", 0.8191),
    "won": ("₩", 0.0041)
}

# Perguntar em qual moeda deseja investir
print(f"\n{Fore.YELLOW}Escolha a moeda para converter seu salário:")
for i, moeda in enumerate(moedas, 1):
    print(f"{i}. {moeda.capitalize()}")

opcao_moeda = int(input(f"{Fore.YELLOW}Digite o número da moeda (1-5): {Fore.RESET}"))
moeda_escolhida = list(moedas.values())[opcao_moeda - 1]
simbolo_moeda, cotacao_moeda = moeda_escolhida

# Converter o salário para a moeda escolhida
salario_convertido = converter_para_moeda(salario_liquido, cotacao_moeda)

# Perguntar sobre o tempo de investimento
tempo = input(f"{Fore.YELLOW}Quanto tempo você gostaria de investir? {Fore.RESET}").strip().lower()

# Variáveis para totalizar dias e meses
total_dias = 0
total_meses = 0

# Expressões regulares para extrair unidades de tempo
padroes = {
    "dia": r"(\d+)\s*dias?",
    "semana": r"(\d+)\s*semanas?",
    "mes": r"(\d+)\s*mes(?:es)?",
    "ano": r"(\d+)\s*anos?"
}

# Extrair números conforme padrão de tempo
dias = sum([int(n) * 1 for n in re.findall(padroes["dia"], tempo)])
semanas = sum([int(n) for n in re.findall(padroes["semana"], tempo)])
meses = sum([int(n) for n in re.findall(padroes["mes"], tempo)])
anos = sum([int(n) for n in re.findall(padroes["ano"], tempo)])


total_dias += dias + (semanas * 7)
total_meses += meses + (anos * 12)

# Calcular o investimento com base no tempo
if total_dias + (total_meses * 30) <= 30:
    total_dias += total_meses * 30  # converte meses para dias
    saldo_final = calcular_investimento_diario(salario_convertido, total_dias)
    investimento_tipo = "diário"
    tempo_exibicao = f"{dias} dia(s), {semanas} semana(s), {meses} mês(es), {anos} ano(s) → Total: {total_dias} dias"
else:
    total_meses += total_dias // 30
    saldo_final = calcular_investimento_mensal(salario_convertido, total_meses)
    investimento_tipo = "mensal"
    tempo_exibicao = f"{dias} dia(s), {semanas} semana(s), {meses} mês(es), {anos} ano(s) → Total: {total_meses} mês(es)"

# Limpar a tela antes de mostrar o resumo
limpar_tela()

# Exibindo o saldo final
print(f"\n{Fore.CYAN}Estimativa de saldo final para {tempo_exibicao} de investimento com {investimento_tipo} de rendimento:{Fore.RESET}\n")

# Exibir a tabela de dados do cliente
dados_cliente = [
    [f"{Fore.CYAN}{nome_cliente}{Fore.RESET}", f"{Fore.CYAN}{cpf_formatado}{Fore.RESET}",
     f"{Fore.GREEN}{anos} anos e {meses} meses{Fore.RESET}",
     f"{simbolo_moeda} {saldo_final:.2f}{Fore.RESET}"]
]

# Exibir a tabela de dados do cliente
exibir_tabela(dados_cliente, ["Nome", "CPF", "Tempo de Investimento", f"Total Final ({simbolo_moeda})"])

# Loop principal
while True:
    voltar = input(f"\n{Fore.YELLOW}Pressione Enter para voltar ao início ou digite 'sair' para encerrar: {Fore.RESET}").strip().lower()
    if voltar == "sair":
        print(f"{Fore.GREEN}Obrigado por usar o Banco GTX! Até logo.{Fore.RESET}")
        break
    else:
        limpar_tela()
        exibir_titulo()
        nome_cliente = input(f"{Fore.BLUE}Digite seu nome completo: {Fore.RESET}")
