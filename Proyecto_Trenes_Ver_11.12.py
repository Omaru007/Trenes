import tkinter
from tkinter import *

# ---------------------------------------------------------------------------------------------------
# Proyecto #2           [IC1803] - Taller de Programación
# 2020028513            Natifpee Durán Campos
# 2019334177            Omar S. Chacón Porras
# ---------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------
# Variables globales.
# ---------------------------------------------------------------------------------------------------

administradores = []
ciudades = []
conexiones = []
paises = []
rutas = []
tipoTren = []
trenes = []
usuarios = []

repetidos = []
errores = []
eliminados = []

ultimoTren = []
ultimaRuta = []

fila = []
filasTipoTren = [] #  [ [01,[987,231,652]] , [02,[]] , [03,[]] , [04,[]] ]
reservaciones = []
facturas = []
# ---------------------------------------------------------------------------------------------------
# Pasar la información de los archivos a las variables globales.
# ---------------------------------------------------------------------------------------------------

def asignarLista():
    global administradores
    global ciudades
    global conexiones
    global paises
    global rutas
    global tipoTren
    global trenes
    global usuarios
    administradores = enlistar("Administradores.txt")    
    ciudades = enlistar("Ciudades.txt")
    conexiones = enlistar("Conexiones.txt")
    paises = enlistar("Paises.txt")
    rutas = enlistar("Rutas.txt")
    tipoTren = enlistar("TipoTren.txt")
    trenes = enlistar("Trenes.txt")
    usuarios = enlistar("Usuarios.txt")
    
def enlistar(archivo):
    lista = []
    with open(archivo,"r") as file:
        for line in file:              
            lista += [[x.strip()for x in line.split(";")]]
    lista = arreglarLista(lista)
    return(lista)

def arreglarLista(lista):
    res = []
    elem = []
    for i in lista:
        for j in i:
            try:
                if isinstance(eval(j),int):
                    elem += [eval(j)]
            except:
                elem += [j]
        res += [elem]
        elem = []
    return(res)
asignarLista()    

# ---------------------------------------------------------------------------------------------------
# Verificar la información de los archivos.
# ---------------------------------------------------------------------------------------------------

def comprobarInformacion():
    verificarPaises()
    verificarCiudades()
    verificarConexiones()
    verificarTipoTren()
    verificarTrenes()
    verificarRutas()
    verificarAdmin()
    verificarUser()
    hacerFilasTipoTren()
    menu()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Verificar Usuario

def verificarUser():
    global usuarios
    global errores
    global repetidos
    contador = 0
    res = []
    for i in usuarios:
        if i[4] != 1 and i[4] != 0:
            errores += ["Informacion de estado migratorio indetectable"]
            repetidos += [[i]]
    for i in usuarios:
        contador = 0    
        for j in usuarios:
            if j[2] == i[2]:
                contador += 1
        if contador >=2:
            errores += ["Numero de pasaporte repetido"]
            repetidos += [[i]]
        else:
            res += [i]
    usuarios = res
    verificarUserPaises()
    verificarUserCiudades()
    return

def verificarUserPaises():
    global paises
    global usuarios
    global errores
    global repetidos
    contador = 0
    res = []
    for i in usuarios:
        for j in paises:
            if j[0] == i[0]:
                res += [i]
                
            else:
                contador += 1
        if contador >= 1:
            errores += [["Pais de usuario no existente"]]
            repetidos += [[i]]
        contador = 0
    usuarios = res
    return

def verificarUserCiudades():
    global ciudades
    global usuarios
    global errores
    global repetidos
    res = []
    contador = 0
    for i in usuarios:
        for j in ciudades:
            if j[1] == i[1]:
                res += i
            else:
                contador += 1
        if contador >= 1:
            errores += [["Ciudad de usuario no existente"]]
            repetidos += [[i]]
        contador = 0
    return

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Verificar Administrador

def verificarAdmin():
    global administradores
    global errores
    global repetidos
    res = []
    contador = 0
    for i in administradores:
        contador = 0
        for j in administradores:
            if j[0] == i[0]:
                contador += 1
        if contador >=2:
            errores += [["Codigo de administrador repetido"]]
            repetidos += [[i]]
        else:
            res += [i]
    administradores = res
    return

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Verificar Paises

def verificarPaises():
    global paises
    global errores
    global repetidos
    cont = 0
    tempLista = []
    for i in paises:
        cont = 0
        if tempLista == []:
            tempLista += [i]
        else:
            for j in tempLista:
                if i[0]==j[0]:
                    repetidos += [i]
                    errores += [["Codigo de pais repetido"]]
                    cont += 1
            if cont == 0:
                tempLista = tempLista+[i]
    paises = tempLista


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~       
# Verificar Ciudades

def verificarCiudades():
    global ciudades
    global errores
    global repetidos
    cont = 0
    tempLista = []
    for i in ciudades:
        if comprobarPAIS(i[0]) == True:
            cont = 0
            if tempLista == []:
                tempLista += [i]
            else:
                for j in tempLista:
                    if i[1]==j[1]:
                        cont += 1
                        repetidos += [[i]]
                        errores += [["Pais repetido"]]
                if cont == 0:
                    tempLista = tempLista+[i]
    ciudades = tempLista

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Verificar Tipos de tren

def verificarTipoTren():
    global tipoTren
    global errores
    global repetidos
    res = []
    for i in tipoTren:
        if res == []:
                res += [i]
        else:
            if estaTipoTren(i,res):
                errores += ["Tipo de Tren repetido"]
                repetidos += [i]
            else:
                res += [i]
    tipoTren = res
    return

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Verificar Trenes

def verificarTrenes():
    global trenes
    global errores
    global repetidos
    contador = 0
    res1 = []
    for i in trenes:
        if estaTipoTren(i,tipoTren):
            res1 += [i]
        else:
            errores += ["Tipo de tren no existente"]
            repetidos += [i]

    res2 = []
    for i in res1:
        if res2 == []:
                res2 += [i]
        elif buscarTren_aux(i[1],res2):
            errores += ["Codigo de tren repetido"]
            repetidos += [i]
        else:
            res2 += [i]

    res3 = []
    tren = []
    cont = 0
    for i in res2:
        for j in i:
            if cont < 4:
                tren += [j]
            elif buscarRutas(j) == True:
                tren += [i]
            else:
                errores += ["Ruta no existente en tren"]
        if len(tren) == 4:
            errores +=["Tren sin rutas"]
            repetidos += [j]
        else:
            res3 += [tren]
        tren = []
    trenes = res3
    return

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Verificar Conexiones

def verificarConexiones():
    global conexiones
    global repetidos
    global errores
    cont = 0
    tempLista = []
    for i in conexiones:
        if not comprobarPAIS(i[0])==True or  not comprobarPAIS(i[3])==True:
            errores += [["La conexión", i[2], "presenta un pais inexistente en la base de datos"]]
            repetidos += [i]
        elif not comprobarCIUDAD(i[1])==True or not comprobarCIUDAD(i[4])==True:
            errores += [["La conexión", i[2], "presenta una ciudad inexistente en la base de datos"]]
            repetidos += [i]
        elif not comprobarCiudadEnPais(i[0],i[1]) == True or not comprobarCiudadEnPais(i[3],i[4]) == True:
            errores += [["La conexión", i[2], "presenta un pais inexistente en la base de datos"]]
            repetidos += [i]
        else:
            cont = 0
            if tempLista == []:
                tempLista += [i]
            else:
                for j in tempLista:
                    if i[2]==j[2]:
                        cont += 1
                if cont == 0:
                    tempLista += [i]
                if cont > 0:
                    repetidos += [[i]]
    conexiones = tempLista

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Verificar Ruta

def verificarRutas():
    global rutas
    global errores
    global repetidos
    res = []
    for i in rutas:
        if buscarTipoTren(i[0]) == False:
            repetidos += [i]
            errores += [["Tipo de tren de ruta no existente"]]
        else:
            if buscarTren(i[1]) == False:
                errores += [["Tren de ruta no existente"]]
                repetidos += [i]
            else:
                if buscarRutas(i[4:]) == False:
                    errores += [["Codigo de ruta repetido"]]
                    repetidos += [i]
                else:
                    if comprobarCONEXIONciudad(i[3],i[5]) == False:
                        errores += [["No existe conexion entre ",i[3]," y ",i[5]]]
                        repetidos += [i]
                    else:
                        if comprobarCONEXIONpais(i[4],i[6]) == False:
                            errores += [["No existe conexion entre ",i[4]," y ",i[6]]]
                            repetidos += [i]
                        else:
                            res += [i]
    rutas = res
    return

def hacerFilasTipoTren():
    global tipoTren
    global filasTipoTren
    for i in tipoTren:
        filasTipoTren += [[i[0],[]]]
    return

# ---------------------------------------------------------------------------------------------------
# Menú Principal
# ---------------------------------------------------------------------------------------------------

