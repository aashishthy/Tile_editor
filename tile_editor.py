"""
Following are the modules used for creating the tile editor
"""

import pygame
import PIL.Image
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox
from tkinter import *
import os
import glob
from shutil import copy
from te_constants import *

"""
This dictionary stores the mapping of the tiles that can be used to create the map
"""
tile_dict = {}

"""
This dictionary stores the mapping of all the tiles textures with their corresponding textures
"""
tile_map = {}

"""
This dictionary holds all the tile data that are used in this map. This will be written into the props file
"""
tile_map_prop = {}

"""
Initialize all pygame modules
"""
pygame.init()

"""
Set the screen size to width * height
"""
screen = pygame.display.set_mode((width,  height))


"""
This is the font file that is used for the menu and strength button labels
"""
font = pygame.font.Font("PressStart2P.ttf", 8)

"""
This is the font file that is used for the header files for the menu and strength and the usage text
"""
menu_font = pygame.font.Font("PressStart2P.ttf", 16)



def show_grid():
    """
    This function shows the entire map as a grid
    """
    pygame.draw.rect(screen, black, pygame.Rect(0, 0, width, total_blocks_y*block_size))
    for y in range(total_blocks_y):
        for x in range(total_blocks_x):
            rect = pygame.Rect(x * block_size, y * block_size, block_size - 1, block_size - 1)
            pygame.draw.rect(screen, greyish_white, rect)


def load_tile_set():
    """
    This function is used to load all the tiles from the Tiles/ folder onto the editor
    """
    global tile_dict, current_tile, tile_map, tile_map_prop
    i = 0
    j = tile_location
    pygame.draw.rect(screen, black, pygame.Rect(i, j - 5, width, (block_size*8)))
    tile_index = 1
    for infile in glob.glob('Tiles/*.png'):
        pic = pygame.image.load(infile)
        pic = pygame.transform.scale(pic, (block_size, block_size))
        if i + block_size > width:
            i = 0
            j += block_size
        screen.blit(pic, (i, j))
        index = str(i) + ':' + str(j)
        tile_map[pic] = tile_index
        tile_map_prop[tile_index] = infile
        tile_index += 1
        tile_dict[index] = pic
        i += block_size
    pygame.display.flip()



def text_surface(message_text, text_font, color):
    """
    This function is used to create the font text surface
    """
    text_surf = text_font.render(message_text, True, color)
    return text_surf, text_surf.get_rect()


def display_menu_text():
    """
    This function displays the usage and menu text at the relevant places
    """
    display_text(usage_text, 450, usage_text_location, menu_font, white)
    display_text(menu_text[0], 170, button_text_location, menu_font, white)
    display_text(menu_text[1], 790, button_text_location, menu_font, white)


def display_text(message_text, x, y, text_font, color):
    """
    This function is used to display the text at the given positions with the given font and color
    """
    t_surface, t_rect = text_surface(message_text, text_font, color)
    t_rect.center = (x, y)
    screen.blit(t_surface, t_rect)
    pygame.display.update()


def load_buttons():
    """
    This function displays the menu and usage text and also creates the menu and strength buttons
    """
    display_menu_text()
    create_menu_buttons()
    create_strength_buttons()
    pygame.display.update()


def create_strength_buttons():
    """
    This function creates the strength buttons
    """
    j = width - (block_size*2) - 10
    index = 0
    for i in range(3):
        selected_color = dark_green
        if i == current_strength:
            button_color = selected_color
        else:
            button_color = white
        pygame.draw.rect(screen, button_color, (j, button_location, block_size * 2, block_size))
        button_text = strength_button_text[index]
        index += 1
        pad = 0
        button_split = button_text.split(" ")
        for word in button_split:
            display_text(word, j + block_size, button_location + (block_size / 2) + pad, font, black)
            pad += 10
        j -= ((block_size * 2) + 10)


def create_menu_buttons():
    """
    This function creates the menu buttons
    """
    j = 0
    index = 0
    for i in range(5):
        button_color = white
        pygame.draw.rect(screen, button_color, (j, button_location, block_size * 2, block_size))
        button_text = menu_button_text[index]
        index += 1
        pad = 0
        button_split = button_text.split(" ")
        for word in button_split:
            display_text(word, j + block_size, button_location + (block_size / 3) + pad, font, black)
            pad += 10
        j += ((block_size * 2) + 10)


def in_tile_menu(mouse_y):
    """
    This function is used to check whether the mouse is in the tile menu
    """
    if tile_location - 10 < mouse_y < button_text_location:
        return True
    else:
        return False



def in_button_menu(mouse_y):
    """
    This function is used to check whether the mouse is in the button menu
    """
    if mouse_y >= button_location:
        return True
    else:
        return False


