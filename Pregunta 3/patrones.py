import sys
import sqlite3

class manage_db:
    def __init__(self):
        self.namedb = "cadenacine.db"
        self.conn = sqlite3.connect(self.namedb)
        self.c = self.conn.cursor()

    def createCineTable(self):
        self.c.execute("DROP TABLE IF EXISTS cine")
        # creating table
        self.c.execute("CREATE TABLE cine (idCine INTEGER PRIMARY KEY, nombreCine TEXT)")
        # insert row
        self.c.execute("INSERT INTO cine VALUES (1, 'Cineplaneta')")
        self.c.execute("INSERT INTO cine VALUES (2, 'Cinestark')")

    def createPeliculaTable(self):
        self.c.execute("DROP TABLE IF EXISTS pelicula")
        # creating table
        self.c.execute("CREATE TABLE pelicula (idPelicula INTEGER PRIMARY KEY, nombrePelicula TEXT)")
        # insert row
        self.c.execute("INSERT INTO pelicula VALUES (1, 'IT')")
        self.c.execute("INSERT INTO pelicula VALUES (2, 'La Hora Final')")
        self.c.execute("INSERT INTO pelicula VALUES (3, 'Desparecido')")
        self.c.execute("INSERT INTO pelicula VALUES (4, 'Deep El Pulpo')")

    def createFuncionTable(self):
        self.c.execute("DROP TABLE IF EXISTS funcion")
        # creating table
        self.c.execute("CREATE TABLE funcion (idFuncion INTEGER PRIMARY KEY, hora TEXT)")
        # insert row
        self.c.execute("INSERT INTO funcion VALUES (1,'19:00')")
        self.c.execute("INSERT INTO funcion VALUES (2,'20:30')")
        self.c.execute("INSERT INTO funcion VALUES (3,'22:00')")
        self.c.execute("INSERT INTO funcion VALUES (4,'21:00')")
        self.c.execute("INSERT INTO funcion VALUES (5,'20:00')")
        self.c.execute("INSERT INTO funcion VALUES (6,'23:00')")
        self.c.execute("INSERT INTO funcion VALUES (7,'16:00')")

    def createMultitable(self):
        self.c.execute("DROP TABLE IF EXISTS cineXpeliculaXfuncion")
        # creating table
        self.c.execute("CREATE TABLE cineXpeliculaXfuncion (idCine INTEGER, idPelicula INTEGER, idFuncion INTEGER, FOREIGN KEY(idCine) REFERENCES cine(idCine), FOREIGN KEY(idPelicula) REFERENCES pelicula(idPelicula), FOREIGN KEY(idFuncion) REFERENCES funcion(idFuncion), PRIMARY KEY (idCine, idPelicula, idFuncion))")
        # insert row
        self.c.execute("INSERT INTO cineXpeliculaXfuncion VALUES (1, 1, 1)")
        self.c.execute("INSERT INTO cineXpeliculaXfuncion VALUES (1, 1, 2)")
        self.c.execute("INSERT INTO cineXpeliculaXfuncion VALUES (1, 1, 3)")
        self.c.execute("INSERT INTO cineXpeliculaXfuncion VALUES (1, 2, 4)")
        self.c.execute("INSERT INTO cineXpeliculaXfuncion VALUES (1, 3, 5)")
        self.c.execute("INSERT INTO cineXpeliculaXfuncion VALUES (1, 3, 6)")
        self.c.execute("INSERT INTO cineXpeliculaXfuncion VALUES (1, 4, 7)")
        self.c.execute("INSERT INTO cineXpeliculaXfuncion VALUES (2, 3, 4)")
        self.c.execute("INSERT INTO cineXpeliculaXfuncion VALUES (2, 3, 6)")
        self.c.execute("INSERT INTO cineXpeliculaXfuncion VALUES (2, 4, 7)")
        self.c.execute("INSERT INTO cineXpeliculaXfuncion VALUES (2, 4, 5)")

    def createEntradaTable(self):
        self.c.execute("DROP TABLE IF EXISTS entrada")
        # creating table
        self.c.execute(
            "CREATE TABLE entrada (idEntrada INTEGER PRIMARY KEY, cantEntrada INTEGER, idCine INTEGER, idPelicula INTEGER, idFuncion INTEGER, FOREIGN KEY(idCine) REFERENCES cineXpeliculaXfuncion(idCine), FOREIGN KEY(idPelicula) REFERENCES cineXpeliculaXfuncion(idPelicula), FOREIGN KEY(idFuncion) REFERENCES cineXpeliculaXfuncion(idFuncion))")

def listar_cines(c):
    for x in c.execute('SELECT * FROM cine'):
        print(str(x[0]) + ". " + x[1])
    print('********************')

def show_interface():
    print('Ingrese la opción que desea realizar')
    print('(1) Listar cines')
    print('(2) Listar cartelera')
    print('(3) Comprar entrada')
    print('(0) Salir')

def listar_cartelera(c, idCine):
    for x in c.execute("SELECT distinct cineXpeliculaXfuncion.idPelicula, nombrePelicula FROM cineXpeliculaXfuncion INNER JOIN pelicula ON pelicula.idPelicula = cineXpeliculaXfuncion.idPelicula "
            "WHERE idCine =?", idCine):
        print(str(x[0]) + ". " + x[1])
    print('********************')

def listar_funciones(c, ids):
    for funcion in c.execute(
            "SELECT hora FROM cineXpeliculaXfuncion INNER JOIN funcion ON funcion.idFuncion = cineXpeliculaXfuncion.idFuncion WHERE idCine = ? and idPelicula = ?",
            ids):
        print(funcion[0])
    print('********************')

def registrar_entrada(c, data):
    c.execute("INSERT INTO entrada values (null,?,?,?,?)", data)

def obtener_nroEntradaRegistrada(c):
    c.execute("SELECT max(idEntrada) from entrada")
    cod = str(c.fetchone()[0])
    return cod

def main():

    admin = manage_db()

    admin.createCineTable()
    admin.createPeliculaTable()
    admin.createFuncionTable()
    admin.createMultitable()
    admin.createEntradaTable()
    admin.conn.commit()

    terminado = False;
    while not terminado:
        show_interface()

        opcion = input('Opción: ')

        if opcion == '1':
            print('********************')
            print('Lista de cines')
            listar_cines(admin.c)

        elif opcion == '2':
            print('********************')
            print('Lista de cines')
            listar_cines(admin.c)

            cine = input('Primero elija un cine:')
            t = (cine,)
            print('********************')
            listar_cartelera(admin.c, t)

        elif opcion == '3':
            print('********************')
            print('COMPRAR ENTRADA')
            print('Lista de cines')
            listar_cines(admin.c)

            cine = input('Primero elija un cine:')
            t = (cine,)
            print('********************')

            listar_cartelera(admin.c, t)

            pelicula_elegida = input('Elija pelicula:')

            ids = (cine,pelicula_elegida)
            print('Ahora elija la función (debe ingresar el formato hh:mm): ')

            listar_funciones(admin.c, ids)

            funcion_elegida = input('Funcion:')
            cantidad_entradas = input('Ingrese cantidad de entradas: ')

            data = (cantidad_entradas, cine, pelicula_elegida, funcion_elegida,)
            registrar_entrada(admin.c, data)

            cod = obtener_nroEntradaRegistrada(admin.c)

            print("Se realizó la compra de la entrada. El código es " + cod)

        elif opcion == '0':
            terminado = True
        else:
            print(opcion)

if __name__ == '__main__':
    main()
