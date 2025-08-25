import allure

# -------------------------------
# Opción 1: Mensaje en el assert
# -------------------------------
def test_suma_ok():
    assert 1 + 1 == 2, "La suma básica debería dar 2"


def test_suma_fail():
    esperado = 5
    resultado = 2 + 2
    assert resultado == esperado, f"Error en suma: esperado {esperado}, pero obtuve {resultado}"


# -------------------------------
# Opción 2: Attach para más detalles
# -------------------------------
def test_resta_ok():
    a, b = 10, 5
    allure.attach(f"Valores: a={a}, b={b}", name="Datos de entrada", attachment_type=allure.attachment_type.TEXT)
    resultado = a - b
    allure.attach(str(resultado), name="Resultado calculado", attachment_type=allure.attachment_type.TEXT)
    assert resultado == 5, "La resta debería dar 5"


def test_resta_fail():
    a, b = 10, 5
    resultado = a - b
    allure.attach(f"Esperado=37, obtenido={resultado}", name="Comparación", attachment_type=allure.attachment_type.TEXT)
    assert resultado == 37, f"Error en resta: esperaba 37, obtuve {resultado}"


# -------------------------------
# Opción 3: Pasos con allure.step
# -------------------------------
def test_multiplicacion():
    a, b = 3, 4

    with allure.step("Multiplicando los valores"):
        resultado = a * b
        allure.attach(str(resultado), name="Resultado parcial", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Verificando el resultado"):
        esperado = 15
        assert resultado == esperado, f"Multiplicación incorrecta: {a}*{b} debería ser {esperado}, pero fue {resultado}"

def test_demo():
    with allure.step("Calcular suma"):
        resultado = 1 + 1
        allure.attach(str(resultado), "Resultado", allure.attachment_type.TEXT)
        assert resultado == 2, "La suma debería dar 2"

def test_demo_error():
    with allure.step("Prueba"):
        resultado = 10 + 10
        allure.attach(str(resultado), "Resultado", allure.attachment_type.TEXT)
        assert resultado == 2, "La suma debería dar 2"

def test_demo_otro():
    with allure.step("Prueba2"):
        resultado = 2 + 2
        allure.attach(str(resultado), "Resultado", allure.attachment_type.TEXT)
        assert resultado == 4, "La suma debería dar 4"