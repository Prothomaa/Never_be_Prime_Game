import random
import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
# pygame.display.set_caption("Turn of Prime Game")

clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PINK = (216, 191, 216)
PURPLE = (122,55,139)

# Font
font = pygame.font.SysFont("comicsansms", 48)


def is_prime(n):
    # Check if a number is prime
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


class Game:

    def __init__(self):
        while True:
            num = random.randint(10000000, 1000000000000)
            # num = 43364867612
            # num = 100923745
            n = num
            if not is_prime(n):
                break
        self.n = num

    def startState(self):
        return self.n

    def isEnd(self, state):
        return True if not self.prime(state) or state == -1 else False

    def utility(self, state, player):
        if not self.prime(state):
            if player == 1:
                return float('inf')
            else:
                return float('-inf')
        if state == -1:
            if player == 1:
                return float('-inf')
            else:
                return float('inf')

    def successor(self, state, action):
        s = str(state)
        t = str(state)[:-action]
        if len(t) <= 3:
            state = -1
        else:
            state = int(t)
        return state

    def prime(self, state):
        n = state
        if n < 2:
            return True
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return True
        return False

def minimaxPolicy(game, state, player):
    def recurse(state, player):
        if game.isEnd(state) == True:
            return (game.utility(state, player), None)
        if (state, player) in cache:
            return cache[(state, player)]
        choices = [(recurse(game.successor(state, action), -1 * player)[0], action) for action in (1, 2, 3)]
        # print(choices)
        if player == 1:
            val = max(choices)
        else:
            val = min(choices)
        cache[(state, player)] = val
        return val

    value, action = recurse(state, player)
    return (value, action)


cache = {}

game = Game()

button_width = 100
button_height = 60
button_margin = 20
button_font = pygame.font.SysFont("comicsansms", 32)

buttons = []
SKY = (135, 206, 235)
human_button_rect = pygame.Rect(100, window_height - 150, button_width, button_height)
human_button_text = button_font.render("Human", True, BLACK)
human_button = (human_button_rect, human_button_text)

computer_button_rect = pygame.Rect(600, window_height - 150, 150, button_height)
computer_button_text = button_font.render("Computer", True, BLACK)
computer_button = (computer_button_rect, computer_button_text)

restart_button_rect = pygame.Rect(300, window_height - 250, 150, button_height)
restart_button_text = button_font.render("  restart", True, BLACK)
restart_button = (restart_button_rect, restart_button_text)
winner = 100
keep = 100
for i in range(1, 4):
    button_x = (window_width - button_width * 3 - button_margin * 2) / 2 + (button_width + button_margin) * (i - 1)
    button_y = window_height - 150
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    button_text = button_font.render("    "+str(i), True, BLACK)

    buttons.append((button_rect, button_text, i))
state = game.startState()
turn = ''


screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Never be a Prime Game")

