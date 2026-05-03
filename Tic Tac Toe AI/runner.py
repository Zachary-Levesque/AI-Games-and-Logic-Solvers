from pathlib import Path
import sys
import time

import pygame

import tictactoe as ttt


WIDTH, HEIGHT = 600, 400
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ASSET_DIR = Path(__file__).resolve().parent


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    medium_font = pygame.font.Font(str(ASSET_DIR / "OpenSans-Regular.ttf"), 28)
    large_font = pygame.font.Font(str(ASSET_DIR / "OpenSans-Regular.ttf"), 40)
    move_font = pygame.font.Font(str(ASSET_DIR / "OpenSans-Regular.ttf"), 60)

    user = None
    board = ttt.initial_state()
    ai_turn = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)

        if user is None:
            title = large_font.render("Play Tic-Tac-Toe", True, WHITE)
            title_rect = title.get_rect(center=(WIDTH / 2, 50))
            screen.blit(title, title_rect)

            play_x_button = pygame.Rect((WIDTH / 8), (HEIGHT / 2), WIDTH / 4, 50)
            play_x = medium_font.render("Play as X", True, BLACK)
            play_x_rect = play_x.get_rect(center=play_x_button.center)
            pygame.draw.rect(screen, WHITE, play_x_button)
            screen.blit(play_x, play_x_rect)

            play_o_button = pygame.Rect(5 * (WIDTH / 8), (HEIGHT / 2), WIDTH / 4, 50)
            play_o = medium_font.render("Play as O", True, BLACK)
            play_o_rect = play_o.get_rect(center=play_o_button.center)
            pygame.draw.rect(screen, WHITE, play_o_button)
            screen.blit(play_o, play_o_rect)

            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if play_x_button.collidepoint(mouse):
                    time.sleep(0.2)
                    user = ttt.X
                elif play_o_button.collidepoint(mouse):
                    time.sleep(0.2)
                    user = ttt.O
        else:
            tile_size = 80
            tile_origin = (WIDTH / 2 - (1.5 * tile_size), HEIGHT / 2 - (1.5 * tile_size))
            tiles = []
            for i in range(3):
                row = []
                for j in range(3):
                    rect = pygame.Rect(
                        tile_origin[0] + j * tile_size,
                        tile_origin[1] + i * tile_size,
                        tile_size,
                        tile_size,
                    )
                    pygame.draw.rect(screen, WHITE, rect, 3)

                    if board[i][j] != ttt.EMPTY:
                        move = move_font.render(board[i][j], True, WHITE)
                        move_rect = move.get_rect(center=rect.center)
                        screen.blit(move, move_rect)
                    row.append(rect)
                tiles.append(row)

            game_over = ttt.terminal(board)
            current_player = ttt.player(board)

            if game_over:
                winner = ttt.winner(board)
                title_text = "Game Over: Tie." if winner is None else f"Game Over: {winner} wins."
            elif user == current_player:
                title_text = f"Play as {user}"
            else:
                title_text = "Computer thinking..."

            title = large_font.render(title_text, True, WHITE)
            title_rect = title.get_rect(center=(WIDTH / 2, 30))
            screen.blit(title, title_rect)

            if user != current_player and not game_over:
                if ai_turn:
                    time.sleep(0.5)
                    move = ttt.minimax(board)
                    board = ttt.result(board, move)
                    ai_turn = False
                else:
                    ai_turn = True

            click, _, _ = pygame.mouse.get_pressed()
            if click == 1 and user == current_player and not game_over:
                mouse = pygame.mouse.get_pos()
                for i in range(3):
                    for j in range(3):
                        if board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse):
                            board = ttt.result(board, (i, j))

            if game_over:
                again_button = pygame.Rect(WIDTH / 3, HEIGHT - 65, WIDTH / 3, 50)
                again = medium_font.render("Play Again", True, BLACK)
                again_rect = again.get_rect(center=again_button.center)
                pygame.draw.rect(screen, WHITE, again_button)
                screen.blit(again, again_rect)

                click, _, _ = pygame.mouse.get_pressed()
                if click == 1:
                    mouse = pygame.mouse.get_pos()
                    if again_button.collidepoint(mouse):
                        time.sleep(0.2)
                        user = None
                        board = ttt.initial_state()
                        ai_turn = False

        pygame.display.flip()


if __name__ == "__main__":
    main()
