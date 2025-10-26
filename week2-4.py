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
