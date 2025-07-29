from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime

class Conta:
    def __init__(self, cliente, numero):
        self._saldo: float = 0
        self._cliente: Cliente = cliente
        self._numero: int = numero
        self._agencia: str = "0001"
        self._historico: Historico = Historico()
        self.limite_valor: int = 0
        self.limite_saques: int = 0
        self.saques: int = 0

    @classmethod
    def nova_conta(cls, cliente, numero: int):  # original: def nova_conta(cls, cliente: Cliente, numero: int) -> Conta:
        return cls(cliente, numero)

    @property
    def saldo(self) -> float:
        saldo = self._saldo
        return saldo

    @property
    def numero(self) -> float:
        numero = self._numero
        return numero

    @property
    def agencia(self) -> str:
        agencia = self._agencia
        return agencia

    @property
    def cliente(self):  # Orginal: -> Cliente
        cliente = self._cliente
        return cliente

    @property
    def historico(self):  # -> Historico
        return self._historico

    def puxar_extrato(self):
        texto_extrato = ("-" * 50 + "\n" + "Extrato:")
        for i in self._historico.extrato:
            texto_extrato += ("\n" + i)
        texto_extrato += ("\n" + "-" * 50)
        return texto_extrato

    def sacar(self, valor: float) -> bool:
        if valor > self.saldo:
            return False
        elif valor > self.limite_valor:
            return False
        elif self.saques >= self.limite_saques:
            return False
        elif self._saldo >= valor:
            self._saldo -= valor
            print("Saques da conta:", self.saques, "Limete para saques da conta:", self.limite_saques)
            self.saques += 1
            print("Saques da conta:", self.saques, "Limete para saques da conta:", self.limite_saques)
            return True
        else:
            return False

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self._saldo += valor
            return True
        else:
            return False

    def __str__(self):
        return f"uma isntancia de Conta"


class ContaCorrente(Conta):
    def __init__(self, cliente, numero):
        super().__init__(cliente, numero)
        self.limite_valor: float = 500.00
        self.limite_saques: int = 3

    def __str__(self):
        return f"""
        Agência:\t {self.agencia}
        C/C:    \t {self.numero}
        Titular:\t {self.cliente.nome}
        """


class ContaBlack(Conta):
    def __init__(self, cliente, numero):
        super().__init__(cliente, numero)
        self.limite_valor: float = 5000.00
        self.limite_saques: int = 16

    def __str__(self):
        return f"""
        Agência:\t {self.agencia}
        C/Black:\t {self.numero}
        Titular:\t {self.cliente.nome}
        """


class TransacaoInterface(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta: Conta):
        pass


class Deposito(TransacaoInterface):
    def __init__(self, valor: float):
        self._valor: float = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta: Conta):
        deu_certo = conta.depositar(self.valor)
        if deu_certo:
            conta.historico.adicionar_transacao(self)
            print(f"deu tudo certo com o deposito de R$ {self.valor}")
        else:
            print("deu ruim :(")


class Saque(TransacaoInterface):
    def __init__(self, valor: float):
        self._valor: float = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta: Conta):
        deu_certo = conta.sacar(self.valor)
        if deu_certo:
            conta.historico.adicionar_transacao(self)
            print(f"deu tudo certo com o saque de R$ {self.valor}")
        else:
            print("deu ruim :(")


class Historico:
    def __init__(self):
        self._extrato = []

    @property
    def extrato(self):
        return self._extrato

    def adicionar_transacao(self, transacao: TransacaoInterface):
        texto_extrato = f"{transacao.__class__.__name__} de R$ {float(transacao.valor)} às {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        self.extrato.append(texto_extrato)


class Cliente:
    def __init__(self, endereco):
        self.endereco: str = endereco
        self.contas: list = []
        self._cpf = 123456789  # teste

    def realizar_transacao(self, conta: Conta, transacao: TransacaoInterface):  # transacao: TransacaoInterface):
        transacao.registrar(conta)

    def adicionar_conta(self, tipo_conta: type(Conta) = ContaCorrente):
        numeros_de_contas = len(self.contas)
        numero_da_conta = numeros_de_contas + 1
        #nova_conta = Conta.nova_conta(self, numero_da_conta)
        nova_conta = tipo_conta.nova_conta(self, numero_da_conta)
        self.contas.append(nova_conta)

    def __str__(self):
        return f"""
        Uma instancia de Cliente nesse endereço: {self.endereco}; 
        Com essas contas: {(conta for conta in self.contas)}."""


class PessoaFisica(Cliente):

    def __init__(self, endereco, nome, cpf, data_nascimento):
        super().__init__(endereco)
        self.nome: str = nome
        self.__cpf: str = cpf
        self.data_nascimento: str = data_nascimento


def run():

    cliente_1 = PessoaFisica("Rua Lopca", "Nome", "123456789-10", "01/01/0001")
    cliente_1.adicionar_conta()
    #print(cliente_1.contas[0])
    conta1_do_cliente_1 = cliente_1.contas[0]
    deposito_10_reais = Deposito(10)

    saque_15_reais = Saque(15)
    saque_2_reais = Saque(2)
    saque_1_reais = Saque(1)

    cliente_1.realizar_transacao(conta1_do_cliente_1, deposito_10_reais)
    cliente_1.realizar_transacao(conta1_do_cliente_1, saque_15_reais)
    cliente_1.realizar_transacao(conta1_do_cliente_1, deposito_10_reais)
    cliente_1.realizar_transacao(conta1_do_cliente_1, saque_15_reais)
    cliente_1.realizar_transacao(conta1_do_cliente_1, saque_1_reais)
    cliente_1.realizar_transacao(conta1_do_cliente_1, saque_2_reais)
    cliente_1.realizar_transacao(conta1_do_cliente_1, saque_2_reais)

    print("Extrato:", conta1_do_cliente_1.historico.extrato)
    print("saldo: R$", conta1_do_cliente_1.saldo)
    print("limite para saque:", conta1_do_cliente_1.limite_valor)
    print("limite para saques:", conta1_do_cliente_1.limite_saques)

    print("-" * 50)

    cliente_2 = PessoaFisica("Rua escorere la vai 1", "Paul", "987654321-00", "00/00/200")
    cliente_2.adicionar_conta()
    conta1_do_cliente_2 = cliente_2.contas[0]
    print("Saldo: R$", conta1_do_cliente_2.saldo)
    cliente_2.realizar_transacao(conta1_do_cliente_2, Saque(20))
    cliente_2.realizar_transacao(conta1_do_cliente_2, Deposito(40))
    cliente_2.realizar_transacao(conta1_do_cliente_2, Saque(20))
    print("Saldo: R$", conta1_do_cliente_2.saldo)
    cliente_2.adicionar_conta(ContaBlack)
    conta2_do_cliente_2 = cliente_2.contas[1]
    print("Saldo: R$", conta2_do_cliente_2.saldo)
    cliente_2.realizar_transacao(conta2_do_cliente_2, Deposito(8000))
    cliente_2.realizar_transacao(conta2_do_cliente_2, Saque(2000))
    cliente_2.realizar_transacao(conta2_do_cliente_2, Saque(1000))
    print("Saldo: R$", conta2_do_cliente_2.saldo)
    print(conta1_do_cliente_1.puxar_extrato())
    print(conta1_do_cliente_2)
    print(conta2_do_cliente_2)


def teste(texto):
    return texto
