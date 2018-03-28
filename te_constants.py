## Width of the pygame screen
width = 900

## Height of the pygame screen
height = 810

## Corresponds to the left click
LEFT = 1

## Corresponds to the right click
RIGHT = 3

## Size of each block
block_size = 30

## Number of blocks in each row
total_blocks_x = 30

## Number of blocks in each columns
total_blocks_y = 15

## Offset used to separate the map and the tile areas
offset = 10

## Location where the usage text is displayed
usage_text_location = (block_size * total_blocks_y) + offset

## Location where the tile area starts
tile_location = usage_text_location + block_size

## Location where the buttons must be created
button_location = (height - block_size)

## Location where the button text must be displayed
button_text_location = (button_location - block_size)

## Holds the current click location's x value
present_x = 0

## Holds the current click location's y value

present_y = 0

## Holds the first tile's location
first_tile = str(0) + ":" + str(tile_location)

## Default strength value
current_strength = 1

## This is the map array which will be written into the .gmap file
map_array = [['0:0'] * total_blocks_x for item in range(total_blocks_y)]

## All the text that must be displayed by the buttons
menu_button_text = ["Import Tile", "Save Map", "Load Map", "New Map", "Exit"]

## All the text that must be displayed by the strength buttons
strength_button_text = ["None", "Normal", "Block"]

## The menu header text
menu_text = ['MENU', 'STRENGTH']

## The usage text to be displayed for the tile editor
usage_text = "Left click to place tile, Right click to delete tile"


##  White color
white = (255, 255, 255)

##  Black color
black = (0, 0, 0)

## Greyish White color
greyish_white = (225, 225, 225)

## Dark Green color
dark_green = (0, 200, 0)

## Green color
green = (0, 255, 0)