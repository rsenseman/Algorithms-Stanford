import sys

def load_file(filename):
    new_table = set()
    for line in f.readlines():
        new_table.add(int(line))
    return new_table

def get_num_2sums(hash_table, lower_bound, upper_bound):
    values_remaining = set(range(lower_bound, upper_bound+1))
    for element in hash_table:
        for target in list(values_remaining):
            if target != element and target-element in hash_table:
                print(f'found {target}', end=', ')
                values_remaining.remove(target)
                print(f'{len(values_remaining)} values remaining')

    return upper_bound - lower_bound - len(values_remaining) + 1

if __name__ == '__main__':
    filename = sys.argv[1]

    with open(filename) as f:
        hash_table = load_file(f)

    num_2sums = get_num_2sums(hash_table, -10000, 10000)

    print(f'{num_2sums} targets with 2sum counterparts')