# Set up the splash screen
window.fill(PINK)
splash_image = pygame.image.load("video.png")  # Replace "splash_image.png" with your own image file
splash_text = font.render(" Start Game . . .", True, PURPLE)
splash_rect = splash_image.get_rect(center=(screen_width // 2, screen_height // 2))
splash_text_rect = splash_text.get_rect(center=(window_width // 2, 150))

# Set up the splash screen duration
splash_duration = 3  # In seconds

screen.blit(splash_text, splash_text_rect)
# Display the splash screen
screen.blit(splash_image, splash_rect)
pygame.display.flip()

# Wait for the specified duration
start_time = time.time()
while time.time() - start_time < splash_duration:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

# Transition to the main window
# window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Never be a Prime Game")

while True:
    window.fill(WHITE)
    BOX_SIZE = 50
    BOX_MARGIN = 10
    # WHITE = (57, 123, 179)
    # blue = (20, 78, 90)
    WHITE = (216, 191, 216)
    blue = (20, 78, 90)
    SKY = (255, 255, 255)
    #SKY = (135, 206, 235)

    # Render current state text
    state_text = font.render("Current State: " + str(state), True, BLACK)
    digits = [int(digit) for digit in str(state) if str(state) != "-1"]
    x = BOX_MARGIN
    y = BOX_MARGIN
    for number in digits:
        pygame.draw.rect(window, SKY, (x, y, BOX_SIZE, BOX_SIZE))
        font = pygame.font.SysFont("comicsansms", 36)
        text = font.render(str(number), True, BLACK)
        text_rect = text.get_rect(center=(x + BOX_SIZE / 2, y + BOX_SIZE / 2))
        window.blit(text, text_rect)
        x += BOX_SIZE + BOX_MARGIN

    if (keep == 1):
        win_text = font.render("Keep at least 3 digit", True, BLACK)
        win_text_rect = win_text.get_rect()
        win_text_rect.center = (420, 120)
        window.blit(win_text, win_text_rect)

    if (winner == 1):
        state_text = font.render("Current State: " + str(t), True, BLACK)
        win_text = font.render("Alas !!!! You Lost the Game ", True, BLACK)
        win_text_rect = win_text.get_rect()
        win_text_rect.center = (420, 120)
        window.blit(win_text, win_text_rect)

    if (winner == 2):
        state_text = font.render("Current State: " + str(t), True, BLACK)
        win_text = font.render("Hurrah!!! You Win the Game", True, BLACK)
        win_text_rect = win_text.get_rect()
        win_text_rect.center = (420, 120)
        window.blit(win_text, win_text_rect)

    if (winner == 3):
        state_text = font.render("Current State: " + str(t), True, BLACK)
        win_text = font.render("Alas!!! Computer Lost", True, BLACK)
        win_text_rect = win_text.get_rect()
        win_text_rect.center = (420, 120)
        window.blit(win_text, win_text_rect)

    if (winner == 4):
        state_text = font.render("Current State: " + str(t), True, BLACK)
        win_text = font.render("Computer Win !!!!", True, BLACK)
        win_text_rect = win_text.get_rect()
        win_text_rect.center = (420, 120)
        window.blit(win_text, win_text_rect)

    state_text_rect = state_text.get_rect(center=(window_width // 2, 200))
    window.blit(state_text, state_text_rect)
    if turn == '':
        # Render player selection text
        select_text = font.render("Select Turn:", True, BLACK)
        select_text_rect = select_text.get_rect(center=(window_width // 2, 300))
        window.blit(select_text, select_text_rect)
        pygame.draw.rect(window, SKY, human_button[0])
        window.blit(human_button[1], human_button[0])

        pygame.draw.rect(window, SKY, computer_button[0])
        window.blit(computer_button[1], computer_button[0])
        # Render buttons
    else:
        for button in buttons:
            pygame.draw.rect(window, SKY, button[0])
            window.blit(button[1], button[0])
        pygame.draw.rect(window, SKY, restart_button[0])
        window.blit(restart_button[1], restart_button[0])
    pygame.display.update()
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and restart_button_rect.collidepoint(event.pos):
            game = Game()
            state = game.startState()
            turn = ''
            winner = 100
            continue

        if event.type == pygame.MOUSEBUTTONDOWN or turn == 'computer':
            if turn == '':
                if human_button_rect.collidepoint(event.pos):
                    turn = 'human'

                elif computer_button_rect.collidepoint(event.pos):
                    turn = 'computer'

            elif turn == 'human':
                for button in buttons:
                    if button[0].collidepoint(event.pos):
                        action = button[2]
                        if not action <= len(str(state))-3:
                            print("Keep at least 3 digit")
                            keep = 1
                            continue

                        s = str(state)

                        t = str(state)[:-action]
                        print("s :", s)
                        print("t :", t)
                        length_s = len(str(s))
                        length_t = len(str(t))
                        print("len_s :", length_s)
                        print("len_t :", length_t)

                        if length_t <= 3:
                            state = -1
                        elif length_t > 3 and not game.prime(int(t)):
                            state = -1
                        else:
                            state = int(t)

                        if state == -1 and not game.prime(int(t)):
                            print("Alas!! You lost!")
                            winner = 1
                            keep = 0
                            break
                        elif state == -1 and game.prime(int(t)):
                            print("human Wins")
                            winner = 2
                            keep = 0
                            break
                        else:
                            print("human has discarded " + str(action) + " digit")
                            print("human moves state to: ", state)
                            turn = 'computer'
                            break

            elif turn == 'computer':

                val, act = minimaxPolicy(game, state, 1)
                s = str(state)
                # print("act :", act)
                if act is None:
                    '''if length_s == 5:
                        t = t2
                    if length_s == 4:
                        t = t3'''
                    act = 0
                    break

                t3 = str(state)[:-act]
                t = t3

                print("s :", s)
                print("t :", t)
                length_s = len(str(s))
                length_t = len(str(t))
                print("len_s :", length_s)
                print("len_t :", length_t)

                if length_t <= 3:
                    t1 = str(state)[:-1]
                    if length_s == 4:
                        t = t1
                        print("s :", s)
                        print("t :", t)
                    if length_s == 5:
                        if not game.prime(int(t1)):
                            t2 = str(state)[:-2]
                            t = t2
                            print("s :", s)
                            print("t :", t)
                        else:
                            t = t1
                            print("s :", s)
                            print("t :", t)
                    state = -1

                elif length_t > 3 and not game.prime(int(t)):
                    state = -1

                else:
                    state = int(t)

                if state == -1 and not game.prime(int(t)):
                    print("Alas!! computer lost!")
                    winner = 3
                    keep = 0
                    break
                elif state == -1 and game.prime(int(t)):
                    print("computer Wins")
                    winner = 4
                    keep = 0
                    break

                else:
                    print("computer has discarded " + str(act) + " digit")
                    print("computer moves state to: ", state)
                    turn = 'human'
                    break
