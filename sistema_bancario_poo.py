from abc import ABC, abstractmethod
import re
from time import sleep
from datetime import datetime


class Cliente:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf
        
    def __str__(self):
        return f"Nome: {self.nome} CPF: {self.cpf}"
    

class ClientesCadastrados:
    def __init__(self):
        self.clientes = []
        self.contas_ativas = ContasAtivas()
    
    def cadastrar_cliente(self, cliente):
        self.clientes.append(cliente)
    
    def mostrar_clientes_cadastrados(self):
        for cliente in self.clientes:
            print(cliente)


class ContasAtivas:
    def __init__(self):
        self.contas = []
    
    def listar_contas(self):
        if len(self.contas) == 0:
            print("Nenhuma conta cadastrada.")
        for conta in self.contas:
            print(f"Nome: {conta.cliente.nome} CPF: {conta.cliente.cpf} - Numero da Conta: {conta.numero}")



class Historico:
    def __init__(self):
        self.transacoes = []
    
    def registrar_transacao(self, transacao):
        self.transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data":  datetime.now().strftime("%d/%m/%Y %A %H:%M")
        })
    
    def listar_transacoes(self):
        for transacao in self.transacoes:
            print(f"{transacao['tipo']:<20}  R${transacao['valor']:>8.2f} - {transacao['data']}")


class Conta:
    def __init__(self, cliente, numero):
        self.cliente = cliente
        self.numero = numero 
        self.agencia = "001"
        self.saldo = 0
        self.historico = Historico()
        self.saldo_poupanca = 0
    
    def deposito(self, valor):
        deposito = Deposito(valor)
        deposito.realizar_transacao(self)
    
    def saque(self, valor):
        saque = Saque(valor)
        saque.realizar_transacao(self)

    def deposito_poupanca(self, valor: float):
        if valor <= 0:
            print("Valor inválido.")
        elif valor > self.saldo:
            print("Saldo insuficiente.")
        else:
            poupanca = DepositoPoupanca(valor)
            poupanca.realizar_transacao_poupanca(self)
            return True
        return False
    
    def pix(self, valor, conta_recebedor):
        pix = PixEnviado(valor)
        pix.realizar_transacao_pix(self, conta_recebedor)
  
          
class Transacao(ABC):
    def __init__(self, valor):
        self.valor = valor
    
    @abstractmethod
    def realizar_transacao(self, conta):
        pass


class TransacaoPoupanca(ABC):
    def __init__(self, valor):
        self.valor = valor
    
    @abstractmethod
    def realizar_transacao_poupanca(self, conta):
        pass


class DepositoPoupanca(TransacaoPoupanca):
    def realizar_transacao_poupanca(self, conta):
        try:
            if self.valor <= 0:
                print("Valor inválido")
            elif self.valor > conta.saldo:
                print("Você não possui saldo suficiente.")
            else:
                conta.saldo -= self.valor
                conta.saldo_poupanca += self.valor
                conta.historico.registrar_transacao(self)
                return True
            return False
        except ValueError:
            print("Digite um valor válido.")
            

class ResgatePoupanca(TransacaoPoupanca):
    def realizar_transacao_poupanca(self, conta):
        if conta.saldo_poupanca == 0:
            print("Você não possui dinheiro na poupança.")
        elif self.valor <= 0:
            print("Valor inválido")
        elif self.valor > conta.saldo_poupanca:
            print("Saldo insuficiente")
        else:
            conta.saldo_poupanca -= self.valor
            conta.saldo += self.valor
            conta.historico.registrar_transacao(self)
            return True
        return False


class Deposito(Transacao):
    def realizar_transacao(self, conta):
        try:
            if self.valor <= 0:
                print("Valor inválido")
                return False
            else:
                conta.saldo += self.valor
                conta.historico.registrar_transacao(self)
                print(f"Deposito de R${self.valor:.2f} realizado")
            return True
        except TypeError:
            print("Digite apenas número")


class Saque(Transacao):
    def realizar_transacao(self, conta):
        if self.valor > conta.saldo:
            print("Saldo insuficiente.")
        elif self.valor <= 0:
            print("Valor inválido.")
        else:
            conta.saldo -= self.valor
            conta.historico.registrar_transacao(self)
            print(f"Saque de R${self.valor:.2f} realizado")
            return True
        return False


class TransacaoPix(ABC):
    def __init__(self, valor):
        self.valor = valor 
    
    @abstractmethod
    def realizar_transacao_pix(self, conta):
        pass


class PixEnviado(TransacaoPix):
    def realizar_transacao_pix(self, conta, conta_recebedor):
        if self.valor > conta.saldo:
            print("Saldo insuficiente.")
        elif self.valor <= 0:
            print("Valor inválido")
        else:
            conta.saldo -= self.valor
            conta_recebedor.saldo += self.valor
            conta.historico.registrar_transacao(self)
            conta_recebedor.historico.transacoes.append({
                "tipo": "Pix recebido",
                "valor": self.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M")
            })


