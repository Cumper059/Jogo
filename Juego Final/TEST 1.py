import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Papers, Please Inspired Game")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Cargar imágenes
logo_image = pygame.image.load("logo.png")  # Asegúrate de tener el archivo 'logo.png'
logo_image = pygame.transform.scale(logo_image, (WIDTH, HEIGHT))  # Escalar imagen del logo

# Imágenes de introducción
inicio_image = pygame.image.load("image-inicio.png")
inicio_image = pygame.transform.scale(inicio_image, (WIDTH, HEIGHT))

inter_image = pygame.image.load("image-inter.png")
inter_image = pygame.transform.scale(inter_image, (WIDTH, HEIGHT))

final_image = pygame.image.load("image-final.png")
final_image = pygame.transform.scale(final_image, (WIDTH, HEIGHT))

# Fondos y finales
fondo_image = pygame.image.load("fondo.png")
fondo_image = pygame.transform.scale(fondo_image, (WIDTH, HEIGHT))

final_bueno_image = pygame.image.load("final-bueno.png")
final_bueno_image = pygame.transform.scale(final_bueno_image, (WIDTH, HEIGHT))

final_normal_image = pygame.image.load("final-normal.png")
final_normal_image = pygame.transform.scale(final_normal_image, (WIDTH, HEIGHT))

final_malo_image = pygame.image.load("final-malo.png")
final_malo_image = pygame.transform.scale(final_malo_image, (WIDTH, HEIGHT))

# Fuente para el texto
font = pygame.font.Font(None, 36)

# Música de fondo
pygame.mixer.music.load("audio.mp3")  # Asegúrate de tener el archivo 'audio.mp3'
pygame.mixer.music.play(-1)  # Reproducir en bucle

# Variables de estado del juego
problem_variations = [
    [("¿Cuánto es 2 + 2?", "4"), ("¿Cuánto es 2 + 1?", "3"), ("¿Cuánto es 2 + 3?", "5")],
    [("¿Cuánto es 3 + 3?", "6"), ("¿Cuánto es 3 + 2?", "5"), ("¿Cuánto es 3 + 1?", "4")],
    [("¿Cuánto es 1 + 1?", "2"), ("¿Cuánto es 1 + 2?", "3"), ("¿Cuánto es 1 + 3?", "4")]
]

problems = [random.choice(variation) for variation in problem_variations]

current_problem_index = 0
answer = ""
correct_count = 0
show_result = False
show_intro = False
show_logo = True
show_menu = False
show_end_menu = False
show_context_intro = False
context_screen_index = 0  # Control de las pantallas de contexto

# Control de tiempo para la animación
logo_start_time = pygame.time.get_ticks()  # Tiempo de inicio de la animación del logo
fade_duration = 3000  # Duración del fade-in y fade-out en milisegundos
fade_in = True  # Control de la dirección del fade
alpha = 0  # Valor de alpha (opacidad)

# Función para dibujar texto centralizado en la parte inferior (solo para diálogos y finales)
def draw_centered_text_bottom(text, y_offset=50):
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - y_offset))
    screen.blit(text_surface, text_rect)