def menu():
    menuPrincipal = Tk()
    menuPrincipal.title("Menu Principal")
    menuPrincipal.geometry("675x375")
    menuPrincipal.resizable(False,False)
    panel = Frame(menuPrincipal,bg = "lavender",width = 700,height = 527)
    panel.place(x = 0,y=0)
    labelTitulo = Label(panel,text = "Bienvenido al Menú Principal",bg="lavender",fg="black",font = ("Helvetica",24))
    labelTitulo.place(x = 140,y = 75)#creacion, configuracion y colocacion de un titulo
    labelTitulo = Label(panel,text = "¿Como le gustaría ingresar?",bg="lavender",fg="black",font = ("Helvetica",20))
    labelTitulo.place(x = 165,y = 120)#creacion, configuracion y colocacion de un titulo
    admin = Button(panel,text = "Administrador",bg = "light grey",width=16,height = 3,command = lambda:[menuPrincipal.withdraw(),comprobarAdmin()])
    admin.place(x=170,y=200)
    user = Button(panel,text = "Usuario",bg = "light grey",width=16,height = 3,command = lambda:[menuPrincipal.withdraw(),comprobarUser()])
    user.place(x=370,y=200)

# ---------------------------------------------------------------------------------------------------     
# Verificar codigo de ingreso.
# ---------------------------------------------------------------------------------------------------

def comprobarAdmin():
    global administradores
    codigo = input(" Digite su codigo de administrador: ",)
    try:
        codigo = eval(codigo)
    except:
        print("")
    for i in administradores:
        if i[0] == codigo:
            print("Bienvenid@ ",i[1])
            menuAdmin()
            return
    print(" Favor digitar un codigo valido.")
    print(" Intente de nuevo.")
    menu()
    return

def comprobarUser():
    global usuarios
    pasaporte = input(" Digite numero de pasaporte: ",)
    try:
        pasaporte = eval(pasaporte)
    except:
        print("")
    for i in usuarios:
        if i[2] == pasaporte:
            print("")
            print(" Bienvenid@ ",i[3])
            print("")
            if i[4] == 1:
                print(" Actualmente se presenta un problema con su estado migratorio.")
                print(" Contacte a un administrador para consultar sobre su estado migratorio.")
                print("")
            menuUser("user")
            return 
    print(" Se ha digitado un codigo invalido.")
    print(" El codigo no corresponde a ningún usuario.")
    print("")
    print(" ¿Desea crear un usuario nuevo? ")
    print(" > Si")
    print(" > No")
    newUser = input(" >>",)
    if newUser.upper().strip() == "SI":
        crearUsuario("menu")
        return 
    print(" Intente de nuevo.")
    comprobarUser()

# ---------------------------------------------------------------------------------------------------
# Crear Nuevo Usuario
# ---------------------------------------------------------------------------------------------------

def crearUsuario(flag):
    global usuarios
    pais = userPais()
    ciudad = userCiudad(pais)
    if flag == "menu":
        pasaporte = userPasaporte()
    else:
        pasaporte = flag[1]
    print(" Digite nombre.")
    nombre = input(" > ",)
    nuevoUsuario = [pais,ciudad,pasaporte,nombre]
    usuarios += nuevoUsuario
    print(" El usuario ha sido creado exitosamente.")
    if flag == "menu":
        menu()
        return
    return
        
        
    
    
def userPais():
    print(" Digite pais de procedencia")
    pais = input(" > ",)
    try:
        pais = eval(pais)
    except:
        print(" Solo aceptamos un numero entero como codigo")
        print(" Intente nuevamente")
    if comprobarPAIS(pais) == False:
        print(" Pais no existente en la base de datos")
        print(" Intente nuevamente")
        userPais()
        return
    else:
        return pais

    
def userCiudad(pais):
    print(" Digite ciudad de procedencia")
    ciudad = input(" > ",)
    try:
        ciudad = eval(ciudad)
    except:
        print(" Solo aceptamos un numero entero como codigo")
        print(" Intente nuevamente")
    if comprobarCiudad(ciudad) == False:
        print(" Pais no existente en la base de datos")
        print(" Intente nuevamente")
        userCiudad()
    else:
        return ciudad

    
def userPasaporte():
    print(" Digite numero de pasaporte")
    pasaporte = input(" > ",)
    try:
        pasaporte = eval(pasaporte)
    except:
        print("")
    if comprobarUSUARIO(pasaporte) == True:
        print(" Pasaporte ya existente en la base de datos")
        print(" Intente nuevamente")
        userPasaporte()
    else:
        return pasaporte
    
# ---------------------------------------------------------------------------------------------------
# Menú Administrador
# ---------------------------------------------------------------------------------------------------

def menuAdmin():
    print("")
    print(" Bienvenid@ al Menú del Administrador.")
    print(" Seleccione una opcion para continuar.")
    print("")
    print("  1) Insertar elemento.")
    print("  2) Eliminar elemento.")
    print("  3) Modificar elemento.")
    print("  4) Consultas de informacion.")
    print("  5) Consultas del sistema.")
    print("  6) Venta de Tiquetes")
    print("  7) Cancelación de Reservaciones.")
    print("  8) Cerrar sesion")
    print("")
    opcion = input(">> ",)
    if not isinstance(eval(opcion),int):
        print(" Por favor digite unicamente el numero que corresponda a la opcion que desea.")
        print(" Intente de nuevo.")
        menuAdmin()
        return
    opcion = eval(opcion)
    if opcion >=1 and opcion<=8:
        if opcion == 1:
            menuInsertar()
        if opcion == 2:
            menuEliminar()
        if opcion == 3:
            menuModificar()
        if opcion == 4:
            menuUser("admin")
        if opcion == 5:
            menuSistema()
        if opcion == 6:
            menuVentas()
        if opcion == 7:
            cancelacion()
        if opcion == 8:
            menu()
    else:
        print(" Por favor digite unicamente el numero que corresponda a la opcion que desea.")
        print(" Intente de nuevo.")
        menuAdmin()

# ---------------------------------------------------------------------------------------------------
# Menú Usuario/Consultas
# ---------------------------------------------------------------------------------------------------

def menuUser(etiqueta):
    print("")
    print(" ¿Que información desea consultar?")
    print("")
    print("   1. Consultar Países")
    print("   2. Consultar Ciudades")
    print("   3. Consultar Conexiones")
    print("   4. Consultar Trenes")
    print("   5. Precio de una ruta")
    print("   6. Consultar asientos disponibles de un tren")
    print("   7. Consultar Rutas")
    print("   8. Precio de una conexion")
    if etiqueta == "user":
        print("   9. Reservar Asientos.")
        print("   10. Facturación")
        print("")
        print("   11. Cerrar sesion")
    if etiqueta != "user":
        print("")
        print("   9. Volver")
    print("")
    opcion = input(">> ",)
    opcion = eval(opcion)
    if opcion <= 8 and opcion >= 1:
        if opcion == 1:
            consultarPaises(etiqueta)
        if opcion == 2:
            consultarCiudades(etiqueta)
        if opcion == 3:
            consultarConexiones(etiqueta)
        if opcion == 4:
            consultarTrenes(etiqueta)
        if opcion == 5:
            consultarPrecioRuta(etiqueta)
        if opcion == 6:
            consultarAsientos(etiqueta)
        if opcion == 7:
            consultarRutas(etiqueta)
        if opcion == 8:
            precioDeConexion(etiqueta)
    if etiqueta == "user":
        if opcion == 9:
            reservacion()
        if opcion == 10:
            facturacion()
        if opcion == 11:
            menu()
    elif etiqueta != "user":
        if opcion == 9:
            menuAdmin()
    else:
        print(" Por favor digite unicamente el numero que corresponda a la opcion que desea.")
        print(" Intente de nuevo.")
        menuUser()


# ---------------------------------------------------------------------------------------------------
# Reservaciones
# ---------------------------------------------------------------------------------------------------

def reservacion():
    global rutas
    global trenes
    global reservaciones
    print("")
    print(" Bienvenido al sistema de reservaciones.")
    print("")
    print(" Digite la información según corresponda.")
    
    pasaporte = aux_reserve1()
    tipoTren = aux_reserve2()
    codTren = aux_reserve3()
    codRuta = aux_reserve4(codTren)
        
    precioUnidad = 0
    
    for i in rutas:
        if i[2] == codRuta:
            print (" El precio cada asiento para la ruta ", i[2], "es", i[7],".")
            precioUnidad = i[7]
    
    numAsientosDisponibles = 0
    
    for i in trenes:
        if i[1] == codTren:
            print(" Actualmente hay", i[3], "asientos disponibles en el tren", i[1])
            numAsientosDisponibles = i[3]
            
    numAsientos = aux_reserve5(numAsientosDisponibles)
    precioTotal = precioUnidad*numAsientos

    if reservaciones != []:
        for i in reservaciones:
            if i[0] == pasaporte:
                i[1] + [[tipoTren,codTren,codRuta,numAsientos,precioUnidad,precioTotal]]
                print(" Su reservacion se ha procesado exitosamente.")
                return

    reservaciones += [[pasaporte,[[tipoTren,codTren,codRuta,numAsientos,precioUnidad,precioTotal]]]]
    print(" Su reservacion se ha procesado exitosamente.")
    
    menuUsuario()

