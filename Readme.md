# 🔐 Generador de Contraseñas Seguras 🔐

Este proyecto es una aplicación de escritorio moderna y segura, construida en **Python**, diseñada para crear contraseñas robustas y personalizadas con una interfaz gráfica intuitiva.

> La seguridad no es un producto, sino un proceso. Esta herramienta te ayuda en ese proceso, dándote el control total sobre la creación de tus contraseñas.

---

## ✨ Características Principales

- **Interfaz Gráfica Moderna**: Construida con `customtkinter`, ofrece un tema oscuro y elegante que es agradable a la vista y fácil de usar.
- **Alta Personalización**: Permite un control granular sobre:
  - **Longitud**: Desde `8` hasta `128` caracteres.
  - **Juego de Caracteres**: Selección múltiple de `Mayúsculas`, `Minúsculas`, `Números`, `Símbolos` y hasta caracteres `Cilíricos`.
- **Seguridad Criptográfica**: Utiliza el módulo `secrets` de Python, asegurando que cada contraseña sea generada con un alto grado de aleatoriedad, haciéndola impredecible y segura contra ataques de fuerza bruta.
- **Indicador de Fortaleza Visual**: Una barra de progreso coloreada muestra instantáneamente la robustez de la contraseña generada, basada en su entropía en bits.
- **Funcionalidad "Copiar con un Clic"**: Un botón para copiar la contraseña directamente al portapapeles, evitando la selección manual y mejorando la seguridad.

---

## 🚀 ¿Cómo Funciona el Código?

El programa se estructura en dos clases principales para separar la lógica de la interfaz.

### 1. `GeneradorApp` (La Ventana Principal)

Esta es la clase que orquesta toda la aplicación.

```python
class GeneradorApp(ctk.CTk):
    def __init__(self):
        # Configura la ventana, los botones y los menús.
        ...
    
    def generar_contrasena(self):
        # Es el corazón de la app. Llama al módulo 'secrets'.
        contrasena = "".join(secrets.choice(self.juego_caracteres_seleccionado) for _ in range(longitud))
        ...

    def calcular_y_mostrar_fortaleza(self, contrasena):
        # Mide la entropía y actualiza la barra de colores.
        entropia = len(contrasena) * math.log2(len(self.juego_caracteres_seleccionado))
        ...
```

| Método                      | Descripción                                                                 |
| --------------------------- | --------------------------------------------------------------------------- |
| `__init__`                  | **Constructor**: Inicializa todos los componentes visuales.                 |
| `generar_contrasena`        | **Lógica Central**: Crea la contraseña usando los parámetros del usuario.   |
| `calcular_y_mostrar_fortaleza` | **Feedback Visual**: Calcula la entropía y colorea la barra de seguridad. |
| `copiar_al_portapapeles`    | **Utilidad**: Copia la contraseña generada al portapapeles del sistema.     |

### 2. `VentanaSeleccion` (La Ventana Emergente)

Una ventana secundaria que permite al usuario elegir qué tipos de caracteres desea incluir.

```python
class VentanaSeleccion(ctk.CTkToplevel):
    def __init__(self, master):
        # Crea una ventana con checkboxes para cada tipo de caracter.
        ...
    
    def aplicar_y_cerrar(self):
        # Comunica la selección a la ventana principal.
        self.master.actualizar_juego_caracteres()
        self.destroy()
```

---

## 🎨 Paleta de Colores y Diseño

El diseño de la aplicación sigue una paleta de colores específica para lograr una estética coherente y moderna.

| Elemento            | Color Hex   | Color                               |
| ------------------- | ----------- | ----------------------------------- |
| Fondo Principal     | `#1C1C1C`   | ![#1C1C1C](https://placehold.co/15x15/1C1C1C/1C1C1C.png) Negro Intenso |
| Acentos y Botones   | `#00A878`   | ![#00A878](https://placehold.co/15x15/00A878/00A878.png) Verde Moderno  |
| Texto Principal     | `#F0F0F0`   | ![#F0F0F0](https://placehold.co/15x15/F0F0F0/F0F0F0.png) Blanco Suave   |
| Fortaleza (Débil)   | `#D90429`   | ![#D90429](https://placehold.co/15x15/D90429/D90429.png) Rojo Alerta    |
| Fortaleza (Fuerte)  | `#00B4D8`   | ![#00B4D8](https://placehold.co/15x15/00B4D8/00B4D8.png) Azul Eléctrico |

---

## 🛠️ Tecnologías Utilizadas

- **Python 3**: El lenguaje de programación principal.
- **CustomTkinter**: Para la creación de la interfaz gráfica moderna.
- **secrets**: Para la generación segura de números y caracteres aleatorios.
- **pyperclip**: Para la funcionalidad de copiado al portapapeles multiplataforma.

¡Este generador no solo crea contraseñas, sino que te educa visualmente sobre su fortaleza, dándote las herramientas para mejorar tu seguridad digital!