# Función para dibujar la interfaz
def draw_interface():
    global show_logo, show_menu, show_end_menu, fade_in, alpha, logo_start_time  # Asegúrate de declarar aquí las variables globales

    screen.fill(BLACK)  # Fondo negro para todo el texto

    if show_logo:
        # Calcular el tiempo transcurrido
        elapsed_time = pygame.time.get_ticks() - logo_start_time

        # Determinar la fase de la animación
        if fade_in:
            alpha = min(255, (elapsed_time / fade_duration) * 255)  # Fade-in
        else:
            alpha = max(0, 255 - ((elapsed_time - fade_duration) / fade_duration) * 255)  # Fade-out

        # Aplicar el alpha a la imagen del logo
        logo_image.set_alpha(alpha)
        screen.blit(logo_image, (0, 0))

        # Comprobar si la fase de fade-in ha terminado
        if fade_in and elapsed_time >= fade_duration:
            fade_in = False  # Cambiar a fade-out
            logo_start_time = pygame.time.get_ticks()  # Reiniciar el tiempo para fade-out

        # Comprobar si la fase de fade-out ha terminado
        if not fade_in and elapsed_time >= fade_duration * 2:
            show_logo = False
            show_menu = True

    elif show_menu:
        # Menú de inicio
        draw_centered_text_bottom("Bienvenido al Juego", 300)  # Posición en Y para el título
        draw_centered_text_bottom("1. Iniciar", 250)  # Posición en Y para la opción 1
        draw_centered_text_bottom("2. Salir", 200)  # Posición en Y para la opción 2

    elif show_intro:
        # Introducción
        draw_centered_text_bottom("Te matriculaste a la universidad y ya tienes exámenes que tienes que aprobar", 300)
        draw_centered_text_bottom("Presiona Enter para empezar", 250)

    elif not show_result:
        # Fondo negro con el fondo de los problemas
        screen.blit(fondo_image, (0, 0))

        # Dibuja un documento simple
        pygame.draw.rect(screen, GRAY, (100, 100, 600, 400))  # Documento
        pygame.draw.rect(screen, BLACK, (100, 100, 600, 400), 2)  # Borde del documento

        # Texto en el documento
        question, _ = problems[current_problem_index]
        draw_centered_text_bottom(question, 250)  # Texto de la pregunta centrado en la parte inferior

        # Mostrar la respuesta del usuario
        draw_centered_text_bottom("Respuesta: " + answer, 200)  # Texto de respuesta centrado en la parte inferior

    elif show_end_menu:
        # Menú de final
        draw_centered_text_bottom("1. Reiniciar", 250)  # Posición en Y para la opción 1
        draw_centered_text_bottom("2. Salir", 200)  # Posición en Y para la opción 2

    else:
        # Mostrar la imagen del final adecuado
        if correct_count == len(problems):
            screen.blit(final_bueno_image, (0, 0))  # Mostrar imagen de final bueno
            draw_centered_text_bottom("¡Felicitaciones! Ganaste el título de la universidad", 250)
        elif correct_count >= 1:
            screen.blit(final_normal_image, (0, 0))  # Mostrar imagen de final normal
            draw_centered_text_bottom("Lo hiciste bien, ¡pero todavía hay mucho por mejorar!", 250)
        else:
            screen.blit(final_malo_image, (0, 0))  # Mostrar imagen de final malo
            draw_centered_text_bottom("No pasaste los exámenes, inténtalo de nuevo.", 250)

        # Después de mostrar el resultado, habilitar el menú de fin de juego
        pygame.display.flip()
        pygame.time.wait(5000)  # Esperar 5 segundos para mostrar la imagen final
        show_end_menu = True

    pygame.display.flip()

# Función para mostrar las pantallas de contexto con fondo negro y texto blanco, texto centrado en la parte inferior
def draw_context_intro():
    screen.fill(BLACK)

    if context_screen_index == 0:
        screen.blit(inicio_image, (0, 0))
        draw_centered_text_bottom("Estás sentado en tu cuarto y tienes que ir a anotarte en la universidad", 50)
    elif context_screen_index == 1:
        screen.blit(inter_image, (0, 0))
        draw_centered_text_bottom("Pero la matrícula cuesta dinero y ahora necesitas trabajar", 50)
    elif context_screen_index == 2:
        screen.blit(final_image, (0, 0))
        draw_centered_text_bottom("¡Tu esfuerzo determinará si logras tu título!", 50)

    pygame.display.flip()

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if show_menu:
                if event.key == pygame.K_1:
                    show_menu = False
                    show_intro = True
                elif event.key == pygame.K_2:
                    pygame.quit()
                    sys.exit()

            elif show_intro:
                if event.key == pygame.K_RETURN:
                    show_intro = False
                    show_context_intro = True

            elif show_end_menu:
                if event.key == pygame.K_1:
                    # Reiniciar el juego
                    current_problem_index = 0
                    answer = ""
                    correct_count = 0
                    show_result = False
                    show_end_menu = False
                    show_menu = True
                elif event.key == pygame.K_2:
                    pygame.quit()
                    sys.exit()

            elif show_context_intro:
                if event.key == pygame.K_RETURN:
                    context_screen_index += 1
                    if context_screen_index == 3:
                        show_context_intro = False

            else:
                if event.key == pygame.K_RETURN:
                    # Comprobar si la respuesta es correcta
                    _, correct_answer = problems[current_problem_index]
                    if answer == correct_answer:
                        correct_count += 1

                    # Pasar al siguiente problema o terminar el juego
                    current_problem_index += 1
                    if current_problem_index == len(problems):
                        show_result = True
                    else:
                        answer = ""

                elif event.key == pygame.K_BACKSPACE:
                    # Eliminar el último carácter de la respuesta
                    answer = answer[:-1]
                else:
                    # Agregar el carácter ingresado a la respuesta
                    answer += event.unicode

    if show_context_intro:
        draw_context_intro()
    else:
        draw_interface()