def aux_reserve1():
    print("")
    pasaporte = input(" Numero de Pasaporte: ",)
    try:
        pasaporte = eval(pasaporte)
    except:
        print(" ")
    if comprobarUSUARIO(pasaporte) == True:
        return pasaporte
    else:
        print(" Valor ingresado invalido.")
        print(" Intente de nuevo.")
        aux_reserve1()


def aux_reserve2():
    print("")
    valor = input(" Tipo de Tren: ",)
    if buscarTipoTren(valor) == True:
        return valor
    else:
        print(" Valor ingresado invalido.")
        print(" Intente de nuevo.")
        aux_reserve2()

def aux_reserve3():
    print("")
    valor = input(" Codigo de Tren: ",)
    try:
        valor = eval(valor)
    except:
        print(" Valor ingresado invalido.")
        print(" Intente de nuevo.")
        aux_reserve3()
    if buscarTren(valor) == True:
        return valor
    else:
        print(" Valor ingresado invalido.")
        print(" Intente de nuevo.")
        aux_reserve3()

def aux_reserve4(codTren):
    print("")
    valor = input(" Codigo de Ruta: ",)
    try:
        valor = eval(valor)
    except:
        print(" Valor ingresado invalido.")
        print(" Intente de nuevo.")
        aux_reserve4(codTren)
    
    if buscarRutas(valor) == True:
        if trenYRuta(valor,codTren) == True:
            return valor
        else:
            print(" La ruta ingresada no correspode con el tren.")
            print(" Intente ingresando otro codigo de ruta.")
            aux_reserve4(codTren)            
    else:
        print(" Valor ingresado invalido.")
        print(" Intente de nuevo.")
        aux_reserve4(codTren)

def aux_reserve5(numAsientosDisponibles):
    print("")
    valor = input(" Numero de asientos que desea reservar: ",)
    try:
        valor = eval(valor)
    except:
        print(" Valor ingresado invalido.")
        print(" Intente de nuevo.")
        aux_reserve5(numAsientosDisponibles)
    
    if valor > 0:
        print(" Favor ingresar un número positivo.")
        aux_reserve5(numAsientosDisponibles)
    
    elif valor <= numAsientosDisponibles:
        return valor
    
    else:
        print(" Actualmente es imposible cumplir con su solicitud.")
        print(" Intente ingrsar un numero menor.")
        aux_reserve5(numAsientosDisponibles)
        

# ---------------------------------------------------------------------------------------------------
# Facturacion
# ---------------------------------------------------------------------------------------------------
        
def facturacion():
    global reservaciones
    print(" Bienvenido al apartado Facturas")
    print(" Por favor digite el pasaporte de quien se efectuara la factura")
    pasaporte = input(" >> ",)
    try:
        pasaporte = eval(pasaporte)
    except:
        print("")
    for i in reservaciones:
        if pasaporte == i[0]:
            print(" Cual de las siguientes reservaciones le gustaria efectuar la factura:")
            contador = 1
            for j in i[1]:
                print(contador,": ",j)
                contador += 1
            factura = input(" >>",)
            try:
                factura = eval(factura)
                factura = factura - 1
            except:
                print("")
                print(" Digite un numero entero como pasaporte")
                print(" Intente nuevamente")
                facturacion()
            crearFactura(i[0],i[1][factura],factura+1)
            guardarFactura(i[0],i[1][factura])
            menuUser()
    print(" No se encuentran reservaciones a su nombre")
    print(" Volviendo al menu")
    menuUser()        
    return 


def guardarFactura(usuario,factura):
    global facturas
    if facturas == []:
        facturas += [[usuario,[factura]]]
        return
    for i in facturas:
        if i[0] == usuario:
            i[1] += factura
            return
    facturas += [[usuario,[factura]]]
    return

           
def crearFactura(pasaporte,reservacion,numero):
    pasaporte = str(pasaporte)
    numero = str(numero)
    nombre = "Factura "+pasaporte+"-"+numero
    usuario = getNombre(pasaporte)
    factura = open(nombre+".txt","w")
    factura.write(nombre+"\n")
    factura.write(" Pasaporte "+pasaporte+"\n")
    factura.write(" Nombre "+usuario+"\n")
    factura.write(" Tipo Tren "+reservacion[0]+"\n")
    factura.write(" Tren "+reservacion[1]+"\n")
    factura.write(" Ruta "+reservacion[2]+"\n")
    factura.write(" Numero de Asientos "+reservacion[3]+"\n")
    factura.write(" Precio Unitario "+reservacion[4]+"\n")
    factura.write(" Total: "+reservacion[5]+"\n")
    factura.close()

def getNombre(pasaporte):
    global usuarios
    for i in usuarios:
        if pasaporte == i[2]:
            return i[3]    
    


# ---------------------------------------------------------------------------------------------------
# Consultas
# ---------------------------------------------------------------------------------------------------

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Consultar Paises.
# Imprime todos los paises en la base de datos con sus codigos respectivos.

def consultarPaises(etiqueta):
    global paises
    print(" Ofrecemos nuestros servicios en los siguientes paises:")
    print("")
    for i in paises:
        print(i[0], i[1])
    print("")
    if etiqueta == "user":
        menuUser(etiqueta)
    else:
        menuAdmin()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Consultar Ciudades.
# Apunta todas las ciudades de un pais en especifico.

def consultarCiudades(etiqueta):
    pais = input("Digite el codigo del pais para el que desea consultar: ",)
    pais = eval(pais)
    if isinstance (pais,int):
        if comprobarPaisParaCiudad(pais)==True:
            print("")
            print("Este pais ofrece servicios en las siguientes ciudades:")
            print("")
            global ciudades
            for i in ciudades:
                if i[0]==pais:
                    print (i[1],i[2])
        else:
            print("Se ha digitado un codigo invalido. Intente de nuevo.")
    else:
        print("Se ha digitado un codigo invalido. Intente de nuevo.")
    print("")
    if etiqueta == "user":
        menuUser(etiqueta)
    else:
        menuAdmin()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Consultar conexiones
# Apunta todas las conexiones de una ciudad especifica dentro de un pais especifico.

def consultarConexiones(etiqueta):
    global conexiones
    global ciudades
    global paises
    pais = input(" Digite el codigo del pais que desea consultar: ",)
    ciudad = input(" Digite el codigo de la ciudad que desea consultar: ",)
    pais = eval(pais)
    ciudad = eval(ciudad)
    if comprobarPaisParaCiudad(pais) == False:
        print("Pais no existente")
        print("Intente de nuevo")
        print("")
        consultarConexiones()
    if comprobarCiudad(pais,ciudad) == False:
        print("Ciudad no existente")
        print("Intente de nuevo")
        print("")
        consultarConexiones()
    for k in paises:
        if k[0] == pais:
            for j in ciudades:
                if j[1] == ciudad:
                    print("La ciudad ",j[2]," del pais ",k[1]," posee las siguientes conexiones:")
    for i in conexiones:
        if i[0] == pais:
            if i[1] == ciudad:
                print("Destino: ",i[3:5],"  Codigo: ",i[2])
    print("")
    if etiqueta == "user":
        menuUser(etiqueta)
    else:
        menuAdmin()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Consultar Trenes.
# Imprime todos los trenes de un mismo tipo.

def consultarTrenes(etiqueta):
    global trenes
    for i in tipoTren:
        print(i[0],". ",i[1])
    print("Digite el codigo correspondiente con")
    tipo = input("el tipo de tren que desea consultar: ",)
    print("")
    if comprobarTipoParaTren(tipo)==True:
        for i in trenes:
            if i[0]==tipo:
                print (i[1],i[2])
    else:
        print("")
        print(" Actualmente no existe un tren con el codigo de tipo de tren ingresado.")
        print(" Intente de nuevo.")

    if etiqueta == "user":
        menuUser(etiqueta)
    else:
        menuAdmin()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Consultar Precios
# Imprime el precio de un tren especifico.

def consultarPrecioRuta(etiqueta):
    global rutas
    codigoTipoTren = input("Digite el codigo del tipo de tren: ",)
    if buscarTipoTren(codigoTipoTren) == False:
        print(" Tipo de tren no existente.")
        print(" Intente de nuevo")
        consultarPrecios()
        
    codigoTren = input(" Digite el codigo del tren: ",)
    codigoTren = eval(codigoTren)
    if buscarTren(codigoTren) == False:
        print(" Tren no existente.")
        print(" Intente de nuevo")
        consultarPrecios()
    contador = 0
    for i in rutas:
        if i[0] == codigoTipoTren and i[1] == codigoTren:
                contador += 1
                break
    if contador == 1:
        print(" El tren que busca tiene los siguientes precios:")
        for i in rutas:
            if i[0] == codigoTipoTren and i[1] == codigoTren:
                print("Codigo de ruta: ",i[2],"  Precio: ",i[7])
    else:
        print("Ruta no disponible")
    if etiqueta == "user":
        menuUser(etiqueta)
    else:
        menuAdmin()
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Consultar asientos disponibles.
# Imprime numero de asientos disponibles de un tren en especifico.

