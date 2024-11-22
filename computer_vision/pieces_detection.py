import cv2
import numpy as np

from util import *
from time import sleep

from create_grid import game_board

SIDE_LENGTH = 9
CELL_SIZE = 24
WALL_SIZE = 6

color = [99, 56, 44]  # Color in BGR colorspace

color_red = [19, 48, 176]  # Color in BGR colorspace
color_blue = [242, 27, 7]  # Color in BGR colorspace

color_wall1 = []
color_wall2 = []
color_player1 = []
color_player2 = []

def detect_color(color, frame):
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lowerLimit, upperLimit = get_limits(color, sensitivity=30)      #Change this depending on the light
    return cv2.inRange(hsvImage, lowerLimit, upperLimit)


def detect_walls(color, image, intersections, vis_img):
    #Create color mask
    mask = detect_color(color, image)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    walls = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        # Ignore contours that are too small or too large
        #TODO: Tune these values
        if area < 500 or 30000 < area:
            continue

        # cv.minAreaRect returns: (center(x, y), (width, height), angle of rotation) 
        rect = cv2.minAreaRect(cnt)
        cvAngle = int(rect[2])

        if (cvAngle > 45):
            cvAngle = 90
        else :
            cvAngle = 0

        width = int(rect[1][0])
        height = int(rect[1][1])

        if (width == height):
            continue

        if (width < height):
            angle = 'V'
        if (height < width): 
            angle = 'H'

        if(angle == 'V' and (height > 150 or height < 80 )) :
            continue
        if (angle == 'H' and (width > 150 or width < 80 )) :
            continue

        if (cvAngle == 90):
            if (angle == 'H'):
                angle = 'V'
            else:
                angle = 'H'

        ##print(f'WIDTH: {rect[1][0]}')
        ##print(f'HEIGHT: {rect[1][1]}')

        box = cv2.boxPoints(rect)
        box = np.int0(box)

        center = (int(rect[0][0]),int(rect[0][1])) 
     

        #Detect cell of the wall
        cell = detect_cell_wall(image, center, intersections)

        # walls.append((cell,angle))
        walls.append((cell,angle))

        # Draw each contour only for visualisation purposes
        vis_img = cv2.drawContours(vis_img,[box],0,(0,0,255),2)
        vis_img = cv2.putText(vis_img, f"({angle}, w-{width}, h-{height})", (center[0], center[1]), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    return vis_img, walls

def detect_player(color, image, intersections, vis_img):
    #Create color mask
    mask = detect_color(color, image)
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # print(f'Found {len(contours)} contours')
    cell = [0,0]

    for cnt in contours:
        area = cv2.contourArea(cnt)
        # Ignore contours that are too small or too large
        #TODO: Tune these values
        # if area < 500 or 30000 < area:
        #     continue

        # cv.minAreaRect returns: (center(x, y), (width, height), angle of rotation) 
        rect = cv2.minAreaRect(cnt)
        width = int(rect[1][0])
        height = int(rect[1][1])

        if(width < 10 or width > 50 or height > 50 or height < 10) : #or np.abs(width - height) > 7) :
            continue

        box = cv2.boxPoints(rect)
        box = np.int0(box)

        center = (int(rect[0][0]),int(rect[0][1])) 

        # Now detect the cell associated with this player
        cell = detect_cell_player(center, intersections)
        # print(f'Cell: {cell}')
        
        # Draw each contour only for visualisation purposes
        vis_img = cv2.drawContours(vis_img,[box],0,(0, 255, 0),2)
        

    return vis_img, cell


# given the center coordinates of the detected player and all the grid intersections points, find the game-coordinates of the player
def detect_cell_player(center, intersections):
    cx = center[0]
    cy = center[1]

    for i in range(len(intersections) - SIDE_LENGTH*2 - 1):
        # print("index is ", i)
        top_left = intersections[i+0]
        top_right = intersections[i+1]
        bottom_left = intersections[i+SIDE_LENGTH*2]
        bottom_right = intersections[i+1+SIDE_LENGTH*2]
        if top_left[0][0] <= cx and top_left[0][1] >= cy and top_right[0][0] >= cx and top_right[0][1] >= cy and bottom_left[0][0] <= cx and bottom_left[0][1] <= cy and bottom_right[0][0] >= cx and bottom_right[0][1] <= cy:
            # print(f"For wall centered on {(cx, cy)} within coordinates top left {top_left}, top right {top_right}, bottom left {bottom_left} and bottom right {bottom_right}")
            # print(f"at index {i} intersection for top left is {intersections[i]}")
            print(top_left[1])
            return top_left[1]

# same as detect_cell_player but for wall pieces
def detect_cell_wall(image, center, intersections):
    cx = center[0]
    cy = center[1]

    for i in range(len(intersections) - SIDE_LENGTH*2 - 1):
        # print("index is ", i)
        top_left = intersections[i+0]
        top_right = intersections[i+1]
        bottom_left = intersections[i+SIDE_LENGTH*2]
        bottom_right = intersections[i+1+SIDE_LENGTH*2]
        # """ print("corners are: ", top_left[0][0], " ", top_left[0][1], ", ",  
        #       top_right[0][0], " ", top_right[0][1], ", ", bottom_left[0][0], " ",
        #         bottom_left[0][1], ", ", bottom_right[0][0], " ", bottom_right[0][1])
        # print (" and object center is ", cx, " ", cy) """
        if top_left[0][0] <= cx and top_left[0][1] >= cy and top_right[0][0] >= cx and top_right[0][1] >= cy and bottom_left[0][0] <= cx and bottom_left[0][1] <= cy and bottom_right[0][0] >= cx and bottom_right[0][1] <= cy:
            # print(f"For wall centered on {(cx, cy)} within coordinates top left {top_left}, top right {top_right}, bottom left {bottom_left} and bottom right {bottom_right}")
            # print(f"at index {i} intersection for top left is {intersections[i]}")
            # """ cv2.circle(image, (top_left[0]), 5, (255, 255, 0), -1)
            # cv2.circle(image, (top_right[0]), 5, (255, 255, 0), -1)
            # cv2.circle(image, (bottom_left[0]), 5, (255, 255, 0), -1)
            # cv2.circle(image, (bottom_right[0]), 5, (255, 255, 0), -1) """
            return top_left[1]


def show_camera(camera_id):
    cap = cv2.VideoCapture(camera_id)
    print(f"Camera {camera_id} is open: {cap.isOpened()}")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        warped_img, intersections = game_board(frame.copy(), 500, SIDE_LENGTH, CELL_SIZE, WALL_SIZE)
        frame_walls1, walls_1 = detect_walls(color_red, warped_img.copy(), intersections, warped_img.copy())
        frame_walls2, walls_2 = detect_walls(color_blue, warped_img.copy(), intersections, warped_img.copy())
        frame_piece1, player1 = detect_player(color_red, warped_img.copy(), intersections, warped_img.copy())
        frame_piece2, player2 = detect_player(color_blue, warped_img.copy(), intersections, warped_img.copy())

        # cv2.imshow('frame', frame)
        # cv2.imshow('warped', warped_img)
        cv2.imshow('frame_walls_red', frame_walls1)
        cv2.imshow('frame_walls_blue', frame_walls2)
        cv2.imshow('frame_piece_red', frame_piece1)
        cv2.imshow('frame_piece_blue', frame_piece2)
        

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    while True:
        show_camera(1)
        sleep(1)


if __name__ == "__main__":
    main()
