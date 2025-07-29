import math

class Calculadora:
    
    @staticmethod
    # Función que suma dos números
    def sumar(a : int|float, b : int|float) -> int|float:
        if(isinstance(a,(int,float)) and isinstance(b,(int,float)) ):
            return a + b
        else:
            raise ValueError("Debe ingresar valores numéricos enteros o flotantes.")

    @staticmethod
    # Función que resta dos números
    def restar(a : int|float, b : int|float) -> int|float:
        if(isinstance(a,(int,float)) and isinstance(b,(int,float))):
            return a - b
        else:
            raise ValueError("Debe ingresar valores numéricos enteros o flotantes.")

    @staticmethod
    # Función que multiplica dos números
    def multiplicar(a : int|float, b : int|float) -> int|float:
        if(isinstance(a,(int,float)) and isinstance(b,(int,float)) ):
            return a * b
        else:
            raise ValueError("Debe ingresar valores numéricos enteros o flotantes.")

    @staticmethod
    # Función que divide dos números
    def dividir(a : int|float, b : int|float) -> int|float:
        if(isinstance(a,(int,float)) and isinstance(b,(int,float))):
            if b == 0:
                raise ValueError("No se puede dividir entre 0")
            return a / b
        else:
            raise ValueError("Debe ingresar valores numéricos enteros o flotantes.")
        
    @staticmethod
     # Función que divide dos números
    def exponenciar(a : int|float, b : int|float) -> int|float:
        if(isinstance(a,(int,float)) and isinstance(b,(int,float))):
            return math.pow(a,b)
        else:
            raise ValueError("Debe ingresar valores numéricos enteros o flotantes.")
        
    @staticmethod
     # Función que divide dos números
    def obtener_raiz(a : int|float, b : int|float) -> int|float:
        if(isinstance(a,(int,float)) and isinstance(b,(int,float))):
            return round(math.pow(a,1/b),4)
        else:
            raise ValueError("Debe ingresar valores numéricos enteros o flotantes.")
        