def consultarAsientos(etiqueta):
    global trenes
    tipoTren = input("Digite el codigo del tipo del tren: ",)
    if buscarTipoTren(tipoTren) == False:
        print("Tipo de tren no existente!!!")
        print("Intente de nuevo")
        consultarAsientos()
        
    tren = input("Digite el codigo del tren: ",)
    tren = eval(tren)
    if buscarTren(tren) == False:
        print("Tren no existente!!!")
        print("Intente de nuevo")
        consultarAsientos()
    for i in trenes:
        if i[0] == tipoTren and i[1] == tren:
            print("En el tren", i[2], "hay", i[3], "asientos disponibles")
    print("")
    if etiqueta == "user":
        menuUser(etiqueta)
    else:
        menuAdmin()
        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Consultar Rutas
# Imprime las rutas de un tren especifico.

def consultarRutas(etiqueta):
    tipoTren = input("Digite el codigo del tipo de tren para el que desea consultar: ",)
    tren = input("Digite el codigo del tren para el que desea consultar: ",)
    tren = eval(tren)
    if isinstance (tren,int):
        if buscarTipoTren(tipoTren) == True:
            if buscarTren(tren) == True:
                if comprobarTrenParaRutas(tren)==True:
                    global rutas
                    for i in rutas:
                        if i[1]==tren:
                            print ("Ruta", i[2])
                else:
                    print("Actualmente este tren no tiene rutas disponibles")
            else:
                print("Se ha digitado un codigo invalido. Intente de nuevo.")
        else:
            print("Tipo de tren no disponible")
    else:
        print("Se ha digitado un codigo invalido. Intente de nuevo.")
    print("")
    if etiqueta == "user":
        menuUser(etiqueta)
    else:
        menuAdmin()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Consultar Precio de una conexion
# Imprime el pais, la ciudad de partida y de llegada, e indica el precio.

def precioDeConexion(etiqueta):
    global conexiones
    print(" Digite una conexion para saber el precio")
    conexion = input(" >> ", )
    try:
        conexion = eval(conexion)
    except:
        print(" Digite un numero valido")
        print("")
        precioDeConexion(etiqueta)
    for i in conexiones:
        if i[2] == conexion:
            print(" Pais: ", i[0])
            print(" Ciudad de partida: ", i[1])
            print(" Ciudad de llegada: ", i[4])
            print(" Precio: ", i[6])
            print("")
    if etiqueta == "user":
        menuUser(etiqueta)
    else:
        menuAdmin()

# ---------------------------------------------------------------------------------------------------
# Menú de Sistema
# ---------------------------------------------------------------------------------------------------

def menuSistema():
    global paises
    global ciuidades
    global conexiones
    global trenes
    global eliminados
    print("")
    print(" Seleccione una opcion.")
    print("   1) Ultimo pais ingresado")
    print("   2) Ultima ciudad ingresada")
    print("   3) Ultima conexion ingresada")
    print("   4) Ultimo tren ingresado")
    print("   5) Ultimo elemento eliminado")
    print("   6) Ruta mas utilizada")
    print("   7) Ruta nunca utilizada")
    print("   8) Pais mas visitado")
    print("   9) Ciudad mas visitada")
    print("   10) Usuario que mas compro")
    print("   11) Usuario que menos compro")
    print("   12) Cantidad de compras por usuario")
    print("   13) Tren mas utilizado")
    print("   14) Tren menos utilizado")
    opcion = input("> ",)
    if not isinstance(eval(opcion),int):
        print(" Digite un numero entre 1 al 14")
        print(" Intente de nuevo")
        menuSistema()
        return
    opcion = eval(opcion)
    if opcion >=1 and opcion <= 14:
        if opcion == 1:
            print(paises[-1])
            menuAdmin()
        if opcion == 2:
            print(ciudades[-1])
            menuAdmin()
        if opcion == 3:
            print(conexiones[-1])
            menuAdmin()
        if opcion == 4:
            print(trenes[-1])
            menuAdmin()
        if opcion == 5:
            if eliminados == []:
                print(" Actualmente no se a eliminado ningun elemento.")
            else:
                print(eliminados[-1])
            menuAdmin()
        if opcion == 6:
            rutaMasUsada()
            menuAdmin()
        if opcion == 7:
            rutaNuncaUtilizada()
            menuAdmin()
        if opcion == 8:
            paisMasVisitado()
            menuAdmin()
        if opcion == 9:
            ciudadMasVisitada()
            menuAdmin()
        if opcion == 10:
            usuarioQueMasCompro()
            menuAdmin()
        if opcion == 11:
            usuarioQueMenosCompro()
            menuAdmin()
        if opcion == 12:
            comprasDeUsuario()
            menuAdmin()
        if opcion == 13:
            trenMasUsado()
            menuAdmin()
        if opcion == 14:
            trenMenosUsado()
            menuAdmin()
    else:
        print(" Por favor digite unicamente el numero que corresponda a la opcion que desea.")
        print(" Intente de nuevo")
        menuSistema()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Ruta Mas Utilizada
def rutaMasUsada():
    global reservaciones
    global rutas
    contador = 0
    mayor = 0
    ruta = []
    for i in rutas:
        contador = estaRutaInReservaciones(i[2])
        if contador > mayor:
            mayor = contador
            ruta = [i[2]]
        elif contador == mayor:
            ruta += [i[2]]
    if len(ruta) != 1:
        print(" No se encuentra ninguna ruta mas utilizada que las demas")
        print(" Volviendo al menu")
    else:
        print(" La ruta mas utilizada es:")
        print(" ",ruta)
    menuAdmin()
    return
            
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Ruta Nunca Utilizada
def rutaNuncaUtilizada():
    global rutas
    global reservaciones
    rutas = []
    contador = 0
    for i in rutas:
        contador = estaRutaInReservaciones(i[2])
        if contador == 0:
            rutas += [i[2]]
    if rutas == []:
        print(" Ninguna ruta se ha usado")
    else:
        print(" Estas son las rutas que todavia no se han usado:")
        print("")
        for i in rutas:
            print(i)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Pais mas Visitado
def paisMasVisitado():
    global rutas
    global paises
    contador = 0
    mayor = 0
    pais = []
    for i in rutas:
        contador = estaRutaInReservaciones(i[2])
        if contador > mayor:
            mayor = contador
            pais = [i[5]]
        elif contador == mayor:
            pais += [i[5]]
    if len(pais) != 1:
        print(" No se encuentra ningun pais mas visitado que las demas")
        print(" Volviendo al menu")
    else:
        for i in paises:
            if i[0] == pais[0]:
                pais = i[1]
        print(" El pais mas visitado es:")
        print(" ",pais)
    menuAdmin()
    return
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
# Ciudad mas visitada
def ciudadMasVisitada():
    global rutas
    global ciudades
    contador = 0
    mayor = 0
    ciudad = []
    for i in rutas:
        contador = estaRutaInReservaciones(i[2])
        if contador > mayor:
            mayor = contador
            ciudad = [i[6]]
        elif contador == mayor:
            ciudad += [i[6]]
    if len(ciudad) != 1:
        
        print(" No se encuentra ninguna ciudad mas visitada que las demas")
        print(" Volviendo al menu")
    else:
        for i in ciudades:
            if i[1] == ciudad[0]:
                ciudad = i[2]
        print(" La ciudad mas visitada es:")
        print(" ",ciudad)
    menuAdmin()
    return
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
# Usuario que mas Compro
def usuarioQueMasCompro():
    global reservaciones
    mayor = 0
    usuario = []
    for i in reservaciones:
        contador = 0
        for j in i[1]:
            contador += 1
        if contador > mayor:
            mayor = contador
            usuario = [i[0]]
        elif contador == mayor:
            usuario += [i[0]]
    if len(usuario) != 1:
        print(" No hay ningun usuario que haya comprado mas que los demas")
        print(" Volviendo al menu")
    else:
        print(" El usuario que mas compro es:")
        print(" ",usuario)
    menuAdmin() 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Usuario que menos compro
def usuarioQueMenosCompro():
    global reservaciones
    menor = 1000000000
    usuario = []
    for i in reservaciones:
        contador = 0
        for j in i[1]:
            contador += 1
        if contador < menor:
            menor = contador
            usuario = [i[0]]
        elif contador == menor:
            usuario += [i[0]]
    if len(usuario) != 1:
        print(" No hay ningun usuario que haya comprado menos que los demas")
        print(" Volviendo al menu")
    else:
        print(" El usuario que menos compro es:")
        print(" ",usuario)
    menuAdmin()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Cantidad de compras por usuario
