# -*- coding: utf-8 -*-

import sqlite3 as clientes
from gi.repository import Gtk

settings = Gtk.Settings.get_default()
settings.props.gtk_button_images = True
class Clientes:
    """É a clase principal que executa todo o programa"""

    # Créase aceso a ventá de Glade
    archivoVentanaPrincipal = "VentanaPrincipal.glade"
    archivoVentanaConsulta = "ConsultaClientes.glade"
    archivoVentanaIntroducir = "CrearCliente.glade"
    archivoVentanaEliminar = "EliminarCliente.glade"

    archivoVentanaArticuloEliminado = "VentanaArticuloEliminado.glade"

    # Créanse constructores de GTK para as interfaces
    builderVentanaPrincipal = Gtk.Builder()
    builderVentanaConsulta = Gtk.Builder()
    builderVentanaIntroducir = Gtk.Builder()
    builderVentanaEliminar = Gtk.Builder()
    builderVentanaArticuloEliminado = Gtk.Builder()

    # Añádense os archivos os constructores da interface
    builderVentanaPrincipal.add_from_file(archivoVentanaPrincipal)
    builderVentanaConsulta.add_from_file(archivoVentanaConsulta)
    builderVentanaIntroducir.add_from_file(archivoVentanaIntroducir)
    builderVentanaEliminar.add_from_file(archivoVentanaEliminar)

    # Recóllense as ventás contedoras
    ventanaEntrada = builderVentanaPrincipal.get_object("VentanaPrincipal")
    ventanaConsultas = builderVentanaConsulta.get_object("VentanaConsulta")
    ventanaIntroducir = builderVentanaIntroducir.get_object("VentanaIntroducir")
    ventanaEliminar = builderVentanaEliminar.get_object("VentanaEliminar")

    ventanaEntrada.show_all()

    # Conéctase a base de datos e créase un cursor para recollela
    bd = clientes.connect("clientes.dat")
    print(bd)
    cursor = bd.cursor()


    def al_buscar(self, busqueda):
        """Funcións de búsqueda e modificación:"""
        self.cajaNombreConsultar.set_text("")
        self.cajaPrecioConsultar.set_text("")
        self.cajaNumeroConsultar.set_text("")
        self.cajaApellidosConsultar.set_text("")


        # Recolle a mensaxe da caixa de texto
        hora = self.cajaHoraConsultacion.get_text()
        # Búsqueda do código recollido na base de datos
        self.cursor.execute("Select * from clientes where Hora='"+hora+"'")
        # Recorreremos o cursor e mostraremos por pantalla si existe
        for cliente in self.cursor:
         self.cajaNombreConsultar.set_text(str(cliente[1]))
         self.cajaPrecioConsultar.set_text(str(cliente[4]))
         self.cajaTratamientoConsultar.set_text(str(cliente[6]))
         self.cajaNumeroConsultar.set_text(str(cliente[7]))
         self.cajaPeluqueroConsultar.set_text(str(cliente[5]))
         self.cajaApellidosConsultar.set_text(str(cliente[2]))


    def introducirStock(self, introducir):
        """Función de introdución de datos"""
        nombre = self.cajaIntroducirNombre.get_text().upper()
        apellidos = self.cajaIntroducirApellidos.get_text().upper()
        hora = self.boxIntroducirHora.get_active_text()
        precio = self.cajaIntroducirPrecio.get_text().upper()
        peluquero = self.comboPeluquero.get_active_text()
        numero = self.cajaIntroducirNumero.get_text().upper()
        dni = self.cajaIntroducirDni.get_text().upper()
        tratamiento=self.comboTratamiento.get_active_text()
        self.limpiarIntroducir(self)

        self.cursor.execute("select nombre from clientes")
        # Recóllense os códigos dos produtos para despois descartar se está ou no na base
        codigos = self.cursor.fetchall()
        existe=False
        for producto in codigos:

            idCompare = str(producto)
            # Se xa hai un na base "existe" pasa a True e non se añadirá a base
            if idCompare[2:4]==nombre:
                print("Hora de inserccion repetida")

                existe=True

        if existe==False:
            # Introdúcense valores na tabla
            self.cursor.execute("insert into clientes values('" + dni + "','" + nombre + "','" + apellidos + "','" + hora + "','" + precio + "','"+peluquero+"','" + tratamiento + "','" + numero+ "')")
            print(" Cliente Insertado")
            self.bd.commit()

        existe=False


    def al_modificar(self, modificacion):
        """Definición de variables de texto que recollen o texto das caixas"""
        nombre = self.cajaNombreConsultar.get_text().upper()
        precio = self.cajaPrecioConsultar.get_text().upper()

        tratamiento = self.cajaTratamientoConsultar.get_text()
        peluquero = self.cajaPeluqueroConsultar.get_text().upper()
        apellidos = self.cajaApellidosConsultar.get_text().upper()
        hora = self.cajaHoraConsultacion.get_text().upper()
        numero = self.cajaNumeroConsultar.get_text().upper()
        self.cursor.execute(
            "update clientes set Nombre='" + nombre + "',Apellidos='" + apellidos + "',Hora='" + hora + "',Precio='" + peluquero +"',Peluquero='" + peluquero +"'"+" where Hora='" + hora + "'")




        print("Cliente Modificado")
        self.bd.commit()
        # Borrado das caixas xa usadas
        self.cajaNombreConsultar.set_text("")
        self.cajaPrecioConsultar.set_text("")
        self.cajaTratamientoConsultar.set_text("")
        self.cajaNumeroConsultar.set_text("")
        self.cajaApellidosConsultar.set_text("")
        self.cajaPeluqueroConsultar.set_text("")


    def Eliminar(self, eliminado):
        """Recolle o código e borra os datos pasando como parámetro a hora"""
        cajaEliminar = self.cajaEliminar.get_text()
        self.cursor.execute("delete from clientes where Hora ='" + cajaEliminar + "'")
        print("Cliente Borrado")
        self.bd.commit()
        # Borra a caixa de "eliminar"
        self.cajaEliminar.set_text("")


    def click_limpiarConsulta(self,limpieza):
        """Limpeza das caixas de texto en consultas"""
        self.cajaHoraConsultacion.set_text("")
        self.cajaNombreConsultar.set_text("")
        self.cajaPrecioConsultar.set_text("")
        self.cajaTratamientoConsultar.set_text("")
        self.cajaPeluqueroConsultar.set_text("")
        self.cajaApellidosConsultar.set_text("")
        self.cajaNumeroConsultar.set_text("")




    def limpiarIntroducir(self, introduccion):
        """Limpeza das caixas de texto en introducir"""
        self.cajaIntroducirNombre.set_text("")
        self.cajaIntroducirApellidos.set_text("")
        self.cajaIntroducirPrecio.set_text("")
        self.cajaIntroducirDni.set_text("")
        self.cajaIntroducirNumero.set_text("")


    def click_introducir(self, entrada):
        """Mostra e oculta a ventá de introducir"""
        self.ventanaEntrada.hide()
        self.ventanaIntroducir.show_all()


    def click_consultar(self, consulta):
        """Mostra e oculta a ventá de consultar"""
        self.ventanaEntrada.hide()
        self.ventanaConsultas.show_all()


    def Eliminar_articulo(self,eliminado):
        """Mostra e oculta a ventá de eliminar"""
        self.ventanaEntrada.hide()
        self.ventanaEliminar.show_all()


    def click_volverConsulta(self, vuelta):
        """Devólvete a ventá principal"""
        self.click_limpiarConsulta(self)
        self.ventanaConsultas.hide()
        self.ventanaEntrada.show_all()


    def volverIntroducir(self, vuelta):
        """Devólvete a ventá introducir"""
        self.limpiarIntroducir(self)
        self.ventanaIntroducir.hide()
        self.ventanaEntrada.show_all()


    def volverEliminar(self, vuelta):
        """Devólvete a ventá eliminar"""
        self.cajaEliminar.set_text("")
        self.ventanaEliminar.hide()
        self.ventanaEntrada.show_all()


    def __init__(self):
        """Declaración inicial de "handlers" e entrada da ventá Principal o iniciar o programa"""
        # Mostramos a ventá principal
        self.ventanaEntrada.show_all();
        # Manejadores; Funcións definidas en Glade ca súa equivalencia en Python
        manejadores = {
                  "click_limpiarConsulta":self.click_limpiarConsulta,
                  "click_volverConsulta":self.click_volverConsulta,
                  "limpiarCamposIntroducir":self.limpiarIntroducir,
                  "click_introducirStock":self.introducirStock,
                  "Eliminar_articulo":self.Eliminar_articulo,
                  "click_introducir": self.click_introducir,
                  "volverIntroducir":self.volverIntroducir,
                  "click_consultar": self.click_consultar,
                  "volverEliminar":self.volverEliminar,
                  "click_modificar":self.al_modificar,


                  "al_buscar":self.al_buscar,
                  "Terminar1":self.Terminar,
                  "Terminar2":self.Terminar,
                  "Terminar3":self.Terminar,
                  "Terminar":self.Terminar,
                  "Eliminar":self.Eliminar,

        }
        # Conéctanse os constructores cos manejadores
        self.builderVentanaPrincipal.connect_signals(manejadores)
        self.builderVentanaConsulta.connect_signals(manejadores)
        self.builderVentanaIntroducir.connect_signals(manejadores)
        self.builderVentanaEliminar.connect_signals(manejadores)

        self.builderVentanaArticuloEliminado.connect_signals(manejadores)

        # Recollense a caixas das ventás
        self.cajaHoraConsultacion = self.builderVentanaConsulta.get_object("cajaHoraConsultacion")

        self.cajaNombreConsultar = self.builderVentanaConsulta.get_object("cajaNombreConsultar")
        self.consolaVenta = self.builderVentanaConsulta.get_object("LConsola")
        self.cajaDniConsultar=self.builderVentanaConsulta.get_object("cajaDniConsultar")
        self.cajaPrecioConsultar = self.builderVentanaConsulta.get_object("cajaPrecioConsultar")
        self.cajaNumeroConsultar = self.builderVentanaConsulta.get_object("cajaNumeroConsultar")
        self.cajaApellidosConsultar = self.builderVentanaConsulta.get_object("cajaApellidosConsultar")
        self.cajaPeluqueroConsultar = self.builderVentanaConsulta.get_object("cajaPeluqueroConsultar")
        self.cajaTratamientoConsultar = self.builderVentanaConsulta.get_object("cajaTratamientoConsultar")
        self.cajaIntroducirNombre = self.builderVentanaIntroducir.get_object("cajaIntroducirNombre")
        self.cajaIntroducirDni = self.builderVentanaIntroducir.get_object("cajaIntroducirDni")
        self.cajaIntroducirNumero = self.builderVentanaIntroducir.get_object("cajaIntroducirNumero")
        self.cajaIntroducirApellidos = self.builderVentanaIntroducir.get_object("cajaIntroducirApellidos")
        self.boxIntroducirHora = self.builderVentanaIntroducir.get_object("boxIntroducirHora")
        self.comboPeluquero = self.builderVentanaIntroducir.get_object("comboPeluquero")
        self.comboTratamiento=self.builderVentanaIntroducir.get_object("comboTratamiento")
        self.cajaIntroducirPrecio = self.builderVentanaIntroducir.get_object("cajaIntroducirPrecio")
        self.cajaEliminar = self.builderVentanaEliminar.get_object("cajaEliminar")




    def Terminar(self, dos, tres):
        """Cierre do programa"""
        self.ventanaEntrada.connect("delete-event", Gtk.main_quit)
        self.ventanaIntroducir.connect("delete-event", Gtk.main_quit)
        self.ventanaEliminar.connect("delete-event", Gtk.main_quit)
        self.ventanaConsultas.connect("delete-event", Gtk.main_quit)
        Gtk.main_quit()


Clientes()
Gtk.main()
