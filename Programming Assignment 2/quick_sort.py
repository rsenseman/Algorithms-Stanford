import sys
import random


class quick_sort():
    def __init__(self, array, pivot='first'):
        self.num_comparisons = 0
        assert (pivot in ('first', 'last', 'median')), "Pivot type not \
            recognized"
        self.pivot = pivot
        self._sort(array, len(array))

    def _sort(self, array, n):
        if n > 1:
            self.num_comparisons += n - 1
            p = self._choose_pivot(array, n)
            a, b = self._partition(array)
            return self._sort(a, len(a)) + [p] + self._sort(b, len(b))
        else:
            return array

    def _choose_pivot(self, array, n):
        pivot_location = None
        if self.pivot == 'first': pivot_location = 0
        elif self.pivot == 'last': pivot_location = n - 1
        else:
            pivot_location = int(n / 2)

        # move pivot to front, move front value to index of pivot
        array[0], array[pivot_location] = array[pivot_location], array[0]
        return array[0]

    def _partition(self, array):
        pivot = array[0]
        i = 0

        for j in range(1, len(array)):
            # i marks the right-most value that is less than or equal to the
            # pivot. If x is less than or equal to the pivot, swap the value
            # x with the value at i+1 and increment the pointer i. If x is
            # greater than the pivot, continue to the next value value in
            # the array

            x = array[j]
            if x <= pivot:
                array[j], array[i + 1] = array[i + 1], array[j]
                i += 1

        return array[1:i+1], array[i+1:]


if __name__ == '__main__':
    filename = sys.argv[1]

    with open(filename) as f:
        int_list = [int(val.strip()) for val in f.readlines()]

    qs = quick_sort(int_list, 'first')
    print(qs.num_comparisons)