def comprasDeUsuario():
    global facturas
    print(" Digite el numero de pasaporte del usuario")
    usuario = input(" >>", )
    try:
        usuario = eval(usuario)
    except:
        print(" ")
    if facturas == []:
        print(" No se encuentra ninguna factura efectuada")
        menuAdmin()
    for i in facturas:
        if i[0] == usuario:
            print(" El usuario ",usuario," a efectuado ",len(i[1])," compras.")
            print("")
            print("")
            menuAdmin()

        else:
            print(" Este usuario no a hecho ninguna reservacion")
            menuAdmin()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Tren mas utilizado
def trenMasUsado():
    global facturas
    global trenes
    mayor = 0
    tren = []
    contador = 0
    for i in trenes:
        contador = estaTrenEnFacturas(i[1])
        if contador > mayor:
            mayor = contador
            tren = [i[1]]
        if contador == mayor:
            tren += [i[1]]
    if len(tren) != 1:
        print(" No hay ningun tren mas utilizado que los demas")
        menuAdmin()
        return 
    print(" El tren mas utilizado es ",tren)
    print(" Con un total de ",mayor)
    menuAdmin()
    return
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Tren menos utilizado
def trenMenosUsado():
    global facturas
    global trenes
    menor = 100000000000
    tren = []
    contador = 0
    for i in trenes:
        contador = estaTrenEnFacturas(i[1])
        if contador < menor:
            menor = contador
            tren = [i[1]]
        if contador == menor:
            tren += [i[1]]
    if len(tren) != 1:
        print(" No hay ningun tren mas utilizado que los demas")
        menuAdmin()
        return 
    print(" El tren mas utilizado es ",tren)
    print(" Con un total de ",menor)
    menuAdmin()
    return
 

# -------------------------------------------------------------------------------------------------
# Menú de Insertar
# -------------------------------------------------------------------------------------------------

def menuInsertar():
    print("")
    print(" Seleccione el elemento que desea insertar.")
    print("    1) Pais")
    print("    2) Ciudad")
    print("    3) Conexion")
    print("    4) Tipo de Tren")
    print("    5) Ruta")
    print("    6) Tren")
    print("")
    opcion = input(">> ",)
    if not isinstance(eval(opcion),int):
        print(" Por favor digite unicamente el numero que corresponda a la opcion que desea.")
        print(" Intente de nuevo.")
        menuAdmin()
        return
    opcion = eval(opcion)
    if opcion <= 6 and opcion >= 1:
        if opcion == 1:
            insertarPais()
        if opcion == 2:
            insertarCiudad()
        if opcion == 3:
            insertarConexion()
        if opcion == 4:
            insertarTipoTren()
        if opcion == 5:
            insertarRuta()
        if opcion == 6:
            insertarTren()
    else:
         print(" Por favor digite unicamente el numero que corresponda a la opcion que desea.")
         print(" Intente de nuevo.")
         menuAdmin()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Insertar Pais

def insertarPais():
    global paises
    global ultimoPais
    print("Digite la informacion correspondiente: ")
    codigo = input("Nuevo codigo de pais: ",)
    if not isinstance(eval(codigo),int):
        print("Digite un codigo valido")
        print("Intente de nuevo")
        insertarPais()
        return
    codigo = eval(codigo)
    if comprobarPAIS(codigo) == True:
        print("El codigo que digito correponde a otro pais existente.")
        print("Intente de nuevo.")
        insertarPais()
    nombre = input("Nombre del pais: ",)
    paises += [[codigo,nombre]]
    ultimoPais = [paises]
    print("El pais se ha agregado correctamente a la base de datos")
    menuAdmin()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Insertar Ciudad

def insertarCiudad():
    global ciudades
    global ultimaCiudad
    print(" Digite la informacion correspondiente: ")
    codPais = input(" Codigo del pais: ",)
    if not isinstance(eval(codPais),int):
        print(" Digite un codigo valido")
        print(" Intente de nuevo")
        insertarCiudad()
        return
    codPais = eval(codPais)
    if not comprobarPAIS(codPais) == True:
        print(" El codigo que digito no corresponde a ningun pais en nuestra base de datos.")
        print(" Intente de nuevo.")
        insertarCiudad()
    codCiudad = input(" Nuevo codigo de ciudad: ",)
    codCiudad = eval(codCiudad)
    if comprobarCIUDAD(codCiudad) == True:
        print(" El codigo que digito correponde a otra ciudad existente.")
        print(" Intente de nuevo.")
        insertarCiudad()
    nombre = input(" Nombre de la ciudad: ",)
    ciudades += [[codPais,codCiudad,nombre]]
    ultimaCiudad = [codPais,codCiudad,nombre]
    print(" La ciudad se ha agregado correctamente a la base de datos")
    menuAdmin()
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Insertar Conexion

def insertarConexion():
    global conexiones
    global ultimaConexion
    print(" Digite la informacion correspondiente:")
    print("")
    print(" El primer pais y ciudad de la conexion:")
    print("")
    codPais1 = aux_insertarConexion()
    codCiudad1 = aux_insertarConexion2()
    print(" El segundo pais y ciudad de la conexion:")
    print("")
    codPais2 = aux_insertarConexion()
    codCiudad2 = aux_insertarConexion2()
    codConexion = aux_insertarConexion3()
    tiempo = aux_insertarConexion4()
    precio = aux_insertarConexion5()
    
    conexiones += [[codPais1,codPais2,codConexion,codPais2,codCiudad2,tiempo,precio]]
    ultimaConexion = [codPais1,codPais2,codConexion,codPais2,codCiudad2,tiempo,precio]
    print(" Conexion insertada de manera exitosa")
    menuAdmin()
# _auxiliares

def aux_insertarConexion():
    codPais = input(" Codigo del pais: ",)
    codPais = eval(codPais)
    if comprobarPAIS(codPais) == True:
        return codPais
    else:
        print(" El codigo que digito no corresponde a ningun pais en nuestra base de datos.")
        print(" Intente de nuevo.")
        print("")
        aux_insertarConexion()

def aux_insertarConexion2():
    codCiudad = input(" Codigo de la ciudad: ",)
    codCiudad = eval(codCiudad)
    if comprobarCIUDAD(codCiudad) == True:
        return codCiudad
    else:
        print(" El codigo que digito no corresponde a ninguna ciudad en nuestra base de datos.")
        print(" Intente de nuevo.")
        print("")
        aux_insertarConexion2()

def aux_insertarConexion3():
    codConexion = input(" Digite un codigo para su conexion: ",)
    codConexion = eval(codConexion)
    if comprobarCONEXION(codConexion) == True:
        print(" Ese codigo pertenece a otra conexion existente.")
        print(" Intente de nuevo.")
        print("")
        aux_insertarConexion3()
    else:
        return codConexion

def aux_insertarConexion4():
    tiempo = input(" Digite el tiempo de la conexion: ",)
    tiempo = eval(tiempo)
    if not isinstance(tiempo,int):
        print(" Digite unicamente numeros enteros. El tiempo debe mostrarse en horas.")
        print(" Intente de nuevo.")
        print("")
    else:
        return tiempo
    
def aux_insertarConexion5():
    print(" Digite el precio que tendra la conexion")
    precio = input(" >>",)
    try:
        precio = eval(precio)
        return precio
    except:
        print(" Digite un numero natural como precio intente de nuevo")
        aux_insertarConexion5()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Insertar Tipo de Tren

def insertarTipoTren():
    global tipoTren
    global ultimoTipoTren
    global filasTipoTren
    res = []
    print("")
    print(" Digite el codigo del tipo de tren que desea ingresar")
    codigo = input(">> ",)
    for i in tipoTren:
        if i[0] == codigo:
            print(" Codigo ya existente intente de nuevo")
            insertarTipoTren()
            
    print(" Digite el nombre que le pondra al tipo de tren")
    nombre = input(">> ",)
    res = [codigo,nombre]
    ultimoTipoTren = res
    tipoTren += [res]
    filasTipoTren += [[codigo,[]]]
    menuAdmin()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Insertar Ruta

def insertarRuta():
    global rutas
    global trenes
    newRuta = []
    tren = getTren()
    ruta = getRuta()
    print(" Pais y ciudad de salida")
    zona1 = getZona()
    print(" Pais y ciudad de llegada")
    zona2 = getZona()
    precio = getPrecio()
    newRuta += tren
    newRuta += [ruta]
    newRuta += zona1
    newRuta += zona2
    newRuta += [precio]
    rutas += [newRuta]
    for i in trenes:
        if newRuta[0] == i[0]:
            if newRuta[1] == i[1]:
                i[4] += newRuta[2]
    print(" Ruta insertada exitosamente")
    menuAdmin()

