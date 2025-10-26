# task1

def way(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def func1(begin):

    points = {
        "貝吉塔": (-4, -1),
        "悟空": (0, 0),
        "辛巴": (-3, 3),
        "特南克斯": (1, -2),
        "弗利沙": (4, -1),
        "丁滿": (-1, 4)
    }

    groupA = ["貝吉塔", "悟空", "特南克斯", "辛巴"]
    groupB = ["弗利沙", "丁滿"]

    if begin not in points:
        print("錯誤！請輸入以下角色之一：", list(points.keys()))
        return

    distance = {}

    for name, coord in points.items():
        d = way(points[begin], coord)

        if (begin in groupA and name in groupB) or (begin in groupB and name in groupA):
            d = d + 2

        distance[name] = d

    closest_names = []
    farthest_names = []
    min_dist = None
    max_dist = None

    for name, d in distance.items():
        if name == begin:
            continue
        if min_dist is None or d < min_dist:
            min_dist = d
            closest_names = [name]
        elif d == min_dist:
            closest_names.append(name)

        if max_dist is None or d > max_dist:
            max_dist = d
            farthest_names = [name]
        elif d == max_dist:
            farthest_names.append(name)

    closest_str = "、".join(closest_names)
    farthest_str = "、".join(farthest_names)

    print("最遠" + farthest_str + ",最近" + closest_str)


func1("辛巴")  # print 最遠弗利沙；最近丁滿、⾙吉塔
func1("悟空")  # print 最遠丁滿、弗利沙；最近特南克斯
func1("弗利沙")  # print 最遠⾟巴，最近特南克斯
func1("特南克斯")  # print 最遠丁滿，最近悟空


# task2

def func2(services, start, end, criteria, bookings):
    def availabletime(name):
        for rs, re in bookings[name]:
            # rs=已預約起始時間 re=已預約結束時間
            if start < re and end > rs:
                return False
        return True

    criteria = criteria.replace(" ", "")
    chosen = None

    if ">=" in criteria:
        field, value = criteria.split(">=")
        if field not in ("r", "c"):
            print("Sorry")
            return
        value = float(value)

        okopt = [
            rs for rs in services
            if availabletime(rs["name"]) and rs[field] >= value
        ]
        if okopt:
            chosen = min(okopt, key=lambda rs: rs[field] - value)

    elif "<=" in criteria:
        field, value = criteria.split("<=")
        if field not in ("r", "c"):
            print("Sorry")
            return
        value = float(value)

        okopt = [
            rs for rs in services
            if availabletime(rs["name"]) and rs[field] <= value
        ]
        if okopt:
            chosen = min(okopt, key=lambda rs: value - rs[field])

    elif "=" in criteria:
        field, value = criteria.split("=")

        if field != "name":
            print("Sorry")
            return
        okopt = [
            rs for rs in services
            if availabletime(rs["name"]) and str(rs[field]) == value
        ]
        if okopt:
            chosen = okopt[0]

    if chosen:
        print(chosen["name"])
        bookings[chosen["name"]].append((start, end))
    else:
        print("Sorry")


services = [
    {"name": "S1", "r": 4.5, "c": 1000},
    {"name": "S2", "r": 3.0, "c": 1200},
    {"name": "S3", "r": 3.8, "c": 800}
]

bookings = {
    "S1": [],
    "S2": [],
    "S3": []
}

func2(services, 15, 17, "c>=800", bookings)  # S3
func2(services, 11, 13, "r<=4", bookings)  # S3
func2(services, 10, 12, "name=S3", bookings)  # Sorry
func2(services, 15, 18, "r>=4.5", bookings)  # S1
func2(services, 16, 18, "r>=4", bookings)  # Sorry
func2(services, 13, 17, "name=S1", bookings)  # Sorry
func2(services, 8, 9, "c<=1500", bookings)  # S2


# task3
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

# task4


def func4(sp, stat, n):
    def difference(value):
        return abs(value - n)

    available = [sp[i] for i in range(len(sp)) if stat[i] == "0"]

    if not available:
        print("No available car")
        return

    Ans = min(available, key=difference)
    car = sp.index(Ans)
    print(car)


func4([3, 1, 5, 4, 3, 2], "101000", 2)
func4([1, 0, 5, 1, 3], "10100", 4)
func4([4, 6, 5, 8], "1000", 4)
