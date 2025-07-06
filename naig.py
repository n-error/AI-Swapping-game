import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants for toast message
TOAST_COLOR = (255, 255, 0)  # Yellow color for the toast message background
TOAST_WIDTH = 400  # Width of the toast message box
TOAST_HEIGHT = 50  # Height of the toast message box
Total_move = 0

# Set up the game window
window_width = 800
window_height = 600
screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
pygame.display.set_caption("Swaping Game")

# Colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
PASTEL = (130, 237, 159)

# Font
font = pygame.font.Font(None, 36)

# Global arrays to store the generated permutation and elements of two types
global_filtered_elements1 = []
global_filtered_elements2 = []


# Function to generate a random permutation of balls and filter elements
def generate_permutation(num_balls):
    global global_permutation, global_filtered_elements1, global_filtered_elements2

    ball_radius = 30
    permutation = []
    filtered_elements1 = []
    filtered_elements2 = []
    while True:
        permutation = random.sample(range(1, num_balls + 1), num_balls)
        filtered_elements1 = [num for num, ind in enumerate(permutation) if num != ind + 1]
        filtered_elements2 = [num for num, ind in enumerate(permutation) if num != num_balls - ind]
        if num_balls > 9:
            # Check if at least three elements are true in both filtered lists
            if len(filtered_elements1) >= 3 and len(filtered_elements2) >= 3:
                break
        if num_balls > 4:
            # Check if at least two elements are true in both filtered lists
            if len(filtered_elements1) >= 2 and len(filtered_elements2) >= 2:
                break
        else:
            if any(filtered_elements1) and any(filtered_elements2):
                break
    colors = [RED] * num_balls
    ball_centers = [(ball_radius + i * 2 * ball_radius, window_height // 2) for i in range(num_balls)]

    # Assign the generated permutation and filtered elements to the global variables
    global_permutation = permutation
    global_filtered_elements1 = filtered_elements1
    global_filtered_elements2 = filtered_elements2

    return permutation, colors, ball_radius, ball_centers


# Function to draw the balls on the screen
def draw_balls(permutation, colors, ball_radius, ball_centers, selected_balls):
    max_columns = 11  # Maximum number of columns in the grid
    spacing = 10  # Spacing between balls

    num_balls = len(permutation)
    num_rows = (num_balls + max_columns - 1) // max_columns

    for i, (num, center) in enumerate(zip(permutation, ball_centers)):
        column = i % max_columns
        row = i // max_columns
        x = column * (2 * ball_radius + spacing) + ball_radius
        y = window_height // 2 + row * (2 * ball_radius + spacing)

        if colors[i] == BLUE:
            pygame.draw.circle(screen, BLUE, (x, y), ball_radius)
            if i in selected_balls:
                pygame.draw.circle(screen, GRAY, (x, y), ball_radius - 2)
        else:
            pygame.draw.circle(screen, RED, (x, y), ball_radius)

        text = font.render(str(num), True, WHITE)
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)


# Game state variables
num_balls = None  # Number of balls
permutation = []  # Permutation of balls
colors = []  # Colors of balls
ball_radius = 0  # Radius of the balls
ball_centers = []  # Centers of the balls
game_started = False  # Flag to indicate if the game has started
selected_balls = []  # List to store the indices of selected blue balls
swap_button_visible = False  # Flag to indicate if the swap button is visible
ai_player = False  # Flag to indicate if it's the AI player's turn

# Create the input field
input_field_width = 200
input_field_height = 50
input_field_x = (window_width - input_field_width) // 2
input_field_y = (window_height - input_field_height) // 2
input_rect = pygame.Rect(input_field_x, input_field_y, input_field_width, input_field_height)
input_text = ""
active = False

# Create the confirm button
button_width = 100
button_height = 50
button_x = (window_width - button_width) // 2
button_y = input_field_y + input_field_height + 20
confirm_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

# Create the swap button
swap_button_width = 100
swap_button_height = 50
swap_button_x = (window_width - swap_button_width) // 2
swap_button_y = button_y + button_height + 20
swap_button_rect = pygame.Rect(swap_button_x, swap_button_y, swap_button_width, swap_button_height)


# Function to handle button click event
def button_callback():
    global num_balls, permutation, colors, ball_radius, ball_centers, game_started, ai_player, confirm_button_rect
    num_balls = int(input_text)  # Get the number of balls from the input field
    permutation, colors, ball_radius, ball_centers = generate_permutation(num_balls)
    game_started = True
    ai_player = False  # Reset AI player flag
    confirm_button_rect = None  # Remove the confirm button after it's clicked


def ball_click_handler(pos):
    global colors, selected_balls, swap_button_visible, global_filtered_elements1, global_filtered_elements2

    max_columns = 11  # Maximum number of columns in the grid
    spacing = 10  # Spacing between balls

    num_balls = len(permutation)
    num_rows = (num_balls + max_columns - 1) // max_columns

    for i, (num, center) in enumerate(zip(permutation, ball_centers)):
        column = i % max_columns
        row = i // max_columns
        x = column * (2 * ball_radius + spacing) + ball_radius
        y = window_height // 2 + row * (2 * ball_radius + spacing)

        if pygame.Rect(x - ball_radius, y - ball_radius, 2 * ball_radius, 2 * ball_radius).collidepoint(pos):
            if colors[i] == RED:
                colors[i] = BLUE
                screen.fill((239, 194, 240))
                draw_balls(permutation, colors, ball_radius, ball_centers, selected_balls)
                pygame.display.flip()
                pygame.time.delay(500)

                # Update filtered elements
                if i in global_filtered_elements1:
                    global_filtered_elements1.remove(i)
                if i in global_filtered_elements2:
                    global_filtered_elements2.remove(i)
                # AI Move
                ai_move()
            elif colors[i] == BLUE:
                if i in selected_balls:
                    selected_balls.remove(i)
                    colors[i] = BLUE
                else:
                    selected_balls.append(i)
                    colors[i] = BLUE

    if len(selected_balls) == 2:
        if global_filtered_elements1:
            swap_button_visible = False  # Disable the swap button
            toast("You need to make all Blue", BLUE, 200)
        else:
            swap_button_visible = True  # Enable the swap button
    else:
        swap_button_visible = False


# Function to handle swap button click event
def swap_button_callback():
    global permutation, colors, selected_balls, swap_button_visible, ai_player

    # Swap the positions of the selected blue balls
    index1, index2 = selected_balls
    permutation[index1], permutation[index2] = permutation[index2], permutation[index1]
    colors[index1], colors[index2] = colors[index2], colors[index1]

    # Clear the selected balls list and hide the swap button
    selected_balls = []
    swap_button_visible = False

    # Update the screen to show the swapped balls
    screen.fill((239, 194, 240))
    draw_balls(permutation, colors, ball_radius, ball_centers, selected_balls)
    pygame.display.flip()
    pygame.time.delay(500)  # Add a delay of 500 milliseconds to show the updated state

    # Check for win conditions
    if permutation == sorted(permutation):
        hide_balls("You Won!")
        return
    if permutation == sorted(permutation, reverse=True):
        hide_balls("You Lost!")
        return

    # AI Move
    ai_move()


# Function to display a toast message
def show_toast_message(message):
    toast_width = 250
    toast_height = 50
    toast_x = (window_width - toast_width) // 2
    toast_y = (window_height - toast_height) // 2
    toast_rect = pygame.Rect(toast_x, toast_y, toast_width, toast_height)

    pygame.draw.rect(screen, BLACK, toast_rect)
    toast_text = font.render(message, True, WHITE)
    toast_text_rect = toast_text.get_rect(center=toast_rect.center)
    screen.blit(toast_text, toast_text_rect)
    pygame.display.flip()
    time.sleep(2)  # Display the toast message for 2 seconds


# Function to display a toast message
def toast(message, color, width):
    toast_font = pygame.font.Font(None, 24)
    toast_surface = toast_font.render(message, True, color)
    toast_rect = pygame.Rect((window_width - width) // 2, window_height - 40, width, 30)
    pygame.draw.rect(screen, WHITE, toast_rect)
    screen.blit(toast_surface, toast_rect.move(5, 5))
    pygame.display.update(toast_rect)
    time.sleep(2)
    pygame.draw.rect(screen, WHITE, toast_rect)
    pygame.display.update(toast_rect)


def hide_balls(s):
    # Set up the window size
    width, height = 600, 400
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Winning Message")
    font = pygame.font.Font(None, 36)
    text = font.render(s, True, (0, 0, 0))
    text_rect = text.get_rect(center=(width // 2, height // 2))
    window.fill((255, 255, 255))
    window.blit(text, text_rect)
    pygame.display.flip()
    time.sleep(5)
    pygame.quit()


# Function to evaluate the game state using fuzzy logic
def evaluate_state(permutation, colors, descending=False):
    value = 0
    num_balls = len(permutation)

    # Fuzzy membership values for position only
    position_match = lambda p, i: 1 if p == i else 0.5 if abs(p - i) == 1 else 0

    for i in range(num_balls):
        # Apply fuzzy logic for position evaluation
        if descending:
            value += position_match(permutation[i], num_balls - i)
        else:
            value += position_match(permutation[i], i + 1)

    # Strong fuzzy inference rule: bonus if all balls match their perfect position
    if descending and all(permutation[i] == num_balls - i for i in range(num_balls)):
        value += num_balls * 2  # Strong bonus
    elif not descending and all(permutation[i] == i + 1 for i in range(num_balls)):
        value += num_balls * 2  # Strong bonus

    return value


# Implement Minimax Algorithm
def minimax(permutation, colors, depth, is_maximizing, alpha, beta, descending=False):
    if depth == 0 or permutation == sorted(permutation) or permutation == sorted(permutation, reverse=True):
        return evaluate_state(permutation, colors, descending)

    num_balls = len(permutation)
    if is_maximizing:
        max_eval = float('-inf')
        for i in range(num_balls):
            if colors[i] == RED:
                colors[i] = BLUE
                eval = minimax(permutation, colors, depth - 1, False, alpha, beta, descending)
                colors[i] = RED
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

        # Try all possible swaps for maximizing player
        for i in range(num_balls):
            for j in range(i + 1, num_balls):
                permutation[i], permutation[j] = permutation[j], permutation[i]
                eval = minimax(permutation, colors, depth - 1, False, alpha, beta, descending)
                permutation[i], permutation[j] = permutation[j], permutation[i]
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(num_balls):
            if colors[i] == BLUE:
                colors[i] = RED
                eval = minimax(permutation, colors, depth - 1, True, alpha, beta, descending)
                colors[i] = BLUE
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break

        # Try all possible swaps for minimizing player
        for i in range(num_balls):
            for j in range(i + 1, num_balls):
                permutation[i], permutation[j] = permutation[j], permutation[i]
                eval = minimax(permutation, colors, depth - 1, True, alpha, beta, descending)
                permutation[i], permutation[j] = permutation[j], permutation[i]
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval


# Function for AI move using Minimax Algorithm
def ai_move():
    global permutation, colors, selected_balls, global_filtered_elements1, global_filtered_elements2, Total_move

    Total_move += 1
    toast(f"Total Move: {Total_move}, Now AI's Turn ", RED, 350)

    best_value = float('-inf')
    best_move = None
    best_swap = None
    num_balls = len(permutation)

    # Try changing a single ball's color
    for i in range(num_balls):
        if colors[i] == RED:
            colors[i] = BLUE
            move_value = minimax(permutation, colors, 3, False, float('-inf'), float('inf'), descending=True)
            colors[i] = RED

            if move_value > best_value:
                best_value = move_value
                best_move = i
                best_swap = None

    if best_move is not None:
        colors[best_move] = BLUE
        if best_move in global_filtered_elements1:
            global_filtered_elements1.remove(best_move)
        if best_move in global_filtered_elements2:
            global_filtered_elements2.remove(best_move)

        toast(f"AI turned ball {permutation[best_move]} blue", BLUE, 220)

    # Only try swapping if no more red balls can be turned blue
    if best_move is None:
        for i in range(num_balls):
            for j in range(i + 1, num_balls):
                permutation[i], permutation[j] = permutation[j], permutation[i]
                swap_value = minimax(permutation, colors, 3, False, float('-inf'), float('inf'), descending=True)
                permutation[i], permutation[j] = permutation[j], permutation[i]

                if swap_value > best_value:
                    best_value = swap_value
                    best_move = None
                    best_swap = (i, j)

    if best_swap is not None:
        i, j = best_swap
        permutation[i], permutation[j] = permutation[j], permutation[i]
        toast(f"AI swapped ball {permutation[i]} with ball {permutation[j]}", BLUE, 225)

    Total_move += 1
    toast(f"Total Move: {Total_move}, Now it's Your Turn ", RED, 350)

    # Check for the winning condition after turning all balls blue or making a swap
    if permutation == sorted(permutation):
        hide_balls("You Won!")
        return

    if permutation == sorted(permutation, reverse=True):
        hide_balls("You Lost!")
        return

    if Total_move >= num_balls * num_balls:
        hide_balls("Draw!")
        return


# Game loop
running = True
showing_toast = True


def show_toast_above_input_field(message):
    toast_font = pygame.font.Font(None, 24)
    toast_width = 700
    toast_height = 60
    line_spacing = 5  # spacing between lines
    text_color = BLACK

    # Split the message into multiple lines
    lines = message.split('\n')
    line_surfaces = [toast_font.render(line, True, text_color) for line in lines]

    # Calculate the height of the toast based on the number of lines
    total_text_height = sum(line.get_height() for line in line_surfaces) + (len(line_surfaces) - 1) * line_spacing
    toast_rect = pygame.Rect((window_width - toast_width) // 2, input_field_y - total_text_height - 20, toast_width,
                             total_text_height + 20)

    # Draw the background rectangle
    pygame.draw.rect(screen, PASTEL, toast_rect)

    # Render each line of text
    y_offset = toast_rect.y + 10
    for line_surface in line_surfaces:
        text_rect = line_surface.get_rect(center=(toast_rect.centerx, y_offset + line_surface.get_height() // 2))
        screen.blit(line_surface, text_rect)
        y_offset += line_surface.get_height() + line_spacing

    pygame.display.update(toast_rect)


while running:
    # screen.fill(WHITE)
    screen.fill((239, 194, 240))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False
            if confirm_button_rect and confirm_button_rect.collidepoint(event.pos):
                button_callback()
            if swap_button_visible and swap_button_rect.collidepoint(event.pos):
                swap_button_callback()
            if game_started:
                ball_click_handler(event.pos)
        elif event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    button_callback()
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

    if game_started:
        draw_balls(permutation, colors, ball_radius, ball_centers, selected_balls)

    if confirm_button_rect:
        if showing_toast:
            show_toast_above_input_field(
                "You have to sort the balls in increasing order.\nAI would try to sort in decreasing order. \nSelect number of balls.")
        # Render the input field
        pygame.draw.rect(screen, BLUE if active else WHITE, input_rect)
        pygame.draw.rect(screen, BLACK, input_rect, 2)
        input_surface = font.render(input_text, True, WHITE)
        input_surface_rect = input_surface.get_rect(center=input_rect.center)
        screen.blit(input_surface, input_surface_rect)

        # Render the confirm button
        pygame.draw.rect(screen, GRAY, confirm_button_rect)
        button_text = font.render("Confirm", True, BLACK)
        button_text_rect = button_text.get_rect(center=confirm_button_rect.center)
        screen.blit(button_text, button_text_rect)

    # Render the swap button if visible
    if swap_button_visible:
        pygame.draw.rect(screen, GRAY, swap_button_rect)
        swap_button_text = font.render("Swap", True, BLACK)
        swap_button_text_rect = swap_button_text.get_rect(center=swap_button_rect.center)
        screen.blit(swap_button_text, swap_button_text_rect)

    pygame.display.flip()

pygame.quit()