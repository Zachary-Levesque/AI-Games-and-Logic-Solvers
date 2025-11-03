from game import Game
from ai import minimax, alpha_beta
import time

class CheckersGame:
    def __init__(self):
        self.game = Game()
        self.ai_difficulty = 4  # Depth for minimax
        
    def play_human_vs_human(self):
        """Play a game between two human players"""
        print("Starting Human vs Human Checkers Game!")
        print("Enter moves as: row col (e.g., '2 3')")
        print("First select a piece, then select where to move it.")
        print()
        
        while True:
            self.game.draw_board()
            print(f"Current turn: {self.game.turn.upper()}")
            
            # Check for winner
            winner = self.game.winner()
            if winner:
                print(f"Game Over! {winner.upper()} wins!")
                break
            
            try:
                move = input("Enter your move (row col): ").strip().split()
                if len(move) != 2:
                    print("Please enter row and column separated by space")
                    continue
                    
                row, col = int(move[0]), int(move[1])
                
                if not (0 <= row <= 7 and 0 <= col <= 7):
                    print("Invalid coordinates! Use 0-7 for both row and column")
                    continue
                    
                if self.game.select(row, col):
                    print(f"Selected piece at ({row}, {col})")
                    if self.game.valid_moves:
                        print("Valid moves:", list(self.game.valid_moves.keys()))
                else:
                    print("Invalid selection!")
                    
            except ValueError:
                print("Please enter valid numbers!")
            except Exception as e:
                print(f"Error: {e}")
    
    def play_human_vs_ai(self):
        """Play a game between human and AI"""
        print("Starting Human vs AI Checkers Game!")
        print("You are WHITE, AI is RED")
        print("Enter moves as: row col (e.g., '2 3')")
        print("First select a piece, then select where to move it.")
        print()
        
        while True:
            self.game.draw_board()
            
            # Check for winner
            winner = self.game.winner()
            if winner:
                if winner == 'white':
                    print("Congratulations! You won!")
                else:
                    print("AI wins! Better luck next time!")
                break
            
            if self.game.turn == 'white':
                # Human turn
                print("Your turn (WHITE)")
                try:
                    move = input("Enter your move (row col): ").strip().split()
                    if len(move) != 2:
                        print("Please enter row and column separated by space")
                        continue
                        
                    row, col = int(move[0]), int(move[1])
                    
                    if not (0 <= row <= 7 and 0 <= col <= 7):
                        print("Invalid coordinates! Use 0-7 for both row and column")
                        continue
                        
                    if self.game.select(row, col):
                        if self.game.valid_moves:
                            print("Valid moves:", list(self.game.valid_moves.keys()))
                    else:
                        print("Invalid selection!")
                        
                except ValueError:
                    print("Please enter valid numbers!")
                except Exception as e:
                    print(f"Error: {e}")
            else:
                # AI turn
                print("AI is thinking...")
                start_time = time.time()
                
                # Use alpha-beta pruning for better performance
                _, new_board = alpha_beta(self.game.get_board(), self.ai_difficulty, 
                                        float('-inf'), float('inf'), False, self.game)
                
                if new_board:
                    self.game.ai_move(new_board)
                    
                end_time = time.time()
                print(f"AI made its move in {end_time - start_time:.2f} seconds")
    
    def play_ai_vs_ai(self):
        """Watch AI play against itself"""
        print("Starting AI vs AI Checkers Game!")
        print("WHITE AI vs RED AI")
        print()
        
        move_count = 0
        max_moves = 200  # Prevent infinite games
        
        while move_count < max_moves:
            self.game.draw_board()
            print(f"Move {move_count + 1}: {self.game.turn.upper()} AI's turn")
            
            # Check for winner
            winner = self.game.winner()
            if winner:
                print(f"Game Over! {winner.upper()} AI wins!")
                break
            
            # AI move
            start_time = time.time()
            
            if self.game.turn == 'white':
                _, new_board = alpha_beta(self.game.get_board(), self.ai_difficulty, 
                                        float('-inf'), float('inf'), True, self.game)
            else:
                _, new_board = alpha_beta(self.game.get_board(), self.ai_difficulty, 
                                        float('-inf'), float('inf'), False, self.game)
            
            if new_board:
                self.game.ai_move(new_board)
                
            end_time = time.time()
            print(f"AI made its move in {end_time - start_time:.2f} seconds")
            
            move_count += 1
            time.sleep(1)  # Pause to watch the game
            
        if move_count >= max_moves:
            print("Game ended in a draw (max moves reached)")
    
    def main_menu(self):
        """Main menu for game selection"""
        while True:
            print("\n" + "="*50)
            print("CHECKERS GAME")
            print("="*50)
            print("1. Human vs Human")
            print("2. Human vs AI")
            print("3. AI vs AI (Watch)")
            print("4. Set AI Difficulty")
            print("5. Exit")
            print("="*50)
            
            choice = input("Select an option (1-5): ").strip()
            
            if choice == '1':
                self.game.reset()
                self.play_human_vs_human()
            elif choice == '2':
                self.game.reset()
                self.play_human_vs_ai()
            elif choice == '3':
                self.game.reset()
                self.play_ai_vs_ai()
            elif choice == '4':
                try:
                    difficulty = int(input(f"Enter AI difficulty (1-8, current: {self.ai_difficulty}): "))
                    if 1 <= difficulty <= 8:
                        self.ai_difficulty = difficulty
                        print(f"AI difficulty set to {difficulty}")
                    else:
                        print("Please enter a number between 1 and 8")
                except ValueError:
                    print("Please enter a valid number")
            elif choice == '5':
                print("Thanks for playing!")
                break
            else:
                print("Invalid choice! Please select 1-5")

if __name__ == "__main__":
    game = CheckersGame()
    game.main_menu()