def in_map_area(mouse_y):
    """
    This function is used to check whether the mouse is in the map area
    """
    if mouse_y < usage_text_location - 10:
        return True
    else:
        return False


def menu_buttons_clicked(mouse_x):
    """
    This function checks which of the menu buttons was clicked and calls the corresponding function
    """
    if button1(mouse_x):
        open_fd()
    elif button2(mouse_x):
        save_map()
    elif button3(mouse_x):
        load_map()
    elif button4(mouse_x):
        reset_map()
    elif button5(mouse_x):
        exit_tile_editor()


def exit_tile_editor():
    """
    This function is used to exit the Tile Editor if Yes was clicked in the pop up message
    """
    if pop_up_msg("Exit Map ?"):
        pygame.quit()


def reset_map():
    """
    This function is used to clear the map in the Tile Editor if Yes was clicked in the pop up message
    """
    if pop_up_msg("Create new Map ?"):
        clear_map()


def pop_up_msg(message):
    """
    This function pops up a messagebox and returns true if the Yes button is clicked and no otherwise
    """
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    answer = messagebox.askquestion(message, "Are you sure you want to - " + message)
    root.focus()
    root.destroy()
    if answer == 'yes':
        return True
    return False


def clear_map():
    """
    This function clears the map in the Tile Editor and displays the grid
    """
    global map_array
    map_array = [['0:0'] * total_blocks_x for item in range(total_blocks_y)]
    show_grid()
    pygame.display.update()


def button_clicked(mouse_x):
    """
    This function calls functions which detect which buttons were clicked
    """
    menu_buttons_clicked(mouse_x)
    strength_buttons_clicked(mouse_x)



def strength_buttons_clicked(mouse_x):
    """
    This function sets the strength to 0, 1 or 2 based on which strength button is clicked
    """
    global current_strength
    if (width - (block_size * 2) - 10) <= mouse_x <= (width - 10):
        current_strength = 0
    elif (width - (block_size * 4)) - 20 <= mouse_x <= (width - block_size * 2) - 20:
        current_strength = 1
    elif (width - (block_size * 6)) - 30 <= mouse_x <= (width - (block_size * 4)) - 30:
        current_strength = 2
    load_buttons()


def load_map():
    """
    This function loads the map from the .gmap and .gmap.props file. We first select the files from the window that is displayed
    """
    extracted_map = []
    extracted_tile_dict = {}
    index = 0
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    file_types = [("Map File", "*.gmap")]
    root.map_file = askopenfilename(filetypes=file_types)
    map_file = root.map_file
    if map_file == '':
        root.destroy()
        return

    file_types = [("Map Props File", "*.props")]
    root.props_file = askopenfilename(filetypes=file_types)
    props_file = root.props_file
    if props_file == '':
        root.destroy()
        return

    fd = open(map_file, "r")
    line = fd.readline()
    while line:
        extracted_line = line.split(" ")
        extracted_line = extracted_line[:-1]
        line = fd.readline()
        extracted_map.insert(index, extracted_line)
        index += 1

    fd_prop = open(props_file, "r")
    line = fd_prop.readline()
    while line:
        tile_index, tile_path = line.split("=")
        extracted_tile_dict[tile_index] = tile_path
        line = fd_prop.readline()
    fd_prop.close()
    fd.close()
    root.destroy()
    load_textures(extracted_map, extracted_tile_dict)


def load_textures(e_map_array, e_tile_dict):
    """
    This function loads all the textures that were present in the .gmap and .gmap.props file
    """
    global map_array
    map_array = e_map_array
    texture_dict = {}
    for key in e_tile_dict.keys():
        pic = pygame.image.load(e_tile_dict[key].replace('\n', ''))
        pic = pygame.transform.scale(pic, (block_size, block_size))
        texture_dict[key] = pic

    for i in range(total_blocks_y):
        for j in range(total_blocks_x):
            index, strength = e_map_array[i][j].split(":")

            if int(index) == 0:
                continue
            else:
                screen.blit(texture_dict[index], (j*block_size, i*block_size))
    pygame.display.update()


def save_map():
    """
    This function saves the map into a .gmap and .gmap.props file
    """
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    f = asksaveasfilename(confirmoverwrite=False, filetype=[("Map File", "*.gmap")])
    if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
        root.destroy()
        return
    f = f + '.gmap'
    write_map_to_file(f)
    write_map_properties_to_file(f)
    root.destroy()


def write_map_to_file(filename):
    """
    This function writes the map_array to a file in the "<tile_index>:<strength>" format.
    """
    fd = open(filename, "w+")
    for i in range(total_blocks_y):
        for j in range(total_blocks_x):
            fd.write(map_array[i][j]+" ")
        fd.write("\n")
    fd.close()
    os.chmod(filename, 0o777)


