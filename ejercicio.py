class ListaUnidimensional:
    def __init__(self, elementos):
        self.elementos = elementos

    def mostrar(self):
        print(self.elementos)

    def acceder_elemento(self, posicion):
        return self.elementos[posicion]

    def insertar(self, valor, posicion):
        self.elementos.insert(posicion, valor)

    def eliminar(self, posicion):
        if 0 <= posicion < len(self.elementos):
            self.elementos.pop(posicion)

    def buscar(self, valor):
        if valor in self.elementos:
            return self.elementos.index(valor)
        else:
            return -1


class MatrizBidimensional:
    def __init__(self, datos):
        self.datos = datos

    def mostrar(self):
        for fila in self.datos:
            print(fila)

    def acceder_elemento(self, fila, columna):
        return self.datos[fila][columna]

    def insertar(self, fila, columna, valor):
        self.datos[fila][columna] = valor

    def eliminar(self, fila, columna):
        self.datos[fila][columna] = None  # o cualquier valor que indique "eliminado"

    def buscar(self, valor):
        for i, fila in enumerate(self.datos):
            if valor in fila:
                return (i, fila.index(valor))
        return (-1, -1)


# --------- Uso ---------

# 1a. Lista unidimensional tamaño 5
lista = ListaUnidimensional(["dato1", "dato2", "dato3", "dato4", "dato5"])

# 1b. Lista bidimensional 3x3
matriz = MatrizBidimensional([
    ["a1", "a2", "a3"],
    ["b1", "b2", "b3"],
    ["c1", "c2", "c3"]
])

# Mostrar listas iniciales
print("Lista unidimensional inicial:")
lista.mostrar()
print("\nMatriz bidimensional inicial:")
matriz.mostrar()

# 2a. Acceder e imprimir segundo elemento lista unidimensional
print("\nSegundo elemento lista unidimensional:", lista.acceder_elemento(1))

# 2b. Acceder e imprimir elemento segunda fila y segunda columna matriz
print("Elemento segunda fila y segunda columna matriz:", matriz.acceder_elemento(1, 1))

# 3a. Insertar "Estructura de datos" en posición 3 lista unidimensional
lista.insertar("Estructura de datos", 3)
print("\nLista unidimensional después de insertar:")
lista.mostrar()

# 3b. Eliminar elemento de tercera fila y tercera columna matriz (índices 2, 2)
matriz.eliminar(2, 2)
print("\nMatriz después de eliminar elemento (2,2):")
matriz.mostrar()

# 4a. Buscar "Estructura de datos" en lista unidimensional y devolver índice
indice = lista.buscar("Estructura de datos")
print("\nÍndice de 'Estructura de datos' en lista unidimensional:", indice)

# 4b. Buscar valor que prefieras en matriz (ejemplo "b2") y devolver índice (fila, columna)
fila, columna = matriz.buscar("b2")
print("Posición de 'b2' en matriz bidimensional: fila =", fila, ", columna =", columna)


    
    