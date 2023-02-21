from queue import Queue


def movements_finder(pos: tuple, rows) -> list:
    """
    This functions generates the movements vectors according to the size of the squared board
    :param pos: the reference to calc the movmentes
    :param rows: number of rows in the board
    :return:
        list: List that contains posible movements

    """

    movements_vectors = ((2, 1), (1, 2))

    movments = []

    for vector in movements_vectors:
        for i in (+1, -1):
            for j in (+1, -1):

                x_pos = pos[0] + vector[0] * i
                y_pos = pos[1] + vector[1] * j
                if x_pos < 0 or y_pos < 0 or x_pos >= rows or y_pos >= rows:
                    continue
                else:
                    movments.append((x_pos, y_pos))

    return movments


def end_movements_back(table, end) -> dict:
    """
    This function takes cares of calcs in a deep of three from the end the movements posibilites
    :param table: Table of references
    :param end: End pos
    :return:
        A dictonary that references the las pos
    """

    queue = Queue()
    queue.put(end)
    tablero = table.tablero
    movements = {f"{end[0]}_{end[1]}": ""}

    for reps in range(2):
        for positions in list(queue.queue):
            moves = movements_finder(positions, table.rows)
            for i in moves:
                queue.get()
                queue.put(i)
                if f"{i[0]}_{i[1]}" not in movements:
                    movements[f"{i[0]}_{i[1]}"] = f"{positions[0]}_{positions[1]}"
                tablero[i[0]][i[1]].path_finded = True

    return movements


def horse_pathfinder(table, start, end):
    """
    This function takes cares of finding the path of the horse use a similiar algorithm to bfs.
    :param table: table in reference
    :param start: start point
    :param end: end point
    :return:
        returns a list with the coord of the path in a sorted sequence
    """
    end_movements = end_movements_back(table, end)
    queue = Queue()
    queue.put(start)
    movements = {f"{start[0]}_{start[1]}": ""}
    junction = None

    run = True
    while run:
        for positions in list(queue.queue):
            queue.get()
            if f"{positions[0]}_{positions[1]}" in end_movements:
                junction = f"{positions[0]}_{positions[1]}"
                run = False
                break
            moves = movements_finder(positions, table.rows)
            for i in moves:
                queue.put(i)
                if f"{i[0]}_{i[1]}" not in movements:
                    movements[f"{i[0]}_{i[1]}"] = f"{positions[0]}_{positions[1]}"

    res_list = []

    actual = junction
    while True:
        res_list.append(actual)
        if movements[actual] == '':
            break
        else:
            actual = movements[actual]

    res_list.reverse()

    actual = junction
    while True:
        res_list.append(actual)
        if end_movements[actual] == '':
            break
        else:
            actual = end_movements[actual]

    res_list.pop(res_list.index(junction))
    return res_list
