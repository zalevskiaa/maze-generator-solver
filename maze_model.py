import cv2
import random
import numpy as np


class Cell:
    def __init__(self, bottom_wall: bool = False, right_wall: bool = False):
        self.bottom_wall = bottom_wall
        self.right_wall = right_wall


class Maze:
    def __init__(self, rows, cols):
        self.rows, self.cols = rows, cols
        self.grid = [[
                Cell()
                for j in range(cols + 1)
            ]
            for i in range(rows + 1)
        ]

        self.generate_random_maze()

    def create_all_borders(self):
        # maze borders

        for i in range(1, self.rows + 1):
            self.grid[i][0].right_wall = True
            # self.grid[i][self.cols].right_wall = True

        for j in range(1, self.cols + 1):
            self.grid[0][j].bottom_wall = True
            # self.grid[self.rows][j].bottom_wall = True

        # all other borders

        for i in range(1, self.rows + 1):
            for j in range(1, self.cols + 1):
                self.grid[i][j].right_wall = True
                self.grid[i][j].bottom_wall = True

    def rec(self, r, c):
        self.grid[r][c].visited = True

        possible_directions = []

        for dr, dc in zip([0, 0, -1, 1], [-1, 1, 0, 0]):
            nr = r + dr
            nc = c + dc

            if not 1 <= nr <= self.rows or not 1 <= nc <= self.cols:
                continue

            if self.grid[nr][nc].visited:
                continue

            possible_directions.append((dr, dc))

        if not possible_directions:
            return

        dr, dc = random.choice(possible_directions)
        # dr, dc = possible_directions[0]

        if (dr, dc) == (0, -1):
            self.grid[r][c - 1].right_wall = False
        elif (dr, dc) == (0, 1):
            self.grid[r][c].right_wall = False
        elif (dr, dc) == (-1, 0):
            self.grid[r - 1][c].bottom_wall = False
        elif (dr, dc) == (1, 0):
            self.grid[r][c].bottom_wall = False
        else:
            raise ValueError

        self.rec(r + dr, c + dc)
        self.rec(r, c)

    def generate_random_maze(self):
        self.create_all_borders()

        for i in range(1, self.rows + 1):
            for j in range(1, self.cols + 1):
                self.grid[i][j].visited = False

        self.rec(1, 1)

    def to_img(self, img_width, img_height, draw_cell_borders=False, thickness=2, color=0):
        img = np.zeros((img_height, img_width, 3), np.uint8)

        img = cv2.rectangle(img, (0, 0), (img_width, img_height),
                            color=(255, 255, 255), thickness=-1)

        if draw_cell_borders:
            for i in range(self.rows + 1):
                y = round(i * img_height / self.rows)
                img = cv2.line(img, (0, y), (img_width, y),
                               color=(150, 150, 150), thickness=1)

            for j in range(self.cols + 1):
                x = round(j * img_width / self.cols)
                img = cv2.line(img, (x, 0), (x, img_height),
                               color=(150, 150, 150), thickness=1)

        # for i in range(self.rows):
        #     for j in range(self.cols):
        #         x = j * img_width_px / self.cols
        #         y = i * img_height_px / self.rows
       
        #         image = cv2.line(image, )

        for i in range(self.rows + 1):
            top = round((i - 1) * img_height / self.rows)
            bottom = round((i) * img_height / self.rows)

            for j in range(self.cols + 1):
                left = round((j - 1) * img_width / self.cols)
                right = round((j) * img_width / self.cols)

                if self.grid[i][j].right_wall:
                    img = cv2.line(img, (right, top), (right, bottom),
                                   color=color, thickness=thickness)
                if self.grid[i][j].bottom_wall:
                    img = cv2.line(img, (left, bottom), (right, bottom),
                                   color=color, thickness=thickness)

        return img
