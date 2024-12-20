import cv2
from PIL import Image
import numpy as np
from .create_grid import *
import os


from .pieces_detection import *

## This script puts together all the Computer Vision and can be called by the solver algorithm to get the current (stateless) state of the board.

IMAGE_SIZE = 500
SIDE_LENGTH = 9
CELL_SIZE = 24
WALL_SIZE = 6
IMAGE_SIZE = 600


color1 = [140,88,46] #BGR for blue player
color2 = [85,65,173] #BGR for red player

# color1 = [127,47,26]
# color2 = [0,0,255]

def setup_camera():
    cap = cv2.VideoCapture(1)

    # Set capture format to 'MJPG'
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m', 'j', 'p', 'g'))

    return cap

def detect_pieces(cap=setup_camera(), debug = False):

    player1 = None # Tuple with (x, y) coordinates 
    player2 = None # Tuple with (x, y) coordinates 
    walls_1 = [] # List of tuples with ((x, y), orientation) (orientation = H or V) 
    walls_2 = [] # List of tuples with ((x, y), orientation) 

    ## the code loops until it detects both players on the board, which is the minimal requirement for an actual game state
    while player1 == None or player2 == None or player1 == [0,0] or player2 == [0,0]:

        ret = False
        while not ret:
            ret, frame = cap.read()
    
        # USED WHEN DEBUGGING WHILE NOT AT DLL with picture of the board stored
        # script_dir = os.path.dirname(os.path.abspath(__file__))
        # image_dir = os.path.join(script_dir, "board_test/board4.jpeg")
        # frame = cv2.imread(image_dir, cv2.IMREAD_COLOR)

        warped_img, intersections = game_board(frame.copy(),IMAGE_SIZE, SIDE_LENGTH, CELL_SIZE, WALL_SIZE)
        
        frame_walls1, walls_1 = detect_walls(color1, warped_img.copy(), intersections, warped_img.copy())
        frame_walls2, walls_2 = detect_walls(color2, warped_img.copy(), intersections, frame_walls1)
        frame_piece1, player1 = detect_player(color1, warped_img.copy(), intersections, frame_walls2)
        total_frame, player2 = detect_player(color2, warped_img.copy(), intersections, frame_piece1)
        print(player2)

        walls = walls_1 + walls_2

        if(debug):
            print(player1)
            print(player2)
            print(walls)

        
        # ---- FOR DEBUG AND VIZUALISATION PURPOSES --------
        while debug: 
            # print(player2)
            cv2.imshow('frame', total_frame)
            # cv2.imshow('frame', frame_piece2)
            # cv2.imshow('frame', frame_walls1)
            # cv2.imshow('frame', frame_walls2)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break 
            
    # cv2.destroyAllWindows()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir_out = os.path.join(script_dir, "camera_output/output.png")

    cv2.imwrite(image_dir_out, total_frame)

    print("Player 1: ", player1)
    print("Player 2: ", player2)
    print("Walls: ", walls)
    
    return player1, player2, walls


        

if __name__ == "__main__":
    cap = setup_camera()
    p1, p2, w = detect_pieces(cap)
    print("===========")
    print(p1)
    print(p2)
    print(w)
    