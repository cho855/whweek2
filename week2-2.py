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
