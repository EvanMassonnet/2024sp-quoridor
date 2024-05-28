import cv2
from PIL import Image
import numpy as np
import create_grid as grid

import pieces_detection as detect

from util import get_limits

SIDE_LENGTH = 9
CELL_SIZE = 24
WALL_SIZE = 6

color_wall1 = [127,47,26]
color_wall2 = [56,74,189] 
color_player1 = []
color_player2 = []

def detect_pieces():

    player1 = None # Tuple with (x, y) coordinates (ask Alice for the axis used)
    player2 = None # Tuple with (x, y) coordinates (ask Alice for the axis used)
    walls_1 = [] # List of tuples with ((x, y), orientation) (orientation = horizontal or vertical) 
    walls_2 = [] # List of tuples with ((x, y), orientation) 

    # cap = cv2.VideoCapture(0)

    # Set capture format to 'MJPG'
    # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m', 'j', 'p', 'g'))

    # while player1 == [] or player2 == [] or walls_1 == [] or walls_2 == []:
    # while True:
        # ret, frame = cap.read()
        # if not ret:
        #     break

    frame = cv2.imread("board.jpeg", cv2.IMREAD_COLOR)

    detected_markers, intersections = grid.game_board(frame.copy(), SIDE_LENGTH, CELL_SIZE, WALL_SIZE)
    
    frame_walls, walls_1 = detect.detect_walls(color_wall1, frame.copy(), intersections)
    # frame_walls, walls_2 = detect.detect_walls(color_wall2, frame.copy(), intersections)
    # frame_piece1, player1 = detect.detect_player(color_player1, frame.copy(), intersections)
    # frame_piece2, player2 = detect.detect_player(color_player2, frame.copy(), intersections)


    print(f'Found {len(walls_1)} walls')
    print(walls_1)
    
    cv2.imshow('frame', frame_walls)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    # cv2.destroyAllWindows()

    walls = walls_1 + walls_2

    return player1, player2, walls

if __name__ == "__main__":
    detect_pieces()