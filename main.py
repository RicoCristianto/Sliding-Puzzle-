# Main.py

import pygame 
import threading

from pygame.time import Clock
from puzzle import Puzzle
from tkinter import Tk, filedialog , simpledialog , messagebox
from a_star import a_star , apply_move

 
pygame.init()
pygame.font.init()

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 650
BGCOLOR = (50, 50, 50)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Sliding Puzzle Game')

clock = Clock()

BUTTON_WIDTH, BUTTON_HEIGHT = 200, 55
BUTTON_X = 650  
IMPORT_BUTTON_Y = 110  

SCRAMBLE_BUTTON_Y = IMPORT_BUTTON_Y + BUTTON_HEIGHT + 10
SETVOID_BUTTON_Y = SCRAMBLE_BUTTON_Y + BUTTON_HEIGHT + 10
SOLVE_BUTTON_Y = SETVOID_BUTTON_Y + BUTTON_HEIGHT + 10
MOVES_TEXT_Y = SOLVE_BUTTON_Y + BUTTON_HEIGHT + 20


BUTTON_COLOR = (255, 255, 255)
FONT = pygame.font.Font(None, 30)


moves = 0  
puzzle_solved = False
solving = False 
elapsed_time = 0.0

def select_image(): 
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[
            ("JPEG files", "*.jpg"),
            ("JPEG files", "*.jpeg"), 
            ("PNG files", "*.png"),
            ("All files", "*.jpg *.jpeg *.png")
        ]
    )
    if file_path:
        if not file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            messagebox.showerror("Error", "File hanya support JPG JPEG dan PNG")
            return None
        return file_path
    else:
        simpledialog.messagebox.showinfo("Dibatalkan" , "Pemilihan Gambar Dibatalkan (Menggunakan Gambar Default)")
        return None

image_path = "Gambar1.jpg"  
p = Puzzle(image_path, (500, 500), (3, 3), (50, 100))  

def draw_button(screen, text, x, y, width, height, color):
    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=8)
    text_surface = FONT.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

def draw_text(screen, text, x, y, color):
    text_surface = FONT.render(text, True, color)
    screen.blit(text_surface, (x, y))

def set_empty_tile():
    root = Tk()
    root.withdraw()
    try:
        value = simpledialog.askinteger("Input", "Pilih angka untuk jadi ubin kosong (1–9):")
        if value and 1 <= value <= 9:
            p.set_empty_tile_by_number(value)
        else:
            simpledialog.messagebox.showinfo("Integer Tidak Valid","Angka diluar range 1-9")
    except:
        simpledialog.messagebox.showinfo("Integer Tidak Valid","Angka diluar range 1-9")
    finally:
        root.destroy()
        
def reset_puzzle():
    global p, moves, puzzle_solved, elapsed_time

    moves = 0
    puzzle_solved = False
    p = Puzzle(image_path, (500, 500), (3, 3), (50, 100))  # Reset puzzle

def solve_puzzle():
    global solving, moves, elapsed_time

    start_state = p.convert_puzzle_to_array()
    goal_state = p.generate_goal_state() 

    if start_state == goal_state:
        simpledialog.messagebox.showinfo("Tidak Bisa Solve", "Puzzle belum discramble")  
        return 
    
    if solving:
        simpledialog.messagebox.showinfo("Sudah berjalan", "Program sudah berjalan")  
        return  

    solving = True
    moves = 0
    elapsed_time = 0.0

    # Konversi puzzle ke array 1D

    #start_state = [1,2,3,4,6,5,9,7,0]
    #goal_state = [1,2,3,4,5,6,7,0,9]

    # print("Start state = ",start_state) # Sudah  benar
    # print("Goal State = ",goal_state) # Sudah  benar

    def run_a_star():
        global solving, moves, elapsed_time

        if start_state == goal_state:
            simpledialog.messagebox.showinfo("Done", "Puzzle sudah dalam goal condition")
            solving = False
            return
    
        # print("Run A*...")  

        solution, solving_time = a_star(start_state, goal_state)
        elapsed_time = solving_time  # Simpan durasi A*

        if solution:
            current_state = start_state[:]
            # print("Solusi ditemukan oleh A*:")
            for step_num, (_, move) in enumerate(solution):
                current_state = apply_move(current_state, move)
                # print(f"Langkah {step_num + 1}: Move = {move} → State = {tuple(current_state)}")
            

            # print(f"State akhir = {tuple(current_state)}")
            print(f"Waktu yang dibutuhkan = {elapsed_time:.7f}")
            for state, move in solution: 
                pygame.time.delay(300)
                if move == "Up":
                    p.move_up()
                elif move == "Down":
                    p.move_down()
                elif move == "Left":
                    p.move_left()
                elif move == "Right":
                    p.move_right()
                moves += 1

            print(f"Total moves = {moves}")
        else:
            print("Solusi tidak ditemukan karena inverse ganjil")

        solving = False  

    threading.Thread(target=run_a_star).start()
    # run_a_star()

