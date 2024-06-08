import cv2
# import random
import numpy as np

import os
import heapq

from maze_model import Maze


def generate_maze_to_file(dirname='images', filename='maze.png'):
    # w, h = 1600, 900
    w, h = 800, 600
    cell_size = 7
    cols = round(w / cell_size)
    rows = round(h / cell_size)

    maze = Maze(rows, cols)
    img = maze.to_img(w, h, thickness=2, color=(50, 100, 50))

    if 'images' not in os.listdir():
        os.mkdir('images')

    cv2.imwrite('images/maze.png', img)


def distance_to_wall(img, r, c, max_distance):
    if not np.all(img[r, c] == (255, 255, 255)):
        return 0

    for dist in range(1, max_distance):
        if not np.all(img[r-dist:r+dist+1, c-dist:c+dist+1] == (255, 255, 255)):
            return dist

    return max_distance


def gkern(size, sig):
    ax = np.linspace(-(size - 1) / 2., (size - 1) / 2., size)
    gauss = np.exp(-0.5 * np.square(ax) / np.square(sig))
    kernel = np.outer(gauss, gauss)
    return kernel / np.sum(kernel)


def wall_loss_kernel():
    kernel = gkern(size=11, sig=3)
    kernel = (1000 * kernel).astype(np.int64)
    # kernel = np.max(kernel) - kernel
    return kernel


def wall_loss(img):
    """returns matrix of sums (bool(img) * kernel)"""
    pass

def find_and_draw_maze_path(img, max_distance_to_wall):
    # r, c
    start = 5, 5
    finish = img.shape[0] - 5, img.shape[1] - 5

    # heap [ (distance, row, column) ]

    heap = [(0, start[0], start[1])]
    visited = np.zeros(img.shape[:2])
    visited[start[0], start[1]] = 1
    previous = np.zeros((*img.shape[:2], 2), dtype=np.int64)
    
    while heap:
        dist, r, c = heapq.heappop(heap)
        assert np.all(img[r, c, :] == (255, 255, 255))
        
        if (r, c) == finish:
            break

        # for dr, dc in zip([0, 0, -1, 1], [-1, 1, 0, 0]):
        for dr, dc in zip([1, 1, 0, -1, -1, -1, 0, 1], 
                          [0, -1, -1, -1, 0, 1, 1, 1]):
        
            nr, nc = r + dr, c + dc

            if not np.all(img[nr, nc, :] == (255, 255, 255)):
                continue

            if visited[nr, nc]:
                continue
            
            k = 3
            wall_loss = k * (max_distance_to_wall - distance_to_wall(img, r, c, max_distance_to_wall))
            diag_loss = 3 * (dr != 0 and dc != 0)

            nd = dist + 1 + wall_loss + diag_loss

            heapq.heappush(heap, (nd, nr, nc))
            visited[nr, nc] = 1
            previous[nr, nc] = r, c

    else:
        return None

    while (r, c) != start:
        x, y = c, r
        img = cv2.circle(img, (x, y), radius=0, color=(0, 0, 255), thickness=-1)
        r, c = previous[r, c]

    return img


def debug():
    print(wall_loss_kernel())


def main():
    # generate_maze_to_file()
    img = cv2.imread('images/maze.png')
    img_with_path = find_and_draw_maze_path(img, max_distance_to_wall=5)

    if img_with_path is not None:
        cv2.imwrite('images/maze_solved.png', img_with_path)
        # cv2.imshow("A New Image", img_with_path)
        # cv2.waitKey(0)
    else:
        print('not found')


if __name__ == '__main__':
    import sys
    sys. setrecursionlimit(10 ** 5)
    
    # debug()
    main()
