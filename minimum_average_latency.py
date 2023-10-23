import networkx as nx


def initial_collision_vector_generator(reservation_table):
    width_rt = len(reservation_table)
    length_rt = len(reservation_table[0])
    positions = []

    for stage in range(0, width_rt):
        for time in range(0, length_rt):
            if reservation_table[stage][time] == 'X':
                positions.append((stage, time))

    bits = []
    i = 0
    j = 1
    while i != len(positions) - 1:
        if positions[i][0] == positions[j][0]:
            bits.append(positions[j][1] - positions[i][1])
        i += 1
        j += 1

    bits = [x - 1 for x in bits]

    initial_collision_vector = ''
    for i in range(0, length_rt - 1):
        if i in bits:
            initial_collision_vector += '1'
        else:
            initial_collision_vector += '0'

    return initial_collision_vector[::-1]


def state_generator(state, initial_collision_vector):
    zeros = index_of_zeros(state)

    states = []
    for i in zeros:
        states.append(or_function(shifter(state, i), initial_collision_vector))

    return states


def loop_and_edge_finder(state, initial_collision_vector):
    zeros = index_of_zeros(state)
    zeros.append(len(state) + 1)

    graph = []
    for i in zeros:
        graph.append({
            'Source': state,
            'Edge': i,
            'Destination': or_function(shifter(state, i), initial_collision_vector)
        })

    return graph


def cycle_finder(loops, edges):
    edge_list = []

    for i in loops:
        edge_list.append((i[0], i[0]))

    for j in edges:
        edge_list.append((j[0], j[2]))

    G = nx.DiGraph()
    G.add_edges_from(edge_list)
    temp = list(nx.simple_cycles(G))

    cycles = []
    for i in temp:
        if len(i) == 1:
            for j in loops:
                if i[0] == j[0]:
                    cycles.append([j[1]])
        else:
            temp_list = []
            path = path_finder(i)
            for j in path:
                for k in edges:
                    if j[0] == k[0] and j[1] == k[2]:
                        temp_list.append(k[1])
            cycles.append(temp_list)

    return cycles


def minimum_average_latency(cycles):
    average_latency = []
    for i in cycles:
        average_latency.append(sum(i) / len(i))

    return min(average_latency)


def path_finder(cycle):
    path = []
    x = 0
    y = 1
    while y != len(cycle):
        path.append((cycle[x], cycle[y]))
        x += 1
        y += 1

    path.append((cycle[-1], cycle[0]))
    return path


def index_of_zeros(state):
    result = []
    state = state[::-1]
    for i in range(0, len(state)):
        if state[i] == '0':
            result.append(i)

    result = [x + 1 for x in result]
    return result


def or_function(state, initial_collision_vector):
    result = ""
    for i in range(len(state)):
        result += str(int(state[i]) | int(initial_collision_vector[i]))

    return result


def shifter(state, shift_count):
    state = '0b' + state
    state_length = len(state)
    binary_state = int(state, 2)
    shifted_value = bin(int(binary_state) >> shift_count)

    result = ''
    for i in range(0, state_length - len(shifted_value)):
        result += '0'

    result += shifted_value[2:]
    return result


def mal_calculator(pipeline):
    initial_collision_vector = initial_collision_vector_generator(pipeline)

    all_states = [initial_collision_vector]
    for i in all_states:
        new_states = state_generator(i, initial_collision_vector)
        for j in new_states:
            if j not in all_states:
                all_states.append(j)

    graph = []
    for i in all_states:
        graph.append(loop_and_edge_finder(i, initial_collision_vector))

    loops = []
    edges = []
    for i in graph:
        for j in i:
            if j['Source'] == j['Destination']:
                loops.append(j)
            else:
                edges.append(j)

    min_loops = []
    for i in loops:
        if not min_loops:
            min_loops.append((i['Source'], i['Edge']))
        elif i['Source'] not in [x[0] for x in min_loops]:
            min_loops.append((i['Source'], i['Edge']))

    min_edges = []
    for i in edges:
        if not min_edges:
            min_edges.append((i['Source'], i['Edge'], i['Destination']))
        elif i['Source'] not in [x[0] for x in min_edges] or i['Destination'] not in [x[2] for x in min_edges]:
            min_edges.append((i['Source'], i['Edge'], i['Destination']))

    cycles = cycle_finder(min_loops, min_edges)
    mal = minimum_average_latency(cycles)
    return mal