class Investimento:
    def __init__(self, conta):
        self.investimentos = []
        self.conta = conta

    def cdb(self, valor: float):
        if valor <= 0:
            print("Valor inválido.")
        elif valor > self.conta.saldo:
            print("Você não possui saldo suficiente.")
        else:
            self.conta.saldo -= valor
            self.conta.saldo_investimento += valor
            self.conta.historico.registrar_transacao({
                "tipi": "Investimento CDB",
                "valor": self.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M")
            })
            return True
        return False
    

def cadastrar_cliente(clientes_cadastrados):
    cpf = input("CPF: ")
    filtrar_cpf = [cliente for cliente in clientes_cadastrado.clientes if cliente.cpf == cpf]
    if len(filtrar_cpf) == 1:
        print("Cliente já cadastrado.")
        return False
    
    if not re.fullmatch(r"\d+", cpf):
        print("CPF inválido.")
        return False
    
    
    nome = input("Nome: ")
    if not re.fullmatch(r"[A-Za-z]+(?:\s+[A-Za-z]+)+", nome):
        print("Nome inválido.")
        return False
    
    cliente = Cliente(nome, cpf)
    clientes_cadastrados.cadastrar_cliente(cliente)
    return cliente


def cadastrar_conta(clientes_cadastrados, contas_ativas):
    numero = ""
    cpf = input("CPF: ")
    filtrar_cpf = [cliente for cliente in clientes_cadastrado.clientes if cliente.cpf == cpf]
    conta_cadastrada = [conta for conta in contas_ativas.contas if conta.cliente.cpf == cpf]
    
    if len(filtrar_cpf) == 0:
        print("Cliente não encontrado.")
        return False
     
    if len(conta_cadastrada) == 1:
        print("Conta já cadastrada.")
        return False

    for cliente in clientes_cadastrados.clientes:
        if cpf == cliente.cpf:
            if len(contas_ativas.contas) == 0:
                numero = "1"
                conta = Conta(cliente, numero)
                contas_ativas.contas.append(conta)
            else:
                numero = len(contas_ativas.contas) + 1
                conta = Conta(cliente, numero)
                contas_ativas.contas.append(conta)
    return conta


def enviar_pix(conta_rementente, contas_ativas):
    cpf_recebedor = input("CPF do destinatário: ")
    for conta in contas_ativas.contas:
        if conta.cliente.cpf == cpf_recebedor:
            try:
                valor = float(input("R$"))
            except ValueError:
                print("Valor inválido.")
            conta_rementente.pix(valor, conta)


def acessar_conta(contas_ativas):
    cpf = input("CPF: ")
    for conta in contas_ativas.contas:
        if cpf == conta.cliente.cpf:
            while True:
                mensagem = f"Bem vindo {conta.cliente.nome}"
                print(mensagem.center(60, "="))
                print("1- Saldo\n2- Deposito\n3- Saque\n4- Pix\n5- Extrato\n6- Sair")
                print("=" * 60)
                opcao = input("Opcão: ")

                if opcao == "1":
                    print("=" * 60)
                    print(f"R${conta.saldo:.2f}")
                    print("=" * 60)
                    sleep(1)
                elif opcao == "2":
                    print("=" * 60)
                    valor = float(input("R$ "))
                    conta.deposito(valor)
                    sleep(1)
                elif opcao == "3":
                    valor = float(input("R$ "))
                    conta.saque(valor)
                    sleep(1)
                elif opcao == "4":
                    enviar_pix(conta, contas_ativas)
                    sleep(1)
                elif opcao == "5":
                    mensagem2 = "Extrato"
                    print(mensagem2.center(60, "="))
                    conta.historico.listar_transacoes()
                    print("=" * 60)
                    sleep(1)
                elif opcao == "6":
                    print("Saindo...")
                    sleep(1)
                    break
                else:
                    print("Opção inválida.")


clientes_cadastrado = ClientesCadastrados()
contas_ativas = ContasAtivas()   

  
def main():
    while True:
        sleep(1)
        mensagem = " Bem-Vindo ao N&M Bank "
        print(mensagem.center(60, "="))
        print("1- Cadastrar\n2- Criar conta\n3- Acessar conta\n4- Listar Contas\n5- Fechar programa")
        print("=" * 60)
        opcao = input("Opção: ")

        if opcao == "1":
            cliente = cadastrar_cliente(clientes_cadastrado)
            sleep(1)
        elif opcao == "2":
            conta = cadastrar_conta(clientes_cadastrado, contas_ativas)
            sleep(1)
        elif opcao == "3":
            acessar_conta(contas_ativas)
            sleep(1)
        elif opcao == "4":
            contas_ativas.listar_contas()
        elif opcao == "5":
            print("Encerrando programa...")
            sleep(1)
            break


main()