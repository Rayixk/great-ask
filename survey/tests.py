# 二分查找法--区间逼近:每次用中间数的值和目标值对比,如果中间值比目标值大,high直接取到mid-1,如果中间值比目标值小,low直接取到mid+1
def bin_search(li, val):
    low = 0
    high = len(li) - 1
    while low <= high:
        mid = (low + high) // 2
        mid_val = li[mid]
        if mid_val == val:
            return mid
        elif mid_val < val:
            low = mid + 1
        elif mid_val > val:
            high = mid - 1

    return -1


# index = bin_search(range(1, 100000, 3), 99886)
# print(index)

# 冒泡排序
def bubble_sort(li):
    for i in range(len(li) - 1):  # 趟数
        for j in range(len(li) - i - 1):  # 比较区间
            if li[j] > li[j + 1]:  # 如果前一个数比,后一个数大,俩数交换,这样每执行一次,大的数慢慢往上移动,
                li[j + 1], li[j] = li[j], li[j + 1]

# l=list(range(1,10000,3))
# import random
# random.shuffle(l)
# print(l)
# bubble_sort(l)
# print(l)

li=[1,2,3,4].sort()
