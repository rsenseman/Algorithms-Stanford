import sys


def count_inversions(array):
    '''return the number of inversions in given array'''

    # if the array is of length 0 or 1, return the array with guaranteed number
    # of inversions, 0
    #
    # if the array is of length longer than 2, split the array in two and
    # count the inversions in each half before returning the sorted array
    # and number of inversions via merge-sort
    array_length = len(array)
    if array_length < 2:
        return sorted(array), 0
    else:
        array_midpoint = int(array_length/2)
        sorted_array_left, num_inversions_left = count_inversions(array[:array_midpoint])
        sorted_array_right, num_inversions_right = count_inversions(array[array_midpoint:])

        sorted_array, num_inversions_at_node = merge_and_sort(sorted_array_left, sorted_array_right)

        total_inversions = num_inversions_at_node + \
                           num_inversions_left + \
                           num_inversions_right

        return sorted_array, total_inversions


def merge_and_sort(sorted_array_left, sorted_array_right):
    '''merge and sort two arrays, returning both the given array and the number
    of inversions incurred during merge
    '''

    len_left = len(sorted_array_left)
    len_right = len(sorted_array_right)

    pointer_left = 0
    pointer_right = 0
    sorted_array = []
    num_inversions = 0

    # print(f'{sorted_array_left}, {sorted_array_right}')

    for _ in range(len_left + len_right):
        # print(sorted_array)

        # if the left array is exhausted, append remaining right array
        if pointer_left >= len_left:
            sorted_array.extend(sorted_array_right[pointer_right:])
            break

        # if the right array is exhausted, append remaining left array
        if pointer_right >= len_right:
            sorted_array.extend(sorted_array_left[pointer_left:])
            break

        # if both arrays have values remaining: compare the values at the
        # "front", if the left value is greater, append it to the sorted
        # array. If the right value is greater append it and increment
        # num_inversions by the number of values remaining in the left
        # array
        value_left = sorted_array_left[pointer_left]
        value_right = sorted_array_right[pointer_right]

        if value_left <= value_right:
            sorted_array.append(value_left)
            pointer_left += 1
        else:
            sorted_array.append(value_right)
            pointer_right += 1
            num_inversions += len_left - pointer_left

    # print(f'{sorted_array}, {num_inversions}')
    return sorted_array, num_inversions


if __name__ == '__main__':
    filename = sys.argv[1]

    with open(filename) as f:
        int_list = [int(val.strip()) for val in f.readlines()]

    sorted_array, num_inversions = count_inversions(int_list)
    print(num_inversions)
