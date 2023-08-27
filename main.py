# This is a sample Python script.
import os

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

the_way = []
cross_points = []


class CheckPoint:
    def __init__(self, point: tuple, ways: []):
        self.point = point
        self.ways = ways


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def read_map(file_path):
    vmap = []
    with open(file_path, 'r', encoding="utf-8") as __file__:
        for line in __file__.readlines():
            vmap.append(list(map(lambda x: int(x), line.strip().split(","))))
    return vmap


def find_way(start_point, next_point, virtual_map):
    if virtual_map[start_point[0]][start_point[1]] == 1:
        print('error: starting point is wall')
        return
    next_position = virtual_map[next_point[0]][next_point[1]]
    if next_position == 1:
        print('error: wrong direction')
        return
    print(f'robot move to {next_point[0]}, {next_point[1]}')
    the_way.append(next_point)
    three_next_ways = check_three_direction(start_point, next_point)
    if three_next_ways is None:
        print('error: No found next ways')
    positions = list(map(lambda x: virtual_map[x[0]][x[1]], three_next_ways))
    calculated_way = sum(positions)
    if calculated_way > 2:
        if calculated_way > 5:
            print('found the gate!!!')
            return
        else:
            print('no others way!')
            do_backward_way()
    if calculated_way == 2:
        # there's only 1 way
        for way in three_next_ways:
            if int(virtual_map[way[0]][way[1]]) == 0:
                find_way(next_point, way, virtual_map)
    if calculated_way < 2:
        print('found cross ways')
        cp = checkpoint_exist(next_point)
        if cp is None:
            cp = add_checkpoint(next_point, virtual_map)
        # Mark the way just passed
        for way in cp.ways:
            if way[0] == start_point:
                way[1] = way[1] + 1
        # Move to another path
        next_move_point = choose_next_way(cp, start_point)
        if next_move_point is None:
            print('no others way!')
            do_backward_way()
        else:
            find_way(next_point, next_move_point, virtual_map)


def do_backward_way():
    the_old_step = the_way.pop()
    while True:
        try:
            previous_way = the_way.pop()
            print(f'robot move back {previous_way[0]}, {previous_way[1]}')
            cp = checkpoint_exist(previous_way)
            if cp is None:
                the_old_step = previous_way
                continue
            # found cross way
            for way in cp.ways:
                # Mark the way just passed
                if way[0] == the_old_step:
                    way[1] = way[1] + 1
            the_way.append(previous_way)
            next_move_point = choose_next_way(cp, the_old_step)
            if next_move_point is None:
                # Keep doing revert
                do_backward_way()
            else:
                find_way(previous_way, next_move_point, virtual_map)
            break
        except IndexError:
            print('No found way out')
            return


def choose_next_way(checkpoint: CheckPoint, previous_way: tuple) -> tuple:
    # prefer the new way
    for way in checkpoint.ways:
        if way[1] == 0:
            way[1] = way[1] + 1
            return way[0]
    count_way_equal_1 = 0
    for way in checkpoint.ways:
        if way[1] == 1:
            count_way_equal_1 = count_way_equal_1 + 1
    # in case all path has been passed 1 time, prefer the old way
    if count_way_equal_1 == len(way):
        for way in checkpoint.ways:
            if way[0] == previous_way:
                way[1] = way[1] + 1
                return way[0]
    # chose the way can be passed
    for way in checkpoint.ways:
        if way[1] < 2:
            way[1] = way[1] + 1
            return way[0]
    # No path can go
    return None


def add_checkpoint(point, vmap):
    ways = []
    if vmap[point[0] + 1][point[1]] == 0:
        ways.append([(point[0] + 1, point[1]), 0])
    if vmap[point[0] - 1][point[1]] == 0:
        ways.append([(point[0] - 1, point[1]), 0])
    if vmap[point[0]][point[1] + 1] == 0:
        ways.append([(point[0], point[1] + 1), 0])
    if vmap[point[0]][point[1] - 1] == 0:
        ways.append([(point[0], point[1] - 1), 0])
    cp = CheckPoint(point, ways)
    cross_points.append(cp)
    return cp


def checkpoint_exist(p: tuple):
    for cp in cross_points:
        if p == cp.point:
            return cp
    return None


def check_three_direction(previous_point, current_point):
    tx = current_point[0] - previous_point[0]
    ty = current_point[1] - previous_point[1]
    if tx == 0 and ty == 1:
        return [(current_point[0] + 1, current_point[1]), (current_point[0] - 1, current_point[1]),
                (current_point[0], current_point[1] + 1)]
    elif tx == 0 and ty == -1:
        return [(current_point[0] + 1, current_point[1]), (current_point[0] - 1, current_point[1]),
                (current_point[0], current_point[1] - 1)]
    elif ty == 0 and tx == 1:
        return [(current_point[0], current_point[1] + 1), (current_point[0], current_point[1] - 1),
                (current_point[0] + 1, current_point[1])]
    elif ty == 0 and tx == -1:
        return [(current_point[0], current_point[1] + 1), (current_point[0], current_point[1] - 1),
                (current_point[0] - 1, current_point[1])]
    else:
        print('error: wrong move!')
        return None


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi(os.getcwd())
    file_path = os.getcwd() + '/map.txt'
    virtual_map = read_map(file_path)
    start_point = (10, 0)
    next_point = (10, 1)
    the_way.append(start_point)
    find_way(start_point, next_point, virtual_map)

    # Step to List the way

    cps = list(map(lambda x: x.point, cross_points))
    # remove loop way or the way come to the dead end
    index = 0
    while index < len(the_way):
        if cps.count(the_way[index]) > 0:
            if the_way.count(the_way[index]) > 1:
                while the_way.count(the_way[index]) > 1:
                    del the_way[index + 1]
        index += 1

    # Only keep the turn path
    index = 0
    direct = 0  # 1 is Tx, 2 is Rx
    while index < len(the_way) - 1:
        if the_way[index][0] == the_way[index + 1][0]:
            if direct == 1:
                del the_way[index]
            else:
                direct = 1
                index += 1
                continue
        if the_way[index][1] == the_way[index + 1][1]:
            if direct == 2:
                del the_way[index]
            else:
                direct = 2
                index += 1
    print(the_way)
