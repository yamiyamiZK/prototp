import os
from tabulate import tabulate
from colorama import Fore, init

# Inicializa o colorama
init(autoreset=True)

# Função para calcular o salário líquido
def calcular_salario_liquido(salario_bruto):
    desconto = salario_bruto * 0.20
    salario_liquido = salario_bruto - desconto
    return salario_liquido

# Função para converter para dólares
def converter_para_dolar(salario_liquido, cotacao_dolar):
    return salario_liquido / cotacao_dolar

# Função para calcular o investimento com base em 10% de rendimento mensal
def calcular_investimento(salario_liquido, meses):
    saldo_final = salario_liquido * (1 + 0.10)**meses
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
 |  _ )  /  \  |  \  | |/  ____)/  _  \\
 |  _ \ / -- \ |  _\ | || /    |  | | |
 | |_) ) ____ \|  | \| || \____|  |_| |
 |____/_/    \_|__|  |_|\______)\_____/ 
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
salario_bruto = float(input("Digite o valor do seu salário bruto (R$): "))

# Calcular o salário líquido
salario_liquido = calcular_salario_liquido(salario_bruto)

# Exibir o salário líquido
print(f"\n{Fore.GREEN}Salário líquido: R${salario_liquido:.2f}{Fore.RESET}\n")

# Perguntar se quer converter para dólares
converter = input(f"{Fore.YELLOW}Você gostaria de converter seu salário para dólares (R$6.18)? (sim/não): {Fore.RESET}").strip().lower()
cotacao_dolar = 6.18 #supondo que seja esse valor

if converter == "sim":
    salario_em_dolar = converter_para_dolar(salario_liquido, cotacao_dolar)
    print(f"{Fore.GREEN}Seu salário em dólares: ${salario_em_dolar:.2f}{Fore.RESET}\n")

# Perguntar quanto tempo o usuário gostaria de investir
tempo = input(f"{Fore.YELLOW}Quanto tempo você gostaria de investir?: {Fore.RESET}").strip().lower()
print("Informe se são meses ou anos!")

# Identificar se é meses ou anos e converter para meses
if "mes" in tempo:
    meses = int(''.join(filter(str.isdigit, tempo)))
elif "ano" in tempo:
    anos = int(''.join(filter(str.isdigit, tempo)))
    meses = anos * 12
else:
    print(f"{Fore.RED}Entrada inválida. Por favor, insira 'meses' ou 'anos'.{Fore.RESET}")
    exit()

# Limpar a tela
limpar_tela()

# Calcular o saldo final após o investimento
saldo_final = calcular_investimento(salario_liquido, meses)

# Converter meses para anos e meses
anos, meses_restantes = converter_em_anos_meses(meses)

# Exibindo a estimativa de ganhos
print(f"\n{Fore.CYAN}Estimativa de saldo final após {anos} anos e {meses_restantes} meses de investimento com 10% de rendimento mensal:{Fore.RESET}\n")

# Criando a tabela de investimentos
tabela = []

for i in range(1, meses + 1):
    rendimento = salario_liquido * (0.10 * i)
    saldo_atual = salario_liquido * (1 + 0.10)**i
    tabela.append([i, f"{Fore.GREEN}{salario_liquido * i:.2f}{Fore.RESET}",
                   f"{Fore.GREEN}{rendimento:.2f}{Fore.RESET}",
                   f"{Fore.GREEN}{saldo_atual:.2f}{Fore.RESET}"])

# Exibindo o cabeçalho e a tabela
exibir_tabela(tabela, ["Mês", "Investido (R$)", "Rendimento Mensal (R$)", "Saldo Final (R$)"])

# Pedir para pressionar Enter para prosseguir
input(f"\n{Fore.YELLOW}Clique Enter para prosseguir...{Fore.RESET}")

# Limpar a tela
limpar_tela()

# Exibir os dados do cliente e o total final em uma tabela formatada
dados_cliente = [
    [f"{Fore.CYAN}{nome_cliente}{Fore.RESET}", f"{Fore.CYAN}{cpf_formatado}{Fore.RESET}",
     f"{Fore.GREEN}{anos} anos e {meses_restantes} meses{Fore.RESET}",
     f"{Fore.GREEN}R${saldo_final:.2f}{Fore.RESET}"]
]

# Exibir a tabela de dados do cliente
exibir_tabela(dados_cliente, ["Nome", "CPF", "Tempo de Investimento", "Total Final (R$)"])
