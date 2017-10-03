import sys

########################################
#Patron decorator
def mostrar_pelicula(peliculas):
    for pelicula in peliculas:
                print("{}. {}".format(pelicula.id, pelicula.nombre))

def p_decorator(func):
    def func_wrapper(param):
        return func(param)
    return func_wrapper
########################################

class Entrada:
    def __init__(self, pelicula_id, funcion, cantidad):
        self.pelicula_id = pelicula_id
        self.funcion = funcion
        self.cantidad = cantidad

class Pelicula:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        
########################################
class Cine:
    def __init__(self):
        #Patron Comporsite
        self.hijos =[]
    def listar_peliculas(self):
        pass
    def listar_funciones(self, pelicula_id):
        pass
    def guardar_entrada(self, id_pelicula_elegida, funcion_elegida, cantidad):
        pass
    def add_hijos(self, hijo):
        #Patron Comporsite
        self.hijos.append(hijo)
    def imprimir_cine(self):
        #Patron Comporsite
        for hijo in self.hijos:
            id, nombre = hijo.imprimir_cine()
            print(str(id) + ": " + nombre)
########################################
        
class CinePlaneta(Cine):
    ########################################
    #Patron Singleton
    instancia = None

    @classmethod
    def get_instance(cls):
        if cls.instancia == None:
            cls.instancia = CinePlaneta()
        return cls.instancia
    #########################################
    def __init__(self):
        peliculaIT = Pelicula(1, 'IT')
        peliculaHF = Pelicula(2, 'La Hora Final')
        peliculaD = Pelicula(3, 'Desparecido')
        peliculaDeep = Pelicula(4, 'Deep El Pulpo')

        peliculaIT.funciones = ['19:00', '20.30', '22:00']
        peliculaHF.funciones = ['21:00']
        peliculaD.funciones = ['20:00', '23:00']
        peliculaDeep.funciones = ['16:00']

        self.lista_peliculas = [peliculaIT, peliculaHF, peliculaD, peliculaDeep]
        self.entradas = []

    def listar_peliculas(self):
        return self.lista_peliculas

    def listar_funciones(self, pelicula_id):
        return self.lista_peliculas[int(pelicula_id) - 1].funciones

    def guardar_entrada(self, id_pelicula_elegida, funcion_elegida, cantidad):
        self.entradas.append(Entrada(id_pelicula_elegida, funcion_elegida, cantidad))
        return len(self.entradas)

    def imprimir_cine(self):
        #Comporsite
        return (1, "CinePlaneta")



class CineStark(Cine):
    ########################################
    #Patron Singleton
    instancia = None

    @classmethod
    def get_instance(cls):
        if cls.instancia == None:
            cls.instancia = CineStark()
        return cls.instancia
    #########################################
    def __init__(self):
        peliculaD = Pelicula(1, 'Desparecido')
        peliculaDeep = Pelicula(2, 'Deep El Pulpo')

        peliculaD.funciones = ['21:00', '23:00']
        peliculaDeep.funciones = ['16:00', '20:00']

        self.lista_peliculas = [peliculaD, peliculaDeep]
        self.entradas = []


    def listar_peliculas(self):
        return self.lista_peliculas

    def listar_funciones(self, pelicula_id):
        return self.lista_peliculas[int(pelicula_id) - 1].funciones

    def guardar_entrada(self, id_pelicula_elegida, funcion_elegida, cantidad):
        self.entradas.append(Entrada(id_pelicula_elegida, funcion_elegida, cantidad))
        return len(self.entradas)

    def imprimir_cine(self):
        #Comporsite
        return (2, "CineStark")



####################################################
#PATRON FACTORY METHOD
class CineFactory:
    def obtener_cines(self, tipo_cine):
        if tipo_cine == "1":
            #################################
            #Patron Singleton
            return CinePlaneta.get_instance()
        elif tipo_cine == "2":
            #################################
            #Patron Singleton
            return CineStark.get_instance()
        else:
            return None
####################################################


def main():
    cines = Cine()
    cineplaneta = CinePlaneta.get_instance()
    cinestark = CineStark.get_instance()
    cines.add_hijos(cineplaneta)
    cines.add_hijos(cinestark)
    terminado = False;
    while not terminado:
        print('Ingrese la opción que desea realizar')
        print('(1) Listar cines')
        print('(2) Listar cartelera')
        print('(3) Comprar entrada')
        print('(0) Salir')
        opcion = input('Opción: ')

        if opcion == '1':
            print('********************')
            print('Lista de cines')
            cines.imprimir_cine() #Patron Comporsite
            print('********************')

        elif opcion == '2':
            print('********************')
            print('Lista de cines')
            cines.imprimir_cine() #Patron Comporsite
            print('********************')

            cine = input('Primero elija un cine:')
#######################################################
            #Patron Factory
            factory = CineFactory()
            cine = factory.obtener_cines(cine)
            peliculas = cine.listar_peliculas()
#######################################################
            print('********************')
            func_decoradora = p_decorator(mostrar_pelicula)#Patron decorator
            func_decoradora(peliculas)#Patron decorator
            print('********************')

        elif opcion == '3':
            print('********************')
            print('COMPRAR ENTRADA')
            print('Lista de cines')
            cines.imprimir_cine() #Patron Comporsite
            print('********************')
            cine = input('Primero elija un cine:')
#######################################################
            #Patron Factory
            factory = CineFactory()
            cine = factory.obtener_cines(cine)
            peliculas = cine.listar_peliculas()
#######################################################
            func_decoradora = p_decorator(mostrar_pelicula)#Patron decorator
            func_decoradora(peliculas)#Patron decorator
            pelicula_elegida = input('Elija pelicula:')
            print('Ahora elija la función (debe ingresar el formato hh:mm): ')
            for funcion in cine.listar_funciones(pelicula_elegida):
                print('Función: {}'.format(funcion))
            funcion_elegida = input('Funcion:')
            cantidad_entradas = input('Ingrese cantidad de entradas: ')
            codigo_entrada = cine.guardar_entrada(pelicula_elegida, funcion_elegida, cantidad_entradas)
            print('Se realizó la compra de la entrada. Código es {}'.format(codigo_entrada))
        elif opcion == '0':
            terminado = True
        else:
            print(opcion)



if __name__ == '__main__':
    main()
