"""Números a palabras en español (0 .. 999.999.999) sin dependencias."""
_U = ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez",
      "once", "doce", "trece", "catorce", "quince", "dieciséis", "diecisiete", "dieciocho", "diecinueve",
      "veinte", "veintiuno", "veintidós", "veintitrés", "veinticuatro", "veinticinco", "veintiséis",
      "veintisiete", "veintiocho", "veintinueve"]
_D = {30: "treinta", 40: "cuarenta", 50: "cincuenta", 60: "sesenta", 70: "setenta", 80: "ochenta", 90: "noventa"}
_C = {100: "ciento", 200: "doscientos", 300: "trescientos", 400: "cuatrocientos", 500: "quinientos",
      600: "seiscientos", 700: "setecientos", 800: "ochocientos", 900: "novecientos"}


def _lt1000(n: int) -> str:
    if n < 30:
        return _U[n]
    if n < 100:
        d, u = divmod(n, 10)
        return _D[d * 10] + (f" y {_U[u]}" if u else "")
    if n == 100:
        return "cien"
    c, r = divmod(n, 100)
    return _C[c * 100] + (f" {_lt1000(r)}" if r else "")


def to_words(n: int) -> str:
    if n < 0:
        return "menos " + to_words(-n)
    if n < 1000:
        return _lt1000(n)
    if n < 1_000_000:
        m, r = divmod(n, 1000)
        head = "mil" if m == 1 else _lt1000(m).replace("uno", "un") + " mil"
        return head + (f" {_lt1000(r)}" if r else "")
    m, r = divmod(n, 1_000_000)
    head = "un millón" if m == 1 else to_words(m).replace("uno", "un") + " millones"
    return head + (f" {to_words(r)}" if r else "")
