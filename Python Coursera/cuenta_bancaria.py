def calculate_discount(price, percentage):
    if percentage < 0:
        raise ValueError("El porcentaje no puede ser negativo")
    return price - (price * percentage / 100)

class CuentaBancaria:
    def __init__(self, titular, saldo=0):
        self.titular = titular
        self.saldo = saldo

    def depositar(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad a depositar debe ser positiva")
        self.saldo += cantidad

    def retirar(self, cantidad):
        if cantidad > self.saldo:
            raise ValueError("Fondos insuficientes")
        self.saldo -= cantidad

    def transferir(self, destino, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad a transferir debe ser positiva")
        self.retirar(cantidad)
        destino.depositar(cantidad)

    def obtener_saldo(self):
        return self.saldo 