def write_map_properties_to_file(filename):
    """
    This function write the tile_index and the corresponding path to the image file as a .gmap.props 
    file in a "<tile_index> = <path>" format
    """
    filename = filename + '.props'
    fd = open(filename, "w+")
    img = {}
    for i in range(total_blocks_y):
        for j in range(total_blocks_x):
            value = map_array[i][j]
            value = value.split(":")
            if int(value[0]) != 0:
                img[int(value[0])] = tile_map_prop[int(value[0])]
    for i in img.keys():
        head, tail = os.path.split(img[i])
        fd.write(str(i) + "=" + tail + '\n')
    fd.close()
    os.chmod(filename, 0o777)


def open_fd():
    """
    This function opens the file explorer so that a new tile can be imported
    """
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    file_types = [("PNG", "*.png")]
    root.filename = askopenfilename(filetypes=file_types)
    filename = root.filename
    if filename == '':
        root.destroy()
        return
    copy(filename, "Tiles/")
    load_tile_set()
    root.destroy()



def button1(mouse_x):
    """
    This function returns true if the mouse is over the first button
    """
    if mouse_x <= block_size * 2:
        return True
    else:
        return False


def button2(mouse_x):
    """
    This function returns true if the mouse is over the second button
    """
    if (block_size * 2) + 10 <= mouse_x <= (block_size * 2) + 10 + (block_size * 2):
        return True
    else:
        return False



def button3(mouse_x):
    """
    This function returns true if the mouse is over the third button
    """
    if (block_size * 4) + 20 <= mouse_x <= (block_size * 4) + 20 + (block_size * 2):
        return True
    else:
        return False


def button4(mouse_x):
    """
    This function returns true if the mouse is over the fourth button
    """
    if (block_size * 6) + 30 <= mouse_x <= (block_size * 6) + 30 + (block_size * 2):
        return True
    else:
        return False


def button5(mouse_x):
    """
    This function returns true if the mouse is over the fifth button
    """
    if (block_size * 8) + 40 <= mouse_x <= (block_size * 8) + 40 + (block_size * 2):
        return True
    else:
        return False


def highlight_selection():
    """
    This function is used to highlight the tile that is currently selected
    """
    global present_x, present_y
    pygame.draw.rect(screen, green, pygame.Rect(present_x, present_y + 10, block_size, block_size), 3)
    pygame.display.update()


def left_mouse_clicked(mouse_x, mouse_y):
    """
    This function handles what happens when the left mouse button is clicked. If the mouse is over the tile section, it will
    select the tile, if it is over the buttons, it will call a corresponding function, and if it is over the map area, it 
    places the currently selected tile at that spot
    """
    global present_x, present_y, tile_dict, current_tile, current_strength
    present_x = mouse_x - (mouse_x % block_size)
    present_y = mouse_y - (mouse_y % block_size)
    array_index_x = int(present_x/block_size)
    array_index_y = int(present_y/block_size)
    if in_tile_menu(mouse_y) and not in_button_menu(mouse_y):
        index = str(present_x)+":"+str(present_y + offset)
        if index in tile_dict:
            current_tile = tile_dict[index]
            load_tile_set()
            highlight_selection()
    if in_map_area(mouse_y):
        pygame.draw.rect(screen, black, (present_x, present_y, block_size, block_size))
        screen.blit(current_tile, (present_x, present_y))
        tile_details = tile_map[current_tile]
        map_array[array_index_y][array_index_x] = str(tile_details) + ':' + str(current_strength)
        pygame.display.update()
    if in_button_menu(mouse_y):
        button_clicked(mouse_x)



def right_mouse_clicked(mouse_x, mouse_y):
    """
    This function is used to erase the tile that was placed and to make it look like a cleared tile
    """
    if in_map_area(mouse_y):
        global present_x, present_y
        present_x = mouse_x - (mouse_x % block_size)
        present_y = mouse_y - (mouse_y % block_size)
        pygame.draw.rect(screen, black, (present_x, present_y, block_size, block_size))
        pygame.draw.rect(screen, greyish_white, (present_x, present_y, block_size - 1, block_size - 1))
        array_index_x = int(present_x / block_size)
        array_index_y = int(present_y / block_size)
        map_array[array_index_y][array_index_x] = str(0) + ':' + str(0)
        pygame.display.update()


"""
Functions being called here do the following in order

1. Shows the map as a grid,
2. Loads all the tiles into the tile editor
3. sets the current tile editor to the first tile
4. Loads all the buttons
5. runs the loop until the window is closed
"""

show_grid()
load_tile_set()
current_tile = tile_dict[first_tile]
load_buttons()
running = True
while running:
    mouse_X, mouse_Y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_tile_editor()
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
            right_mouse_clicked(mouse_X, mouse_Y)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            left_mouse_clicked(mouse_X, mouse_Y)


pygame.quit()