#  _auxiliares

def getTren():
    global trenes
    print("")
    print("Digite el codigo del tipo de tren de su ruta")
    tipoDeTren = input("> ",)
    print("Digite el codigo del tren de su ruta")
    tren = input("> ",)
    if not isinstance(eval(tren),int):
        print("El codigo tiene que estar compuesto de numeros enteros")
        print("Intente de nuevo")
        getTren()
    tren = eval(tren) 
    for i in trenes:
        if tipoDeTren == i[0]:
            if tren == i[1]:
                tren = [tipoDeTren,tren]
                return tren
    print("Codigo no existente en la base de datos")
    print("Intente de nuevo")
    getTren()
        
def getRuta():
    global rutas
    print("")
    print("Digite el codigo de ruta que desea ingresar")
    ruta = input("> ",)
    if not isinstance(eval(ruta),int):
        print("El codigo solicitado tiene que ser un numero entero")
        print("Intente de nuevo")
        getRuta()
    ruta = eval(ruta)
    
    for i in rutas:
        if i[2] == ruta:
            print("Codigo ya existente")
            print("Intente de nuevo")
            getRuta
    ruta = ruta
    return ruta

def getZona():
    print("")
    print("Digite el codigo del pais de la ruta")
    pais = input("> ",)
    if not isinstance(eval(pais),int):
        print("El codigo solicitado tiene que ser un numero entero")
        print("Intente de nuevo")
        getZona()
    pais = eval(pais)
    if estaPais(pais) == True:
        print("")
        print("Digite el codigo de la ciudad de la ruta")
        ciudad = input("> ",)
        ciudad = eval(ciudad)
        if not isinstance(pais,int):
            print("El codigo solicitado tiene que ser un numero entero")
            print("Intente de nuevo")
            getZona()
        if estaCiudad(ciudad) == True:
            pais = [pais,ciudad]
            return pais
    print("Informacion no existente en la base de datos")
    print("Intente de nuevo")
    getZona()

def getPrecio():
    print("")
    print("Digite el precio que tendra la ruta")
    precio = input("> ",)
    if isinstance(eval(precio),int):
        precio = eval(precio)
        return precio    
    else:
        print("La informacion solicitada tiene que ser un numero entero")
        print("Intente de nuevo")
        getPrecio()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Insertar Tren

def insertarTren():
    global trenes
    print("Digite la informacion correspondiente.")
    tipo = aux_insertarTren()
    cod = aux_insertarTren2()
    name = aux_insertarTren3()
    asientos = aux_insertarTren4()
    rutas = aux_insertarTren6()
    newTren = [tipo,cod,name,asientos]
    newTren += rutas
    trenes += [newTren]
    menuAdmin()

# _auxiliares

def aux_insertarTren():
    global tipoTren
    print("Digite el numero que corresponda al tipo de tren que desea elegir.")
    for i in tipoTren:
        print(i[0],i[1])
    tipo = input("> ",)
    if comprobarTipoTren(tipo) == True:
        return tipo
    else:
        print("Codigo invalido.")
        print("Intente de nuevo.")
        print("")
        aux_insertarTren()

def aux_insertarTren2():
    global trenes
    print("Digite un codigo nuevo para su tren.")
    cod = input("> ",)
    cod = eval(cod)
    if not comprobarTipoTren(cod) == True:
        return cod
    else:
        print("El codigo digitado corresponde a otro tren existente.")
        print("Intente de nuevo.")
        print("")
        aux_insertarTren2()

def aux_insertarTren3():
    print("Digite un nombre para su tren.")
    name = input("> ",)
    return name

def aux_insertarTren4():
    print("Inserte la cantidad de asientos disponibles en su tren.")
    asientos = input("> ",)
    asientos = eval(asientos)
    if isinstance(asientos,int):
        return asientos
    else:
        print("Digite la informacion como un numero entero.")
        print("Intente de nuevo.")
        print("")
        aux_insertarTren4()

def aux_insertarTren5():
    global rutas
    print("Inserte el codigo de la ruta que desea agregar.")
    codRuta = input("> ",)
    codRuta = eval(codRuta)
    if rutas == []:
        print("No se encuentran rutas disponibles")
    if buscarRutas(codRuta) == True:
        return codRuta
    else:
        print("Digite la informacion como un numero entero.")
        print("Intente de nuevo.")
        print("")
        aux_insertarTren5()
    
def aux_insertarTren6():
    lista = []
    print("¿Desea agregar una posible ruta a su tren?")
    print("Si o No")
    desicion = input("> ",)
    while desicion.upper().strip() == "SI":
        ruta = aux_insertarTren5()
        lista += [ruta] 
        print("¿Desea agregar otra posible ruta a su tren?")
        print("Si o No")
        desicion = input("> ",)
    if desicion.upper().strip() == "NO":
        return lista

# -------------------------------------------------------------------------------------------------
# Menú de Eliminar
# -------------------------------------------------------------------------------------------------

def menuEliminar():
    print("")
    print(" Seleccione el elemento que desea eliminar.")
    print("")
    print("   1) Pais")
    print("   2) Ciudad")
    print("   3) Conexion")
    print("   4) Ruta")
    print("   5) Tren")
    print("")
    opcion = input(">> ",)
    opcion = eval(opcion)
    if not isinstance(opcion,int):
        print("Digite un numero entre 1 al 5")
        print("Intente de nuevo")
        menuAdmin()
        return
    if opcion <= 5 and opcion >= 1:
        if opcion == 1:
            menuElimPais()
        if opcion == 2:
            menuElimCiudad()
        if opcion == 3:
            menuElimConexion()
        if opcion == 4:
            menuElimRuta()
        if opcion == 5:
            menuElimTren()
    else:
         print("Digite un numero entre 1 y 5")
         print("Intente nuevamente")
         menuAdmin()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Eliminar Pais

def menuElimPais():
    print("")
    print("Digite el codigo del pais que desea elmininar")
    codigo = input("> ",)
    codigo = eval(codigo)
    if not isinstance(codigo,int):
        print("Digite un numero entero")
        print("Intente de nuevo")
        menuElimPais()
    else:
        elimPais(codigo)
    return menuAdmin()

def elimPais(codigo):
    global paises
    global eliminados
    global ciudades
    global conexiones
    global rutas
    global usuarios
    newList = []
    contador = 0
    if len(paises) > 0:
        for i in paises:
            if i[0] != codigo:
                newList += [i]
            else:
                contador += 1
        paises = newList
    newList = []
    if len(ciudades) > 0:
        for i in ciudades:
            if i[0] != codigo:
                newList += [i]
        ciudades = newList
    newList = []
    if len(conexiones) > 0:
        for i in conexiones:
            if i[0] != codigo and i[3] != codigo:
                newList += [i]
        conexiones = newList
    newList = []
    if len(rutas) > 0:
        for i in rutas:
            if i[3] != codigo and i[5] != codigo:
                newList += [i]
        rutas = newList
    newList = []
    if len(usuarios) > 0:
        for i in usuarios:
            if i[0] != codigo:
                newList += [i]
        usuarios = newList
    return
    if contador == 0:
        print("Pais no existente en la base de datos")
    else:
        print("Pais eliminado exitosamente")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Eliminar Ciudad

def menuElimCiudad():
    print("")
    print("Digite el codigo de la ciudad que desea elmininar: ")
    codigo = input("> ",)
    codigo = eval(codigo)
    if not isinstance(codigo,int):
        print("Digite un numero entero")
        print("Intente de nuevo")
        menuElimCiudad()
    else:
        elimCiudad(codigo)
    return menuAdmin()

def elimCiudad(codigo):
    global ciudades
    global conexiones
    global rutas
    global usuarios
    tempLista = []
    contador = 0
    for i in ciudades:
        if not i[1] == codigo:
            tempLista += [i]
        else:
            contador += 1
    ciudades = tempLista
    tempLista = []
    for i in conexiones:
        if not i[1] == codigo and not i[4] == codigo:
            tempLista += [i]
    conexiones = tempLista
    tempLista = []
    for i in rutas:
        if i[3] == codigo or i[5] == codigo:
            eliminados += [i]
        else:
            tempLista += [i]
    rutas = tempLista
    tempLista = []
    for i in usuarios:
        if not i[1] == codigo:
            tempLista += [i]
    usuarios = tempLista
    if contador == 0:
        print("Ciudad no existente en la base de datos")
    else:
        print("Ciudad eliminado exitosamente")
        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Eliminar Conexion

def menuElimConexion():
    print("")
    print("Digite el codigo de la conexion que desea elmininar: ")
    codigo = input("> ",)
    codigo = eval(codigo)
    if not isinstance(codigo,int):
        print("Digite un numero entero")
        print("Intente de nuevo")
        menuElimConexion()
    else:
        elimConexion(codigo)
    return menuAdmin()

