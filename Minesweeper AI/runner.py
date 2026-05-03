from pathlib import Path
import sys
import time

import pygame

from minesweeper import Minesweeper, MinesweeperAI


HEIGHT = 8
WIDTH = 8
MINES = 8
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)
ASSET_DIR = Path(__file__).resolve().parent / "assets"


def main():
    pygame.init()
    screen_width, screen_height = 600, 400
    screen = pygame.display.set_mode((screen_width, screen_height))

    small_font = pygame.font.Font(str(ASSET_DIR / "fonts" / "OpenSans-Regular.ttf"), 20)
    medium_font = pygame.font.Font(str(ASSET_DIR / "fonts" / "OpenSans-Regular.ttf"), 28)
    large_font = pygame.font.Font(str(ASSET_DIR / "fonts" / "OpenSans-Regular.ttf"), 40)

    board_padding = 20
    board_width = ((2 / 3) * screen_width) - (board_padding * 2)
    board_height = screen_height - (board_padding * 2)
    cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
    board_origin = (board_padding, board_padding)

    flag = pygame.image.load(str(ASSET_DIR / "images" / "flag.png"))
    flag = pygame.transform.scale(flag, (cell_size, cell_size))
    mine = pygame.image.load(str(ASSET_DIR / "images" / "mine.png"))
    mine = pygame.transform.scale(mine, (cell_size, cell_size))

    game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
    ai = MinesweeperAI(height=HEIGHT, width=WIDTH)

    revealed = set()
    flags = set()
    lost = False
    instructions = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)

        if instructions:
            title = large_font.render("Play Minesweeper", True, WHITE)
            title_rect = title.get_rect(center=(screen_width / 2, 50))
            screen.blit(title, title_rect)

            rules = [
                "Click a cell to reveal it.",
                "Right-click a cell to mark it as a mine.",
                "Mark all mines successfully to win!",
            ]
            for i, rule in enumerate(rules):
                line = small_font.render(rule, True, WHITE)
                line_rect = line.get_rect(center=(screen_width / 2, 150 + 30 * i))
                screen.blit(line, line_rect)

            button_rect = pygame.Rect((screen_width / 4), (3 / 4) * screen_height, screen_width / 2, 50)
            button_text = medium_font.render("Play Game", True, BLACK)
            button_text_rect = button_text.get_rect(center=button_rect.center)
            pygame.draw.rect(screen, WHITE, button_rect)
            screen.blit(button_text, button_text_rect)

            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse):
                    instructions = False
                    time.sleep(0.3)

            pygame.display.flip()
            continue

        cells = []
        for i in range(HEIGHT):
            row = []
            for j in range(WIDTH):
                rect = pygame.Rect(
                    board_origin[0] + j * cell_size,
                    board_origin[1] + i * cell_size,
                    cell_size,
                    cell_size,
                )
                pygame.draw.rect(screen, GRAY, rect)
                pygame.draw.rect(screen, WHITE, rect, 3)

                if game.is_mine((i, j)) and lost:
                    screen.blit(mine, rect)
                elif (i, j) in flags:
                    screen.blit(flag, rect)
                elif (i, j) in revealed:
                    neighbors = small_font.render(str(game.nearby_mines((i, j))), True, BLACK)
                    neighbors_rect = neighbors.get_rect(center=rect.center)
                    screen.blit(neighbors, neighbors_rect)

                row.append(rect)
            cells.append(row)

        ai_button = pygame.Rect(
            (2 / 3) * screen_width + board_padding,
            (1 / 3) * screen_height - 50,
            (screen_width / 3) - board_padding * 2,
            50,
        )
        ai_text = medium_font.render("AI Move", True, BLACK)
        ai_text_rect = ai_text.get_rect(center=ai_button.center)
        pygame.draw.rect(screen, WHITE, ai_button)
        screen.blit(ai_text, ai_text_rect)

        reset_button = pygame.Rect(
            (2 / 3) * screen_width + board_padding,
            (1 / 3) * screen_height + 20,
            (screen_width / 3) - board_padding * 2,
            50,
        )
        reset_text = medium_font.render("Reset", True, BLACK)
        reset_text_rect = reset_text.get_rect(center=reset_button.center)
        pygame.draw.rect(screen, WHITE, reset_button)
        screen.blit(reset_text, reset_text_rect)

        status = "Lost" if lost else "Won" if game.mines == flags else ""
        status_text = medium_font.render(status, True, WHITE)
        status_rect = status_text.get_rect(center=((5 / 6) * screen_width, (2 / 3) * screen_height))
        screen.blit(status_text, status_rect)

        move = None
        left, _, right = pygame.mouse.get_pressed()

        if right == 1 and not lost:
            mouse = pygame.mouse.get_pos()
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if cells[i][j].collidepoint(mouse) and (i, j) not in revealed:
                        if (i, j) in flags:
                            flags.remove((i, j))
                        else:
                            flags.add((i, j))
                        time.sleep(0.2)
        elif left == 1:
            mouse = pygame.mouse.get_pos()

            if ai_button.collidepoint(mouse) and not lost:
                move = ai.make_safe_move()
                if move is None:
                    move = ai.make_random_move()
                    if move is None:
                        flags = ai.mines.copy()
                        print("No moves left to make.")
                    else:
                        print("No known safe moves, AI making random move.")
                else:
                    print("AI making safe move.")
                time.sleep(0.2)
            elif reset_button.collidepoint(mouse):
                game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
                ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
                revealed = set()
                flags = set()
                lost = False
                continue
            elif not lost:
                for i in range(HEIGHT):
                    for j in range(WIDTH):
                        if (
                            cells[i][j].collidepoint(mouse)
                            and (i, j) not in flags
                            and (i, j) not in revealed
                        ):
                            move = (i, j)

        if move:
            if game.is_mine(move):
                lost = True
            else:
                nearby = game.nearby_mines(move)
                revealed.add(move)
                ai.add_knowledge(move, nearby)

        pygame.display.flip()


if __name__ == "__main__":
    main()