def main():
    global p, image_path, moves,  puzzle_solved , elapsed_time
    running = True

    while running:
        p.update()
        clock.tick(60)  
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if BUTTON_X < mouse_pos[0] < BUTTON_X + BUTTON_WIDTH and IMPORT_BUTTON_Y < mouse_pos[1] < IMPORT_BUTTON_Y + BUTTON_HEIGHT:
                    new_image = select_image()
                    if new_image:
                        image_path = new_image
                        reset_puzzle()

                    # for i in range(4):
                    #     for j in range(10):
                    #         print(f"Data ke {j+1} scramble {(i+1)*15} =")
                    #         p.scramble(15*(i+1))
                    #         solve_puzzle()
                        

                elif BUTTON_X < mouse_pos[0] < BUTTON_X + BUTTON_WIDTH and SCRAMBLE_BUTTON_Y < mouse_pos[1] < SCRAMBLE_BUTTON_Y + BUTTON_HEIGHT:
                    p.can_scramble()
                    p.scramble(30)

                elif BUTTON_X < mouse_pos[0] < BUTTON_X + BUTTON_WIDTH and SETVOID_BUTTON_Y < mouse_pos[1] < SETVOID_BUTTON_Y + BUTTON_HEIGHT:
                    reset_puzzle()
                    set_empty_tile()

                elif BUTTON_X < mouse_pos[0] < BUTTON_X + BUTTON_WIDTH and SOLVE_BUTTON_Y < mouse_pos[1] < SOLVE_BUTTON_Y + BUTTON_HEIGHT:
                    if puzzle_solved:
                        simpledialog.messagebox.showinfo("Done", "Puzzle Telah Selesai")

                    elif p.can_solve():
                        solve_puzzle()
                    
                    else:
                        simpledialog.messagebox.showinfo("Error", "Set Empty Tile terlebih dahulu")
                        
        window.fill(BGCOLOR)

        p.render(window)

        draw_button(window, "Import Image", BUTTON_X, IMPORT_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR)
        draw_button(window, "Scramble", BUTTON_X, SCRAMBLE_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR)
        draw_button(window, "Set Empty Tile", BUTTON_X, SETVOID_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR)  # ✅ Tambahkan ini
        draw_button(window, "Solve Puzzle", BUTTON_X, SOLVE_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR)


        draw_text(window, f"Moves: {moves}", BUTTON_X, MOVES_TEXT_Y, (255, 255, 255))
        draw_text(window, f"Time: {elapsed_time:.7f}s", BUTTON_X, MOVES_TEXT_Y + 30, (255, 255, 255))

        if p.is_empty_tile_set():
            draw_text(window, f"Empty Tile: {p.empty_tile_number}", BUTTON_X, MOVES_TEXT_Y + 60, (0, 255, 0))
        else:
            draw_text(window, "Empty Tile: Not Set", BUTTON_X, MOVES_TEXT_Y + 60, (255, 255, 0))

        
        if p.is_empty_tile_set():
            current_state = p.convert_puzzle_to_array()
            goal_state = p.generate_goal_state()

            if current_state == goal_state:
                # if not puzzle_solved:
                #     # puzzle_solved = True
                puzzle_solved = False
                draw_text(window, "Puzzle Selesai!", BUTTON_X, MOVES_TEXT_Y + 90, (0, 255, 0))

        pygame.display.update()

if __name__ == '__main__':
    main()
    pygame.quit()
