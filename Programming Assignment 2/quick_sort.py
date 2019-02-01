import sys
# use numpy to enable in-place sorting. Info on lists vs. numpy arrays
# here: https://webcourses.ucf.edu/courses/1249560/pages/python-lists-vs-numpy-arrays-what-is-the-difference
import numpy as np
import random


class quick_sort():
    def __init__(self, array, pivot='random'):
        self.num_comparisons = 0
        assert (pivot in ('first', 'last', 'median', 'random')), "Pivot type not \
            recognized"
        self.pivot = pivot
        self.array = np.array(array)
        self._sort(self.array, len(array))

    def _sort(self, array, n):
        if n > 1:
            self.num_comparisons += n - 1

            self._choose_pivot(array, n)  # move pivot to front of array
            pivot_final_location = self._partition(array)
            a, b = array[0: pivot_final_location], array[pivot_final_location+1:]

            self._sort(a, len(a))
            self._sort(b, len(b))

            return None

        else:
            return None

    def _choose_pivot(self, array, n):
        if self.pivot == 'first': pivot_location = 0
        elif self.pivot == 'last': pivot_location = n - 1
        elif self.pivot == 'random': pivot_location = random.randint(0, n - 1)
        else:
            first_val = array[0]
            last_val = array[-1]
            if n % 2 == 0:
                middle_index = int(n/2 - 1)
            else:
                middle_index = int(n / 2.0)
            middle_val = array[middle_index]

            # go through all possibilities to determine the median of the
            # three values: first, last and middle.
            if first_val < last_val:
                if first_val > middle_val:
                    pivot_location = 0
                else:
                    if middle_val < last_val:
                        pivot_location = middle_index
                    else:
                        pivot_location = n - 1
            else:
                if last_val > middle_val:
                    pivot_location = n - 1
                else:
                    if middle_val < first_val:
                        pivot_location = middle_index
                    else:
                        pivot_location = 0

        # move pivot to front, move front to space vacated by pivot
        array[0], array[pivot_location] = array[pivot_location], array[0]
        return array[0]

    def _partition(self, array):
        pivot = array[0]
        # i marks the left-most value that is more than the pivot.
        i = 1

        for j in range(1, len(array)):
            # If array[j] is less than or equal to the pivot, swap the
            # value at j with the value at i and increment the value of  i.
            # If x is greater than the pivot, continue to the next value
            # in the array
            if array[j] <= pivot:
                array[j], array[i] = array[i], array[j]
                i += 1

        # After the loop has run, i marks one to the right of where the pivot
        # should be placed. Position the pivot in its correct place before
        # returning
        array[i-1], array[0] = array[0], array[i-1]
        return i-1


if __name__ == '__main__':
    filename = sys.argv[1]

    with open(filename) as f:
        int_list = [int(val.strip()) for val in f.readlines()]

    qs = quick_sort(int_list, 'random')
    print(qs.num_comparisons)
