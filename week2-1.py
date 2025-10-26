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
