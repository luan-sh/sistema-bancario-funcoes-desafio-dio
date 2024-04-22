import datetime

def menu():
    menu = """

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nu] Cadastrar usuário
    [nc] Nova conta
    [lc] Listar contas
    [q] Sair

    => """
    
    return input(menu)

def depositar(saldo, valor, extrato, documento, /):
    if valor > 0:
        saldo += valor
        extrato.append({
            "documento": documento,
            "operacao": f"Depósito: R$ {valor:.2f}\n",
            "data": datetime.datetime.now()
        })

        documento += 1

        print(f"Depósito realizado com sucesso no valor de {valor:.2f}")
    else:
        print("Operação falhou!\nO valor informado é inválido.")

    return saldo, extrato, documento

def sacar(*, saldo, valor, extrato, limite, documento, numero_saques, limite_saques):
    excedeu_saldo   = valor > saldo
    excedeu_limite  = valor > limite
    excedeu_saques  = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou!\nVocê não tem saldo suficiente.")

    elif excedeu_limite:
        print("Operação falhou!\nO valor do saque excede o limite.")

    elif excedeu_saques:
        print("Operação falhou!\nNúmero máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato.append({
                "documento": documento,
                "operacao": f"Saque: R$ {valor:.2f}\n",
                "data": datetime.datetime.now()
        })

        documento       += 1
        numero_saques   += 1

        print(f"Saque realizado com sucesso no valor de R$ {valor:.2f}")

    else:
        print("Operação falhou!\nO valor informado é inválido.")

    return saldo, extrato, documento

def exibir_extrato(saldo, /, *, extrato):
    if len(extrato) > 0:
        print("\n============================= EXTRATO =============================")
        print("Documento " + ( " "*( len(str(extrato[-1]["documento"]))-10) )  + "| Data       | Hora     | Operação\n")

        for i in range(len(extrato)):
            print(
                    str(extrato[i]["documento"]) + " "*(10-len(str(extrato[i]["documento"]))) + "| " 
                    + extrato[i]["data"].strftime("%d/%m/%Y") + " | " 
                    + extrato[i]["data"].strftime("%X") + " | " 
                    + extrato[i]["operacao"]
                )
        
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("===================================================================")
    else:
        print("Não foram realizadas movimentações.")

def criar_usuario(usuarios):
    cpf     = input("Informe o CPF (somente números): ")
    usuario = buscar_usuario(cpf, usuarios)

    if usuario:
        print("Já existe um usuário com o CPF informado!")
        return

    nome            = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco        = input("Informe o endereço (logradouro, número, bairro, cidade, estado): ")

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "endereco": endereco,
        "cpf": cpf

    })

    print("Usuário cadastrado com sucesso!")

def buscar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf     = input("Informe o CPF do usuário: ")
    usuario = buscar_usuario(cpf, usuarios)

    if usuario:
        print("Conta criada com sucesso!")
        
        return {
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario
        }

    print("Usuário não encontrado!\nFalha na tentativa de criação de conta.")

def listar_contas(contas):
    for conta in contas:
        linha = f"""
        Agência: {conta["agencia"]}
        C/C: {conta["numero_conta"]}
        Titular: {conta["usuario"]["nome"]}
        """
        print("="*100)
        print(linha)


def main():
    saldo           = 0
    limite          = 500
    numero_saques   = 0
    documento       = 1
    extrato         = []
    usuarios        = []
    contas          = []

    LIMITE_SAQUES   = 3
    AGENCIA         = "0001"

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float( input("Informe o valor do depósito: ") )

            saldo, extrato, documento = depositar(saldo, valor, extrato, documento)

        elif opcao == "s":
            valor = float( input("Informe o valor do saque: ") )

            saldo, extrato, documento = sacar(
                saldo           = saldo,
                valor           = valor,
                extrato         = extrato,
                limite          = limite,
                documento       = documento,
                numero_saques   = numero_saques,
                limite_saques   = LIMITE_SAQUES
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta    = len(contas) + 1
            conta           = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("Volte sempre!")
            break
        else:
            print("Operação inválida!\nPor favor, selecione novamente a operação desejada.")

main()
