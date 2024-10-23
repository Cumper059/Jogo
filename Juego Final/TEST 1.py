import pygame
import sys

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
incorrect_image = pygame.image.load("Incorrect.png")  # Imagen para respuesta incorrecta
correct_image = pygame.image.load("correct.png")  # Imagen para respuesta correcta

# Fuente para el texto
font = pygame.font.Font(None, 36)

# Variables para el estado del juego
problems = [("¿Cuánto es 2 + 2?", "4"),
            ("¿Cuánto es 3 + 3?", "6"),
            ("¿Cuánto es 1 + 1?", "2")]
current_problem_index = 0
answer = ""
correct_count = 0
show_result = False  # Para controlar si mostrar la imagen de resultado

# Función para dibujar la interfaz
def draw_interface():
    screen.fill(WHITE)

    if not show_result:
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
    else:
        # Mostrar la imagen de resultado
        if correct_count > len(problems) // 2:
            screen.blit(correct_image, (0, 0))  # Mostrar imagen correcta
            result_surface = font.render(
                "¡Felicitaciones! Ganaste el título de la universidad", True, BLACK)
        else:
            screen.blit(incorrect_image, (0, 0))  # Mostrar imagen incorrecta
            result_surface = font.render(
                "Por fallar esta vez no vas a ganar el título de la universidad", True, BLACK)

        screen.blit(result_surface, (100, HEIGHT // 2))  # Mostrar mensaje de resultado

    pygame.display.flip()

# Bucle principal
def main():
    global answer, correct_count, show_result, current_problem_index
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:  # Al presionar Enter
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

        draw_interface()

if __name__ == "__main__":
    main()