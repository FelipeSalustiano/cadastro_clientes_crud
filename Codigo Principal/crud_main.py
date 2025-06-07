import datetime
import pandas as pd


usuarios = {}
locais = {}

def menu_principal():
    while True:
        print("\n--- MENU PRINCIPAL ---")
        print("1. Gerenciar Usuários")
        print("2. Gerenciar Locais para Fazendas Verticais")
        print("3. Sair")
        escolha = input("Escolha uma opção: ")
        if escolha == '1':
            menu_usuarios()
        elif escolha == '2':
            menu_locais()
        elif escolha == '3':
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

def menu_usuarios():
    while True:
        print("\n--- MENU USUÁRIOS ---")
        print("1. Adicionar Usuário")
        print("2. Listar Usuários")
        print("3. Atualizar Usuário")
        print("4. Remover Usuário")
        print("5. Voltar")
        escolha = input("Escolha uma opção: ")
        if escolha == '1':
            adicionar_usuario()
        elif escolha == '2':
            listar_usuarios()
        elif escolha == '3':
            atualizar_usuario()
        elif escolha == '4':
            remover_usuario()
        elif escolha == '5':
            break
        else:
            print("Opção inválida.")

def adicionar_usuario():
    nome = input("Nome: ")
    idade = int(input("Idade: "))
    endereco = input("Endereço: ")
    pessoas_casa = int(input("Pessoas morando na mesma casa: "))
    renda = float(input("Renda familiar: "))
    profissao = input("Profissão: ")

    usuario = {
        "nome": nome,
        "idade": idade,
        "endereco": endereco,
        "pessoas_casa": pessoas_casa,
        "renda": renda,
        "profissao": profissao,
        "apto": verificar_aptidao_usuario(idade, renda),
        "local_designado": endereco if verificar_aptidao_usuario(idade, renda) else "N/A",
        "prazo_comparecimento": (datetime.date.today() + datetime.timedelta(days=15)).isoformat() if verificar_aptidao_usuario(idade, renda) else "N/A"
    }

    usuarios[nome] = usuario
    print("Usuário adicionado com sucesso!")

def listar_usuarios():
    if not usuarios:
        print("\nNenhum usuário cadastrado.")
        return

    df = pd.DataFrame(usuarios.values())
    print("\n--- USUÁRIOS CADASTRADOS ---")
    print(df.to_string(index=False))


def atualizar_usuario():
    nome = input("Digite o nome do usuário a atualizar: ")
    if nome in usuarios:
        print("Deixe em branco para manter o valor atual.")
        idade = input(f"Nova idade (atual: {usuarios[nome]['idade']}): ")
        if idade: usuarios[nome]['idade'] = int(idade)
        renda = input(f"Nova renda (atual: {usuarios[nome]['renda']}): ")
        if renda: usuarios[nome]['renda'] = float(renda)

        
        usuarios[nome]['apto'] = verificar_aptidao_usuario(usuarios[nome]['idade'], usuarios[nome]['renda'])
        usuarios[nome]['local_designado'] = usuarios[nome]['endereco'] if usuarios[nome]['apto'] else "N/A"
        usuarios[nome]['prazo_comparecimento'] = (datetime.date.today() + datetime.timedelta(days=30)).isoformat() if usuarios[nome]['apto'] else "N/A"
        print("Usuário atualizado.")
    else:
        print("Usuário não encontrado.")

def remover_usuario():
    nome = input("Digite o nome do usuário a remover: ")
    if usuarios.pop(nome, None):
        print("Usuário removido.")
    else:
        print("Usuário não encontrado.")

def verificar_aptidao_usuario(idade, renda):
    return idade >= 18 and renda <= 2000  

def menu_locais():
    while True:
        print("\n--- MENU LOCAIS ---")
        print("1. Adicionar Local")
        print("2. Listar Locais")
        print("3. Atualizar Local")
        print("4. Remover Local")
        print("5. Voltar")
        escolha = input("Escolha uma opção: ")
        if escolha == '1':
            adicionar_local()
        elif escolha == '2':
            listar_locais()
        elif escolha == '3':
            atualizar_local()
        elif escolha == '4':
            remover_local()
        elif escolha == '5':
            break
        else:
            print("Opção inválida.")

def adicionar_local():
    nome_local = input("Nome do local: ")
    endereco = input("Endereço: ")
    responsavel = input("Nome do responsável: ")
    contato = input("Contato do responsável: ")
    andares = int(input("Quantidade de andares: "))
    area = float(input("Área do local (m²): "))

    capacidade = calcular_capacidade_producao(andares, area)
    apto = "Sim" if capacidade >= 1000 else "Não"

    local = {
        "nome_local": nome_local,
        "endereco": endereco,
        "responsavel": responsavel,
        "contato": contato,
        "andares": andares,
        "area": area,
        "capacidade_producao": capacidade,
        "apto": apto,
        "mensagem": "O responsável será contatado para mais informações."
    }

    locais[nome_local] = local
    print("Local adicionado com sucesso!")

def listar_locais():
    if not locais:
        print("\nNenhum local cadastrado.")
        return

    df = pd.DataFrame(locais.values())
    print("\n--- LOCAIS CADASTRADOS ---")
    print(df.to_string(index=False))


def atualizar_local():
    nome = input("Digite o nome do local a atualizar: ")
    if nome in locais:
        print("Deixe em branco para manter o valor atual.")
        andares = input(f"Novos andares (atual: {locais[nome]['andares']}): ")
        area = input(f"Nova área (atual: {locais[nome]['area']}): ")
        if andares: locais[nome]['andares'] = int(andares)
        if area: locais[nome]['area'] = float(area)
        capacidade = calcular_capacidade_producao(locais[nome]['andares'], locais[nome]['area'])
        locais[nome]['capacidade_producao'] = capacidade
        locais[nome]['apto'] = "Sim" if capacidade >= 1000 else "Não"
        print("Local atualizado.")
    else:
        print("Local não encontrado.")

def remover_local():
    nome = input("Digite o nome do local a remover: ")
    if locais.pop(nome, None):
        print("Local removido.")
    else:
        print("Local não encontrado.")

def calcular_capacidade_producao(andares, area):
    return andares * area * 2  


menu_principal()