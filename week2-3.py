def func3(index):
    nums = [25]
    dif = [-2, -3, 1, 2]
    for i in range(index):
        d = dif[i % 4]
        nums.append(nums[-1] + d)
    print(nums[index])


func3(1)  # print 23
func3(5)  # print 21
func3(10)  # print 16
func3(30)  # print 6
