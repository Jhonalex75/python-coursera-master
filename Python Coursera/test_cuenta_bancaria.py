import pytest
from cuenta_bancaria import calculate_discount, CuentaBancaria

# Tests para calculate_discount
@pytest.mark.parametrize(
    "price, percentage, expected",
    [
        (100, 10, 90),
        (200, 25, 150),
        (50, 0, 50),
        (80, 100, 0),
        (0, 50, 0),
        (100, 0, 100),
    ]
)
def test_calculate_discount(price, percentage, expected):
    assert calculate_discount(price, percentage) == expected

def test_negative_percentage():
    with pytest.raises(ValueError):
        calculate_discount(100, -10)

# Fixture para cuentas bancarias
@pytest.fixture
def cuentas():
    origen = CuentaBancaria("Juan", 200)
    destino = CuentaBancaria("Ana", 100)
    return origen, destino

def test_transferencia_exitosa(cuentas):
    origen, destino = cuentas
    origen.transferir(destino, 50)
    assert origen.obtener_saldo() == 150
    assert destino.obtener_saldo() == 150

def test_transferencia_fondos_insuficientes(cuentas):
    origen, destino = cuentas
    with pytest.raises(ValueError, match="Fondos insuficientes"):
        origen.transferir(destino, 500)

def test_transferencia_cantidad_no_valida(cuentas):
    origen, destino = cuentas
    with pytest.raises(ValueError, match="positiva"):
        origen.transferir(destino, -10) 