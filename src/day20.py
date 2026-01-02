from math import prod
from typing import List, Self


type Pixel = bool
type Image = List[List[Pixel]]
type Border = List[Pixel]


class Camera:
    def __init__(self, s: str) -> None:
        header, *data = s.splitlines()
        self.id = int(header.split()[1].split(":")[0])
        self.image = [[tile == '#' for tile in row] for row in data]
        self.connections: set[Self] = set()

    def borders(self) -> List[Border]:
        return [self.top(), self.left(), self.bottom(), self.right()]

    def top(self) -> Border:
        return self.image[0]

    def bottom(self) -> Border:
        return self.image[-1]

    def left(self) -> Border:
        return [row[0] for row in self.image]

    def right(self) -> Border:
        return [row[-1] for row in self.image]

    def flip(self) -> None:
        self.image = flip_image(self.image)

    def rotate(self) -> None:
        self.image = rotate_image(self.image)


def flip_image(image: Image) -> Image:
    return image[::-1]


def rotate_image(image: Image) -> Image:
    return list(row[::-1] for row in zip(*image))


def match_borders_exact(first: Border, second: Border) -> bool:
    return all(f == s for f, s in zip(first, second))


def match_borders(first: Border, second: Border) -> bool:
    return match_borders_exact(first, second) or match_borders_exact(first, reversed(second))


def match_border_to_camera(border: Border, camera: Camera):
    for b in camera.borders():
        if match_borders(border, b):
            return True
    return False


def count_pattern(image: Image, pattern: Image) -> int:
    result = 0
    for row_offset in range(len(image) - len(pattern) + 1):
        for col_offset in range(len(image[0]) - len(pattern[0]) + 1):
            matches = True
            for image_row, pattern_row in zip(image[row_offset:], pattern):
                for image_tile, pattern_tile in zip(image_row[col_offset:], pattern_row):
                    if pattern_tile and not image_tile:
                        matches = False
                        break
                if not matches:
                    break
            if matches:
                result += 1
    return result


def count_monster_pixels(image: Image) -> int:
    monster_image_str = [
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   "
    ]
    monster_image = [[pixel == '#' for pixel in row]
                     for row in monster_image_str]
    pixel_count = sum(sum(row) for row in monster_image)
    count = 0
    for _ in range(4):
        count += count_pattern(image, monster_image)
        monster_image = rotate_image(monster_image)
    monster_image = flip_image(monster_image)
    for _ in range(3):
        count += count_pattern(image, monster_image)
        monster_image = rotate_image(monster_image)
    count += count_pattern(image, monster_image)

    return pixel_count * count


def build_connections(cameras: List[Camera]) -> None:
    for i, camera in enumerate(cameras):
        for other in cameras[i+1:]:
            for border in camera.borders():
                for other_border in other.borders():
                    if match_borders(border, other_border):
                        camera.connections.add(other)
                        other.connections.add(camera)


def build_grid(cameras: List[Camera]) -> List[List[Camera]]:
    seen = set()
    grid = []

    # Build the top row first
    left = next(filter(lambda x: len(x.connections) == 2, cameras))
    top_row = [left]
    seen.add(left)
    cur = next(iter(left.connections))
    while len(cur.connections) > len(left.connections):
        top_row.append(cur)
        seen.add(cur)
        cur = min(filter(lambda x: x not in seen, cur.connections),
                  key=lambda x: len(x.connections))
    top_row.append(cur)
    seen.add(cur)
    grid.append(top_row)

    # Build the remaining grid based on the left and previous row
    prev_row = top_row[1:]
    while len(seen) < len(cameras):
        left = next(filter(lambda x: x not in seen, left.connections))
        row = [left]
        seen.add(left)
        cur = next(filter(
            lambda x: x not in seen and x in prev_row[0].connections, left.connections))
        while len(cur.connections) > len(left.connections):
            row.append(cur)
            seen.add(cur)
            prev_row = prev_row[1:]
            cur = next(filter(
                lambda x: x not in seen and x in prev_row[0].connections, cur.connections))
        row.append(cur)
        seen.add(cur)
        grid.append(row)
        prev_row = row[1:]

    return grid


def adjust_cameras(grid: List[List[Camera]]) -> None:
    # Adjust top left first
    left = grid[0][0]
    while not match_border_to_camera(left.right(), grid[0][1]):
        left.rotate()
    if not match_border_to_camera(left.bottom(), grid[1][0]):
        left.flip()

    # Adjust top row
    for prev, cur in zip(grid[0], grid[0][1:]):
        while not match_border_to_camera(cur.left(), prev):
            cur.rotate()
        if not match_borders_exact(cur.left(), prev.right()):
            cur.flip()

    # Adjust other rows
    prev_left = left
    for row in grid[1:]:
        left = row[0]
        cur = row[1]
        while not match_border_to_camera(left.right(), cur):
            left.rotate()
        if not match_border_to_camera(left.top(), prev_left):
            left.flip()
        prev_left = left

        for prev, cur in zip(row, row[1:]):
            while not match_border_to_camera(cur.left(), prev):
                cur.rotate()
            if not match_borders_exact(cur.left(), prev.right()):
                cur.flip()


def combine_cameras(grid: List[List[Camera]]) -> Image:
    n = len(grid[0][0].image) - 2
    image = [[] for _ in range(len(grid) * n)]
    for i, row in enumerate(image):
        for camera in grid[i // n]:
            img_row = camera.image[i % n + 1][1:-1]
            row.extend(img_row)
    return image


cameras = [Camera(d) for d in open(0).read().split("\n\n")]
build_connections(cameras)
grid = build_grid(cameras)
adjust_cameras(grid)
image = combine_cameras(grid)
pixel_count = sum(sum(row) for row in image)

print("Part 1:", prod(map(lambda x: x.id, filter(
    lambda x: len(x.connections) == 2, cameras))))
print("Part 2:", pixel_count - count_monster_pixels(image))
