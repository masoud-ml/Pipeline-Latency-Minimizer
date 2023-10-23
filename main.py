from operator import itemgetter
from itertools import combinations
from minimum_average_latency import mal_calculator


def translate_char(char):
    if char == 'x':
        return 'X'
    elif char == 'o':
        return ' '
    else:
        return char


def read_file(file_name):
    reservation_table = []
    row = []

    with open(file_name) as f:
        txt = list(f.read())

        for i in txt:
            if i == '\n':
                reservation_table.append(row)
                row = []
            else:
                row.append(translate_char(i))

        reservation_table.append(row)

    return reservation_table


def delay_stage_creator(x_index, stage_length):
    delay_stage = []

    for i in range(0, stage_length + 1):
        if i == x_index:
            delay_stage.append('X')
        else:
            delay_stage.append(' ')

    return delay_stage


def stage_shifter(stage, x_index):
    new_stage = stage.copy()
    new_stage.insert(x_index, ' ')
    return new_stage


def delay_inserter(reservation_table, delay_location):
    new_reservation_table = []
    stage_len = len(reservation_table[0])

    if delay_location > len(reservation_table) - 1:
        x_index = reservation_table[delay_location - 1].index('X') + 1
        for i in range(0, len(reservation_table)):
            new_reservation_table.append(stage_shifter(reservation_table[i], x_index))

        new_reservation_table.append(delay_stage_creator(x_index, stage_len))

    else:
        x_index = reservation_table[delay_location].index('X')
        for i in range(0, len(reservation_table)):
            if i == delay_location:
                new_reservation_table.append(delay_stage_creator(x_index, stage_len))

            new_reservation_table.append(stage_shifter(reservation_table[i], x_index))

    return new_reservation_table


def combinations_to_list(all_combinations):
    result = []

    for combination in all_combinations:
        for element in map(list, combination):
            result.append(element)

    return result


def main():
    # input files --> {'sample1', 'sample2', 'sample3'}

    file_name = 'sample1'
    reservation_table = read_file(file_name + '.txt')

    print("Original pipeline:\n")
    mal = mal_calculator(reservation_table)
    print('MAL = ' + str(mal))
    print('Reservation Table:')
    for i in reservation_table:
        print(i)

    print()
    print('+----------------------------------------------------------------------+')
    print('+----------------------------------------------------------------------+')
    print()

    combs = []
    for i in range(1, len(reservation_table) + 2):
        combs.append(combinations(list(range(len(reservation_table) + 1)), i))

    combs_list = combinations_to_list(combs)

    all_reservation_table = []
    for i in combs_list:
        if len(i) == 1:
            new_rt = delay_inserter(reservation_table, i[0])
            all_reservation_table.append({
                'Reservation_table': new_rt,
                'Delay_location': i,
                'MAL': mal_calculator(new_rt),
            })

        else:
            is_first = True
            new_rt = []

            for j in i:
                if is_first:
                    new_rt = delay_inserter(reservation_table, j)
                    is_first = False
                else:
                    new_rt = delay_inserter(new_rt, j + 1)

            all_reservation_table.append({
                'Reservation_table': new_rt,
                'Delay_location': i,
                'MAL': mal_calculator(new_rt),
            })

    print("Delay inserted pipelines:\n")
    all_reservation_table = sorted(all_reservation_table, key=itemgetter('MAL'))

    for i in all_reservation_table:
        print("MAL: " + str(i['MAL']))
        print("Delay location: " + str(i['Delay_location']))

        print('Reservation Table:')
        for j in i['Reservation_table']:
            print(j)

        print()

    print('+----------------------------------------------------------------------+')
    print('+----------------------------------------------------------------------+')


if __name__ == '__main__':
    main()