def elimConexion(codigo):
    global conexiones
    global eliminados
    newList = []
    contador = 0
    for i in conexiones:
        if codigo != i[2]:
            newList +=[i]
        else:
            contador += 1
    if contador == 0:
        print("No existe una conexion con ese codigo")
    else:
        print("Conexion eliminada exitosamente")
    conexiones = newList
    return


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Eliminar Ruta

def menuElimRuta():
    print("")
    print("Digite el codigo del Ruta que desea elmininar")
    codigo = input("> ",)
    codigo = eval(codigo)
    if not isinstance(codigo,int):
        print("Digite un numero entero")
        print("Intente de nuevo")
        menuElimRuta()
    else:
        elimRuta(codigo)
    return menuAdmin()

def elimRuta(codigo):
    global rutas
    global trenes 
    tempLista = []
    contador = 0
    cont = 0
    for i in rutas:
        if i[2] == codigo:
            eliminados += [i]
            cont += 1
        else:
            tempLista += [i]
    rutas = tempLista
    temLista = []
    for i in trenes:
        for j in i:
            ruta = []
            if contador >= 4:
                if i != codigo:
                    ruta += [i]
            else:
                ruta += [i]
            contador += 1
        contador = 0
        temLista += ruta
    trenes = temLista
    if cont == 0:
        print("Ruta no existente en la base de datos")
    else:
        print("Ruta eliminada exitosamente")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Eliminar Tren

def menuElimTren():
    print("")
    print("Digite el codigo del tren que desea elmininar: ")
    codigo = input("> ",)
    codigo = eval(codigo)
    if not isinstance(codigo,int):
        print("Digite un numero entero")
        print("Intente de nuevo")
        menuElimTren()
    else:
        elimTren(codigo)
    return menuAdmin()

def elimTren(codigo):
    global trenes
    global rutas
    global eliminados
    tempListaTrenes = []
    tempListaRutas = []
    contador = 0
    for i in trenes:
        if i[1] == codigo:
            eliminados += [i]
            contador += 1
        else:
            tempListaTrenes += [i]
    for j in rutas:
        if j[1] == codigo:
            eliminados += [j] 
        else:
            tempListaRutas += [j]
    trenes = tempListaTrenes
    rutas = tempListaRutas
    if contador == 0:
        print("Tren no existente en la base de datos")
    else:
        print("Tren eliminado exitosamente")

# -------------------------------------------------------------------------------------------------
# Menú de Modificar
# -------------------------------------------------------------------------------------------------

def menuModificar():
    print("")
    print(" Seleccione el elemento que desea modificar")
    print("   1) Precio de ruta")
    print("   2) Tiempo")
    print("   3) Numero de asientos")
    print("   4) Estado migratorio")
    print("   5) Nombre de Tren")
    opcion = input("> ",)
    opcion = eval(opcion)
    if not isinstance(opcion,int):
        print("Digite un numero entre 1 al 6")
        print("Intente de nuevo")
        menuAdmin()
        return
    if opcion <= 5 and opcion >= 1:
        if opcion == 1:
            modPrecio()
        if opcion == 2:
            modTiempo()
        if opcion == 3:
            modNumAsientos()
        if opcion == 4:
            modEstado()
        if opcion == 5:
            modNombreTren()
    else:
         print("Digite un numero entre 1 y 6")
         print("Intente nuevamente")
         menuModificar()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Modificar Precio (ruta)

def modPrecio():
    global rutas
    print("Modificacion de precios")
    print("")
    print("Digite el codigo de la ruta el cual desea modificar")
    codigo = input("> ",)
    codigo = eval(codigo)
    if not isinstance(codigo,int):
        print("Informacion digitada erronea")
        print("Intente nuevamente")
        modPrecio()
    contador = 0
    for i in rutas:
        if i[2] == codigo:
            contador += 1
            print("Cual sera el nuevo precio de la ruta?")
            precio = input("> ",)
            precio = eval(precio)
            if isinstance(precio,int):
                i[7] = precio
                print("Precio modificado exitosamente")
                menuAdmin()
            else:
                print("Digite un numero entero")
                print("Intente de nuevo")
                modPrecio()
    if contador == 0:
        print("Codigo de ruta no existente en la base de datos")
        print("Intente de nuevo")
        modPrecio()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Modificar Tiempo (conexion)

def modTiempo():
    global conexiones
    print("Digite el codigo correspondiente a la conexion que desea modificar:")
    codConexion = input(">",)
    codConexion = eval(codConexion)
    if comprobarCONEXION(codConexion) != True:
        print("El codigo ingresado no corresponde a nunguna conexion.")
        print("Intente de nuevo.")
        modTiempo()
    else:
        for i in conexiones:
            if i[2] == codConexion:
                print("El tiempo actual para la conexion", i[2], "es", i[5])
                print("Digite el nuevo tiempo en horas.")
                tiempo = input(">",)
                tiempo = eval(tiempo)
                if isinstance(tiempo,int):
                    i[5] = tiempo
                    print("Se ha modificado el tiempo en la conexion ", i[2] ," exitosamente.")
                    print("")
                else:
                    print("Ingrese unicamente numeros enteros.")
                    print("Intente de nuevo.")
                    modTiempo()
    menuAdmin()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Modificar Numero de Asientos Disponibles (tren)

def modNumAsientos():
    global trenes
    print("Digite el codigo correspondiente al tren que desea modificar:")
    codTren = input("> ",)
    codTren = eval(codTren)
    if comprobarTREN(codTren) != True:
        print("El codigo ingresado no corresponde a nungun tren.")
        print("Intente de nuevo.")
        modNumAsientos()
    else:
        for i in trenes:
            if i[1] == codTren:
                print("El numero actual de asientos disponibles para el tren", i[1], "es", i[3])
                print("Digite la nueva cantidad de asientos disponibles.")
                num = input("> ",)
                num = eval(num)
                if isinstance(num,int):
                    i[3] = num
                    print("Se ha modificado el numero de asientos disponibles en el tren ", i[1] ," exitosamente.")
                    print("")
                else:
                    print("Ingrese unicamente numeros enteros.")
                    print("Intente de nuevo.")
                    modNumAsientos()
    menuAdmin()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Modificar Estado Migratorio (usuario)

def modEstado():
    global usuarios
    print("Modificacion de estado Migratorio")
    print("")
    print("Digite el pasaporte del usuario el cual desea modificar")
    codigo = input("> ",)
    codigo = eval(codigo)
    if not isinstance(codigo,int):
        print("Informacion digitada erronea")
        print("Intente nuevamente")
    contador = 0
    for i in usuarios:
        if i[2] == codigo:
            contador += 1
            print("Como desea modificar el estado migratiorio del usuario ",i[3]," ?")
            print("Con problemas: 1")
            print("Disponible: 0")
            estado = input("> ",)
            estado = eval(estado)
            if estado == 1 or estado == 0:
                i[4] = [estado]
                print("Estado modificado exitosamente")
                menuAdmin()
            else:
                print("Digite un numero entre 1 y 0")
                print("Intente de nuevo")
                modEstado()
    if contador == 0:
        print("Pasaporte no existente en la base de datos")
        print("Intente de nuevo")
        modEstado()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Modificar Nombre (tren)

def modNombreTren():
    global trenes
    print("Ingrese la informacion correspondiente:")
    codTren = input("Codigo del tren: ",)
    codTren = eval(codTren)
    if comprobarTREN(codTren) == True:
        for i in trenes:
            if i[1] == codTren:
                print("El nombre actual del tren ", codTren, "es", i[2])
                newName = input("Digite el nuevo nombre para el tren: ",)
                i[2] = newName
                print("El nombre del tren ha sido modificado exitosamente.")
                print("")
                menuAdmin()
    else:
        print("El codigo ingresado no corresponde a ningun tren en nuestra base de datos.")
        print("Intente de nuevo")
        modNombreTren()

# -------------------------------------------------------------------------------------------------
# Venta de Tiquetes
# -------------------------------------------------------------------------------------------------

def menuVentas():
    print("")
    print(" Seleccione: ")
    print(" 1) Abrir Venta de Tiquetes.")
    print(" 2) Venta de Tiquetes.")
    print(" 3) Volver Atras.")
    print("")
    choice = input(">> ",)
    try:
        choice = eval(choice)
    except:
        print(" Ingrese unicamente el numero correspondiente a la opción que desea elegir.")
        print(" Intente de nuevo.")
        menuVentas()
    if choice == 1:
        menuFila()
    if choice == 2:
        menuAtender()
    if choice == 3:
        menuAdmin()
    else:
        print(" Se ha digitado un codigo invalido.")
        print(" Intente de nuevo.")
        menuVentas()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Menu Fila

def menuFila():
    print("")
    print(" ¿Desea ingresar un nuevo usuario a la fila de espera?")
    print(" Si o No")
    print("")
    choice = input(">> ",)
    if choice.upper().strip() == "SI":
        print(" Ingrese la información correspondiente.")
        insertarFila()
    if choice.upper().strip() == "NO":
        menuVentas()
    else:
        print(" Se ha ingresado una respuesta invalida.")
        print(" Intente de nuevo.")
        menuVentas()

