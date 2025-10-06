import customtkinter as ctk
import secrets
import string
import math
import pyperclip

# --- DEFINICIÓN DE CONSTANTES Y CONJUNTOS DE CARACTERES ---
# Colores del tema
COLOR_FONDO = "#1C1C1C"      
COLOR_VERDE = "#00A878"     
COLOR_BLANCO = "#F0F0F0"
COLOR_NEGRO = "#000000"
COLOR_ROJO = "#D90429"
COLOR_NARANJA = "#F77F00"
COLOR_AMARILLO = "#FCBF49"
COLOR_AZUL = "#00B4D8"

# Conjuntos de caracteres
CARACTERES = {
    "latin": string.ascii_letters,
    "numeros": string.digits,
    "puntuacion": ".,;:!?¿¡'\"()[]{}<>",
    "especiales": "@#~$%&/()=+\\*-_|°¬",
    "cirilico": "АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя"
}

# --- CLASE DE LA VENTANA DE SELECCIÓN DE CARACTERES ---
class VentanaSeleccion(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master # Referencia a la ventana principal
        
        self.title("Seleccionar Caracteres")
        self.geometry("350x300")
        self.transient(master) # Mantener esta ventana por encima de la principal
        self.grab_set() # Bloquear interacciones con la ventana principal
        self.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
        self.configure(fg_color=COLOR_FONDO)

        self.opciones = {}
        
        etiqueta_titulo = ctk.CTkLabel(self, text="Incluir Caracteres", font=("Arial", 16, "bold"), text_color=COLOR_BLANCO)
        etiqueta_titulo.pack(pady=10)

        # Crear checkboxes para cada tipo de caracter
        opciones_disponibles = {
            "latin": "Mayúsculas y Minúsculas (Latin)",
            "numeros": "Números",
            "puntuacion": "Signos de Puntuación",
            "especiales": "Caracteres Especiales",
            "cirilico": "Cilírico (Ruso)"
        }

        for clave, texto in opciones_disponibles.items():
            self.opciones[clave] = ctk.BooleanVar(value=True) # Por defecto, todos seleccionados
            check = ctk.CTkCheckBox(
                self,
                text=texto,
                variable=self.opciones[clave],
                font=("Arial", 12),
                fg_color=COLOR_VERDE,
                hover_color=COLOR_VERDE,
                text_color=COLOR_BLANCO,
                checkmark_color=COLOR_NEGRO,
                border_color=COLOR_BLANCO 
            )
            check.pack(anchor="w", padx=20, pady=5)
            
        boton_aceptar = ctk.CTkButton(
            self,
            text="Aceptar",
            command=self.aplicar_y_cerrar,
            fg_color=COLOR_VERDE,
            text_color=COLOR_NEGRO,
            hover_color="#008760" 
        )
        boton_aceptar.pack(pady=20)

    def aplicar_y_cerrar(self):
        self.master.actualizar_juego_caracteres()
        self.destroy()

    def cerrar_ventana(self):
        self.destroy()


# --- CLASE PRINCIPAL DE LA APLICACIÓN ---
class GeneradorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURACIÓN DE LA VENTANA PRINCIPAL ---
        self.title("Generador de Contraseñas Seguras")
        self.geometry("450x400")
        self.configure(fg_color=COLOR_FONDO)
        self.resizable(False, False)

        self.juego_caracteres_seleccionado = "".join(CARACTERES.values()) 
        self.ventana_seleccion = None
        

        # 1. Selector de Longitud
        frame_longitud = ctk.CTkFrame(self, fg_color="transparent")
        frame_longitud.pack(pady=10, padx=20, fill="x")

        etiqueta_longitud = ctk.CTkLabel(frame_longitud, text="Longitud:", font=("Arial", 14), text_color=COLOR_BLANCO)
        etiqueta_longitud.pack(side="left")

        opciones_longitud = [str(i) for i in range(8, 129, 4)]
        self.variable_longitud = ctk.StringVar(value="16")
        menu_longitud = ctk.CTkOptionMenu(
            frame_longitud,
            values=opciones_longitud,
            variable=self.variable_longitud,
            fg_color=COLOR_VERDE,
            button_color=COLOR_VERDE,
            button_hover_color="#008760",
            text_color=COLOR_NEGRO,
            dropdown_fg_color=COLOR_VERDE,
            dropdown_hover_color="#008760",
            dropdown_text_color=COLOR_NEGRO
        )
        menu_longitud.pack(side="right")
        
        # 2. Botón de Selección de Caracteres
        boton_seleccionar_chars = ctk.CTkButton(
            self,
            text="Seleccionar Tipos de Caracteres",
            command=self.abrir_ventana_caracteres,
            fg_color=COLOR_VERDE,
            text_color=COLOR_NEGRO,
            hover_color="#008760"
        )
        boton_seleccionar_chars.pack(pady=5, padx=20, fill="x")

        # 3. Campo de Salida de la Contraseña
        frame_salida = ctk.CTkFrame(self, fg_color=COLOR_FONDO, border_width=2, border_color=COLOR_VERDE)
        frame_salida.pack(pady=10, padx=20, fill="x", ipady=5)
        
        self.etiqueta_contrasena = ctk.CTkLabel(frame_salida, text="...", font=("Courier", 18, "bold"), text_color=COLOR_BLANCO)
        self.etiqueta_contrasena.pack(pady=10)

        # 4. Barra de Fortaleza
        self.barra_fortaleza = ctk.CTkProgressBar(self, progress_color=COLOR_VERDE)
        self.barra_fortaleza.set(0)
        self.barra_fortaleza.pack(pady=5, padx=20, fill="x")
        
        self.etiqueta_fortaleza = ctk.CTkLabel(self, text="Fortaleza", font=("Arial", 12), text_color=COLOR_BLANCO)
        self.etiqueta_fortaleza.pack(pady=2)

        # 5. Botones de Acción
        frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        frame_botones.pack(pady=20, padx=20, fill="x")
        frame_botones.columnconfigure((0,1), weight=1)

        boton_generar = ctk.CTkButton(
            frame_botones,
            text="Generar",
            command=self.generar_contrasena,
            font=("Arial", 14, "bold"),
            fg_color=COLOR_VERDE,
            text_color=COLOR_NEGRO,
            hover_color="#008760"
        )
        boton_generar.grid(row=0, column=0, padx=5, sticky="ew")

        self.boton_copiar = ctk.CTkButton(
            frame_botones,
            text="Copiar",
            command=self.copiar_al_portapapeles,
            font=("Arial", 14, "bold"),
            fg_color=COLOR_VERDE,
            text_color=COLOR_NEGRO,
            hover_color="#008760"
        )
        self.boton_copiar.grid(row=0, column=1, padx=5, sticky="ew")
        
        self.etiqueta_copiado = ctk.CTkLabel(self, text="", font=("Arial", 12), text_color=COLOR_VERDE)
        self.etiqueta_copiado.pack()
        
        # Generar una contraseña al iniciar
        self.generar_contrasena()

    # --- LÓGICA ---
    def abrir_ventana_caracteres(self):
        if self.ventana_seleccion is None or not self.ventana_seleccion.winfo_exists():
            self.ventana_seleccion = VentanaSeleccion(self)
        self.ventana_seleccion.focus()

    def actualizar_juego_caracteres(self):
        self.juego_caracteres_seleccionado = ""
        for clave, variable in self.ventana_seleccion.opciones.items():
            if variable.get():
                self.juego_caracteres_seleccionado += CARACTERES[clave]
        # Si el usuario desmarca todo, usar un conjunto por defecto para evitar errores
        if not self.juego_caracteres_seleccionado:
            self.juego_caracteres_seleccionado = CARACTERES["latin"] + CARACTERES["numeros"]

    def generar_contrasena(self):
        try:
            longitud = int(self.variable_longitud.get())
            contrasena = "".join(secrets.choice(self.juego_caracteres_seleccionado) for _ in range(longitud))
            self.etiqueta_contrasena.configure(text=contrasena)
            self.calcular_y_mostrar_fortaleza(contrasena)
        except IndexError:
            self.etiqueta_contrasena.configure(text="Error: Selecciona caracteres")
            self.barra_fortaleza.set(0)
            self.etiqueta_fortaleza.configure(text="Fortaleza", text_color=COLOR_BLANCO)
        
        # Resetear el mensaje de "copiado"
        self.etiqueta_copiado.configure(text="")

    def calcular_y_mostrar_fortaleza(self, contrasena):
        longitud = len(contrasena)
        tamano_pool = len(self.juego_caracteres_seleccionado)

        if tamano_pool > 1: 
            entropia = longitud * math.log2(tamano_pool)
        else:
            entropia = 0
            
        # Mapeo de entropía a progreso y color
        if entropia < 40:
            progreso = 0.15
            color = COLOR_ROJO
            texto = "Muy Débil"
        elif entropia < 60:
            progreso = 0.35
            color = COLOR_NARANJA
            texto = "Débil"
        elif entropia < 80:
            progreso = 0.55
            color = COLOR_AMARILLO
            texto = "Moderada"
        elif entropia < 120:
            progreso = 0.80
            color = COLOR_VERDE
            texto = "Fuerte"
        else:
            progreso = 1.0
            color = COLOR_AZUL
            texto = "Muy Fuerte"
            
        self.barra_fortaleza.configure(progress_color=color)
        self.barra_fortaleza.set(progreso)
        self.etiqueta_fortaleza.configure(text=texto, text_color=color)


    def copiar_al_portapapeles(self):
        contrasena = self.etiqueta_contrasena.cget("text")
        if contrasena and "..." not in contrasena and "Error" not in contrasena:
            pyperclip.copy(contrasena)
            self.etiqueta_copiado.configure(text="¡Contraseña copiada al portapapeles!")
            self.after(2000, lambda: self.etiqueta_copiado.configure(text="")) # Borrar mensaje después de 2 seg

# --- EJECUTA LA APP ---
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = GeneradorApp()
    app.mainloop()