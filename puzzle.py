#Puzzle.py

import pygame
import random

from tkinter import simpledialog


def split_image(image, size):
    tile_width = image.get_width() // size[0]
    tile_height = image.get_height() // size[1]
    tiles = {}

    number = 1
    for row in range(size[1]):
        for col in range(size[0]):
            rect = pygame.Rect(col * tile_width, row * tile_height, tile_width, tile_height)
            tiles[(col, row)] = (image.subsurface(rect), number)
            number += 1

    return tiles


class Puzzle():
    def __init__(self, image_file_name, image_size, puzzle_size, pos, show_scramble=False):
        self.loadedimage = pygame.image.load(image_file_name)
        self.loadedimage = pygame.transform.scale(self.loadedimage, image_size)
        
        self.pos = pos
        self.dim = image_size
        self.tiles = split_image(self.loadedimage, puzzle_size)
        self.original_tiles = dict(self.tiles)
        self.size = puzzle_size

        self.puzzle = []
        for i in range(puzzle_size[0]):
            self.puzzle.append([])
            for j in range(puzzle_size[1]):
                self.puzzle[i].append((i,j))

        # empty_x, empty_y = (2,2)
        # self.void = (empty_x, empty_y) 
        # self.puzzle[empty_x][empty_y] = (-1, -1)
        self.void = None
        self.empty_tile_number = None

        self.show_scramble = show_scramble
        self.scramble_moves = 0
        self.moves = [self.move_up, self.move_down, self.move_left, self.move_right]

        self.animating = None
        self.buffer = (0,0)
        self.ANIMATION_SPEED = 0.1

    def set_empty_tile_by_number(self, number):
        found = False

        if not (1 <= number <= 9):
            print(f"❌ Nomor {number} tidak valid. Harus 1-9.")
            return False
        
    def set_empty_tile_by_number(self, number):
        """Set tile dengan nomor tertentu sebagai empty tile"""
        if not (1 <= number <= 9):
            simpledialog.messagebox.showwarning("Nomor {number} tidak valid. Harus 1-9.")
            return False

        # Cari posisi tile dengan nomor tersebut
        target_pos = None
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                tile = self.puzzle[i][j]
                _, tile_number = self.tiles[tile]
                if tile_number == number:
                    target_pos = (i, j)
                    break
            if target_pos:
                break

        if not target_pos:
            simpledialog.messagebox.showwarning("Tile nomor {number} tidak ditemukan.")
            return False

        # Set void position dan empty tile number
        self.void = target_pos
        self.empty_tile_number = number
        
        # Tandai posisi ini sebagai void di puzzle array
        self.puzzle[target_pos[0]][target_pos[1]] = (-1, -1)
        
        print(f"Tile nomor {number} di posisi {target_pos} dijadikan empty tile.")
        return True

    def is_empty_tile_set(self):
        """Check apakah empty tile sudah diset"""
        return self.void is not None

    def can_scramble(self):
        """Check apakah bisa scramble (empty tile harus sudah diset)"""
        return self.is_empty_tile_set()

    def can_solve(self):
        """Check apakah bisa solve (empty tile harus sudah diset)"""
        return self.is_empty_tile_set()

    def is_solvable(self, state):
         
        if not self.is_empty_tile_set():
            return False
         
        # Cek Inverse
        puzzle = [x for x in state if x != 0]
        inversions = 0
        for i in range(len(puzzle)):
            for j in range(i + 1, len(puzzle)):
                if puzzle[i] > puzzle[j]:
                    inversions += 1
        return inversions % 2 == 0

    def render(self, screen):
        pos = self.pos
        dim = self.dim
        cell_width = dim[0] // self.size[0]
        cell_height = dim[1] // self.size[1]

        font = pygame.font.Font(None, 50)

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                tile = self.puzzle[i][j]

                if tile != (-1, -1):  # Selain ubin kosong
                    tile_image, number = self.tiles[tile]

                    # Hitung offset jika ubin ini sedang dianimasikan
                    offset_x, offset_y = 0, 0
                    if self.animating == (i, j):
                        offset_x = int(self.buffer[0] * cell_width)
                        offset_y = int(self.buffer[1] * cell_height)

                    screen.blit(tile_image, (pos[0] + i * cell_width + offset_x,
                                            pos[1] + j * cell_height + offset_y))

                    # Render angka diatas ubin
                    text_surface = font.render(str(number), True, (255, 0, 0))
                    text_rect = text_surface.get_rect(center=(
                        pos[0] + i * cell_width + cell_width // 2 + offset_x,
                        pos[1] + j * cell_height + cell_height // 2 + offset_y
                    ))
                    screen.blit(text_surface, text_rect)

        # Gambar garis grid
        for i in range(self.size[0] + 1):
            pygame.draw.line(screen, (0, 0, 0), (pos[0] + i * cell_width, pos[1]),
                            (pos[0] + i * cell_width, pos[1] + self.size[1] * cell_height), 5)

        for j in range(self.size[1] + 1):
            pygame.draw.line(screen, (0, 0, 0), (pos[0], pos[1] + j * cell_height),
                            (pos[0] + self.size[0] * cell_width, pos[1] + j * cell_height), 5)
        
    def reduce_buffer(self):
        if self.buffer[0] > 0:
            self.buffer = (max(0,self.buffer[0]-self.ANIMATION_SPEED), self.buffer[1])

        if self.buffer[0] < 0:
            self.buffer = (min(0,self.buffer[0]+self.ANIMATION_SPEED), self.buffer[1])

        if self.buffer[1] > 0:
            self.buffer = (self.buffer[0], max(0,self.buffer[1]-self.ANIMATION_SPEED))

        if self.buffer[1] < 0:
            self.buffer = (self.buffer[0], min(0,self.buffer[1]+self.ANIMATION_SPEED))

    def move_up(self, animate=True, anim_time=1):
        if self.void[1] > 0:
            self.puzzle[self.void[0]][self.void[1]] = self.puzzle[self.void[0]][self.void[1]-1]
            self.puzzle[self.void[0]][self.void[1]-1] = (-1,-1)
            self.void = (self.void[0], self.void[1]-1)
            if animate:
                self.animating = (self.void[0], self.void[1]+1)
                self.buffer = (0, -1 * anim_time)
        

    def move_down(self, animate=True, anim_time=1):
        if self.void[1] < self.size[1] - 1:
            self.puzzle[self.void[0]][self.void[1]] = self.puzzle[self.void[0]][self.void[1]+1]
            self.puzzle[self.void[0]][self.void[1]+1] = (-1,-1)
            self.void = (self.void[0], self.void[1]+1)
            if animate:
                self.animating = (self.void[0], self.void[1]-1)
                self.buffer = (0, 1 * anim_time)

    def move_left(self, animate=True, anim_time=1):
        if self.void[0] > 0:
            self.puzzle[self.void[0]][self.void[1]] = self.puzzle[self.void[0]-1][self.void[1]]
            self.puzzle[self.void[0]-1][self.void[1]] = (-1,-1)
            self.void = (self.void[0]-1, self.void[1])
            if animate:
                self.animating = (self.void[0]+1, self.void[1])
                self.buffer = (-1 * anim_time, 0)

    def move_right(self, animate=True, anim_time=1):
        if self.void[0] < self.size[0] - 1:
            self.puzzle[self.void[0]][self.void[1]] = self.puzzle[self.void[0]+1][self.void[1]]
            self.puzzle[self.void[0]+1][self.void[1]] = (-1,-1)
            self.void = (self.void[0]+1, self.void[1])
            if animate:
                self.animating = (self.void[0]-1, self.void[1])
                self.buffer = (1 * anim_time, 0)

    def update(self):
        if self.animating != None:
            self.reduce_buffer()
            if self.buffer == (0,0):
                self.animating = None
        elif self.scramble_moves > 0:
            self.scramble()

    def scramble(self, num_moves=None):

        if not self.can_scramble():
            simpledialog.messagebox.showwarning("Tidak bisa scramble!", "Set empty tile terlebih dahulu.")
            return
        
        if num_moves is not None:
            self.scramble_moves = num_moves
        elif self.scramble_moves == 0:
            self.scramble_moves = 10
        
        last_move = None
        
        if self.show_scramble:
            if self.scramble_moves > 0:
                valid_moves = self.get_valid_moves(last_move)
                if valid_moves:
                    move_func = random.choice(valid_moves)
                    move_name = move_func.__name__
                    move_func(True, 0.001)
                    last_move = move_name
                    self.scramble_moves -= 1
        else:
            total_scramble = self.scramble_moves
            for i in range(total_scramble):
                valid_moves = self.get_valid_moves(last_move)
                if valid_moves:
                    move_func = random.choice(valid_moves)
                    move_name = move_func.__name__
                    move_func(False)  # No animation
                    last_move = move_name
            self.scramble_moves = 0


    def get_valid_moves(self, exclude_reverse=None):

        valid_moves = []
        
        if self.void[1] > 0:  
            if exclude_reverse != "move_down":  
                valid_moves.append(self.move_up)
        
        if self.void[1] < self.size[1] - 1:  
            if exclude_reverse != "move_up":  
                valid_moves.append(self.move_down)
        
        if self.void[0] > 0:  
            if exclude_reverse != "move_right":  
                valid_moves.append(self.move_left)
        
        if self.void[0] < self.size[0] - 1:  
            if exclude_reverse != "move_left":  
                valid_moves.append(self.move_right)
        
        return valid_moves

    def generate_goal_state(self):
        # Generate goal state dari Start State
        if not self.is_empty_tile_set():
            raise ValueError("Empty tile belum diset! Tidak bisa generate goal state.")
        
        start_state = self.convert_puzzle_to_array()
        angka_ditemukan = set(x for x in start_state if x != 0)
        angka_hilang = list(set(range(1, 10)) - angka_ditemukan)
    
        if not angka_hilang:
            raise ValueError("Tidak ditemukan angka hilang, error")

        missing_tile = angka_hilang[0]

        angka_tersisa = sorted(angka_ditemukan | {missing_tile})
        goal_state = []

        for angka in angka_tersisa:
            if angka == missing_tile:
                goal_state.append(0)
            else:
                goal_state.append(angka)
                
        return goal_state

        
    def convert_puzzle_to_array(self):
        # Konversi puzzle ke 1D
        if not self.is_empty_tile_set():
            
            flat_puzzle = []
            for row in range(self.size[1]):  
                for col in range(self.size[0]):  
                    tile = self.puzzle[col][row]
                    _, tile_number = self.tiles[tile]
                    flat_puzzle.append(tile_number)
            return flat_puzzle
        
        flat_puzzle = []
        for row in range(self.size[1]):  
            for col in range(self.size[0]):  
                tile = self.puzzle[col][row]
                if tile == (-1, -1):  
                    flat_puzzle.append(0) #Ubin kosong
                else:
                    _, tile_number = self.tiles[tile]  #Ambil angka dari dictionary tiles
                    flat_puzzle.append(tile_number)

        return flat_puzzle