def insertarFila():
    global fila
    print("")
    pasaporte = input(" Pasaporte del Usuario: ",)
    try:
        pasaporte = eval(pasaporte)
    except:
        print(" Ingrese unicamente números en este espacio.")
        insertarFila()

    print("")
    tipoTren = input(" Tipo de Tren: ",)
        
    fila += [[pasaporte,tipoTren]]
    
    print(" Usuario agregado exitosamente.")
    print("")
    print(" ¿Desea ingresar otro usuario a la fila?")
    print(" Si o No")
    print("")
    choice = input(">> ",)
    if choice.upper().strip() == "SI":
        insertarFila()
    if choice.upper().strip() == "NO":
        menuVentas()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Menu Atender

def menuAtender():
    global fila
    print("")
    if fila == []:
        print(" No hay nadie en la fila de espera actualmente.")
        print("")
        menuVentas()
    print(" Verificando a ",fila[0])
    verificarPasaporte(fila[0])
    verificarMigracion(fila[0])
    verificarTREN()
    print(" El cliente fue atendido exitosamente.")
    print("")
    fila = fila[1:]
    if fila == []:
        print(" No hay nadie en la fila de espera actualmente.")
        return menuVentas()
    print(" ¿Desea atender al siguiente cliente?")
    print(" Si o No")
    print("")
    choice = input(">> ",)
    if choice.upper().strip() == "SI":
        menuAtender()
    if choice.upper().strip() == "NO":
        menuVentas()
    
    
# verificaciones auxiliares para menuAtender

def verificarPasaporte(usuario):
    global usuarios
    global fila
    if comprobarUSUARIO(usuario[0]) == False:
        print(" Pasaporte inexistente en la base de datos.")
        print(" Creando un nuevo Usuario")
        print("")
        crearUsuario(usuario)
        elemento = fila[0]
        fila = fila[1:]
        fila += [elemento]
        print(" Listo. El usuario ha sido desplazado al final de la fila.")
        menuAtender()


def verificarMigracion(usuario):
    global usuarios
    global fila
    if migracion(usuario[0]) == False:
        print(" Hay un problema con el estado migratorio del usuario.")
        print(" Resolviendo problemas...")
        for i in usuarios:
            if i[2] == usuario[0]:
                i[4] = 0
                fila = fila[1:]
                fila += [usuario]
                print("")
                print(" Listo. El usuario ha sido desplazado al final de la fila.")
                menuAtender()
                return
        return

def verificarTREN():
    global fila
    global TipoTren
    global filasTipoTren
    for i in tipoTren:
        if i[0] == fila[0][1]:
            for i in range(len(filasTipoTren)):
                if fila[0][1] == filasTipoTren[i][0]:
                    filasTipoTren[i][1] += [fila[0][0]]
            return True
    print(" Tipo de tren no existente")
    print(" Digite un codigo de los presentes")
    for i in tipoTren:
        print(i)
    print("")
    corregirTrenUsuario()
    return

def corregirTrenUsuario():
    global fila
    global tipoTren
    codigo = input(" >",)

    fila[0][0] = codigo
    if verificarTREN == True:
        return

def cancelacion():
    global reservaciones
    
    #Pasaporte
    print(" Digite su pasaporte")
    pasaporte = input(" > ",)
    try:
        pasaporte = eval(pasaporte)
    except:
        print(" ")
    pasaporte = cancelPasaporte()

    #Tipo de Tren
    print(" Digite el tipo de tren")
    tipoTren = input(" > ",)

    #Tren
    print(" Digite el codigo del tren")
    tren = input(" > ",)
    try:
        tren = eval(tren)
    except:
        print(" Digite un numero entero como tren")
        print(" Intente de nuevo")
        cancelacion()

    #Ruta
    print(" Digite la Ruta")
    ruta = input(" > ",)
    try:
        ruta = eval(ruta)
    except:
        print(" Digite un numero entero como ruta")
        print(" Intente de nuevo")
        cancelacion()
        
    elim = cancelTipoTren(pasaporte)
    elim = reservaciones[pasaporte][1][elim]
    lista = reservaciones[pasaporte][1]
    res = []
    for i in lista:
        if i != elim:
            res += [i]
    reservaciones[pasaporte][1] = res
    res = []
    return

def cancelPasaporte():
    global reservaciones
    for i in range(len(reservaciones)):
        if reservaciones[i][0] == pasaporte:
            return i

def cancelTipoTren(pasaporte):
    global reservaciones
    for i in range(len(reservaciones[pasaporte][1])):
        if reservaciones[pasaporte][1][i][0] == tipoTren:
            return cancelTren(pasaporte,i)
    print(" No se encuentra ninguna reservacion con esas caracteristicas")
    print(" Intente nuevamente")
    cancelacion()
    
def cancelTren(pasaporte,elim):
    global reservaciones
    if reservaciones[pasaporte][1][elim][1] == tren:
        return cancelRuta(pasaporte,elim)

def cancelRuta(pasaporte,elim):
    global reservaciones
    if reservaciones[pasaporte][1][elim][2] == ruta:
        return i
    




# -------------------------------------------------------------------------------------------------
# Auxiliares comunes
# -------------------------------------------------------------------------------------------------

def trenYRuta(codRuta,codTren):
    global rutas
    global trenes
    for i in rutas:
        if i[2] == codRuta:
            if i[1] == codTren:
                return True
    return False

def migracion(pasaporte):
    global usuarios
    for i in usuarios:
        if i[2] == pasaporte:
            if i[4] == 0:
                return True
            if i[4] == 1:
                return False

def comprobarUSUARIO(codUsuario):
    global usuarios
    for i in usuarios:
        if i[2] == codUsuario:
            return True
    return False

def comprobarPAIS(codigoPais):
    global paises
    for i in paises:
        if i[0]==codigoPais:
            return True
    return False

def comprobarTrenParaRutas(tren):
    global rutas
    for i in rutas:
        if i[1] == tren:
            return True
    return False

def buscarTipoTren(codigo):
    global tipoTren
    for i in tipoTren:
        if i[0] == codigo:
            return True
    return False

def buscarTren(codigo):
    global trenes
    for i in trenes:
        if i[1] == codigo:
            return True
    return False

def comprobarTipoParaTren(tipo):
    global tipoTren
    for i in tipoTren:
        if i[0] == tipo:
            return True

def comprobarCiudad(pais,ciudad):
    global ciudades
    for i in ciudades:
        if i[0]== pais:
            if i[1] == ciudad:
                return True
    return False

def comprobarPaisParaCiudad(pais):
    global ciudades
    for i in ciudades:
        if i[0]==pais:
            return True
    return False

def comprobarCiudadEnPais(codPais,codCiudad):
    global ciudades
    for i in ciudades:
        if i[1] == codCiudad and i[0] == codPais:
            return True

def comprobarCIUDAD(codigoCiudad):
    global ciudades
    for i in ciudades:
        if i[1] == codigoCiudad:
            return True

def estaPais(codigo):
    global paises
    for i in paises:
        if i[0] == codigo:
            return True
    return False

def estaCiudad(codigo):
    global ciudades
    for i in ciudades:
        if i[1] == codigo:
            return True
    return False

def comprobarTipoTren(codTipoTren):
    global tipoTren
    for i in tipoTren:
        if i[0] == codTipoTren:
            return True

def comprobarCONEXION(codConexion):
    global conexiones
    for i in conexiones:
        if i[2] == codConexion:
            return True

def comprobarTREN(codTren):
    global trenes
    for i in trenes:
        if i[1] == codTren:
            return True
    return False

def comprobarCONEXIONciudad(a,b):
    global conexiones
    for i in conexiones:
        if (i[1] == a and i[4] == b)or(i[1] == b and i[4] == a):
            return True
    return False

def comprobarCONEXIONpais(a,b):
    global conexiones
    for i in conexiones:
        if (i[0] == a and i[3] == b)or(i[0] == b and i[3] == a):
            return True
    return False

def buscarTren_aux(codigo,lista):
    for i in lista:
        if i[1] == codigo:
            return True
    return False

def buscarRutas(codigo):
    global rutas
    for i in rutas:
        if i[2] == codigo:
            return True
    return False

def estaTipoTren(elem,lista):
    for i in lista:
        if elem[0] == i[0]:
            return True
    return False

def estaRutaInReservaciones(ruta):
    global reservaciones
    contador = 0
    for i in reservaciones:
        for j in i[1]:
            if j[2] == ruta:
                contador += 1
    return contador

def estaTrenEnFacturas(tren):
    global facturas
    res = 0
    for i in facturas:
        for j in i[1]:
            if j[1] == tren:
                res += 1
    return res

comprobarInformacion()


