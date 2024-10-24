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

presentation_image = pygame.image.load("presentacion.png")
presentation_image = pygame.transform.scale(presentation_image, (WIDTH, HEIGHT))  # Escalar imagen de presentación

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

# Control de tiempo para la animación
logo_start_time = pygame.time.get_ticks()  # Tiempo de inicio de la animación del logo
fade_duration = 3000  # Duración del fade-in y fade-out en milisegundos
fade_in = True  # Control de la dirección del fade
alpha = 0  # Valor de alpha (opacidad)

# Función para dibujar la interfaz
def draw_interface():
    global show_logo, show_menu, show_end_menu, fade_in, alpha, logo_start_time  # Asegúrate de declarar aquí las variables globales

    screen.fill(WHITE)

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
        title_surface = font.render("Bienvenido al Juego", True, BLACK)
        screen.blit(title_surface, (WIDTH // 2 - 100, HEIGHT // 3))

        start_surface = font.render("1. Iniciar", True, BLACK)
        exit_surface = font.render("2. Salir", True, BLACK)

        screen.blit(start_surface, (WIDTH // 2 - 50, HEIGHT // 2))
        screen.blit(exit_surface, (WIDTH // 2 - 50, HEIGHT // 2 + 50))

    elif show_intro:
        # Pantalla de introducción
        screen.blit(presentation_image, (0, 0))  # Mostrar imagen de presentación

        intro_text = "Te matriculaste a la universidad y ya tienes exámenes que tienes que aprobar"
        intro_surface = font.render(intro_text, True, BLACK)
        screen.blit(intro_surface, (100, HEIGHT // 2 - 50))

        prompt_text = "Presiona Enter para empezar"
        prompt_surface = font.render(prompt_text, True, BLACK)
        screen.blit(prompt_surface, (100, HEIGHT // 2))

    elif not show_result:
        # Dibuja un documento simple
        pygame.draw.rect(screen, GRAY, (100, 100, 600, 400))  # Documento
        pygame.draw.rect(screen, BLACK, (100, 100, 600, 400), 2)  # Borde del documento

        # Texto en el documento
        question, _ = problems[current_problem_index]
        text_surface = font.render(question, True, BLACK)
        screen.blit(text_surface, (300, 150))

        # Mostrar la respuesta del usuario
        answer_surface = font.render("Respuesta: " + answer, True, BLACK)
        screen.blit(answer_surface, (300, 250))

        # Dibuja un cuadro de texto para la entrada
        pygame.draw.rect(screen, BLACK, (300, 300, 200, 50), 2)  # Cuadro de texto
        input_text_surface = font.render(answer, True, BLACK)
        screen.blit(input_text_surface, (310, 315))

    elif show_end_menu:
        # Menú de final
        screen.fill(WHITE)
        end_menu_surface = font.render("1. Reiniciar", True, BLACK)
        exit_surface = font.render("2. Salir", True, BLACK)
        screen.blit(end_menu_surface, (WIDTH // 2 - 50, HEIGHT // 2))
        screen.blit(exit_surface, (WIDTH // 2 - 50, HEIGHT // 2 + 50))

    else:
        # Mostrar la imagen del final adecuado
        if correct_count == len(problems):
            screen.blit(final_bueno_image, (0, 0))  # Mostrar imagen de final bueno
            result_surface = font.render("¡Felicitaciones! Ganaste el título de la universidad", True, BLACK)
        elif correct_count >= 1:
            screen.blit(final_normal_image, (0, 0))  # Mostrar imagen de final normal
            result_surface = font.render("Lo hiciste bien, ¡pero todavía hay mucho por mejorar!", True, BLACK)
        else:
            screen.blit(final_malo_image, (0, 0))  # Mostrar imagen de final malo
            result_surface = font.render("No pasaste los exámenes, inténtalo de nuevo.", True, BLACK)

        screen.blit(result_surface, (100, HEIGHT // 2))  # Mostrar mensaje de resultado

        # Después de mostrar el resultado, habilitar el menú de fin de juego
        pygame.display.flip()
        pygame.time.wait(2000)  # Esperar 2 segundos para mostrar la imagen final
        show_end_menu = True

    pygame.display.flip()

# Función para reiniciar el juego
def reset_game():
    global current_problem_index, answer, correct_count, show_result, show_intro, show_menu, show_end_menu
    current_problem_index = 0
    answer = ""
    correct_count = 0
    show_result = False
    show_intro = False
    show_menu = True
    show_end_menu = False

# Bucle principal
def main():
    global answer, correct_count, show_result, current_problem_index, show_intro, show_menu, show_end_menu
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if show_menu:
                    if event.key == pygame.K_1:  # Opción 1: Iniciar el juego
                        show_menu = False
                        show_intro = True
                    elif event.key == pygame.K_2:  # Opción 2: Salir
                        pygame.quit()
                        sys.exit()

                elif show_intro:
                    if event.key == pygame.K_RETURN:
                        show_intro = False  # Ocultar introducción y comenzar el juego

                elif not show_result:
                    if event.key == pygame.K_RETURN:
                        if answer == problems[current_problem_index][1]:  # Verifica si la respuesta es correcta
                            correct_count += 1
                        answer = ""  # Reiniciar respuesta
                        current_problem_index += 1  # Pasar al siguiente problema

                        # Si se han respondido todos los problemas, mostrar resultado
                        if current_problem_index >= len(problems):
                            show_result = True
                    elif event.key == pygame.K_BACKSPACE:  # Eliminar caracteres
                        answer = answer[:-1]
                    else:
                        answer += event.unicode  # Añadir el carácter presionado

                elif show_end_menu:
                    if event.key == pygame.K_1:  # Opción 1: Reiniciar
                        reset_game()
                    elif event.key == pygame.K_2:  # Opción 2: Salir
                        pygame.quit()
                        sys.exit()

        draw_interface()

if __name__ == "__main__":
    main()
