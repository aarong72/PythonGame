def binary_search(lists, item):
    low = 0
    high = len(lists) - 1

    while low <= high:
        mid = int((low + high) // 2)  # in order to start in the middle of the list we must divide the last list place by 2


        if lists[mid] == item:
            return mid

        if lists[mid] > item:
            high = mid - 1

        else:
            low = mid + 1


my_list = [1, 3, 5, 7, 9]

print(binary_search(my_list, 7))

