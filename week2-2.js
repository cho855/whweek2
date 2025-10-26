function availableTime(name, start, end, bookings) {
    var list = bookings[name];
    for (var i = 0; i < list.length; i++) {
        var rs = list[i][0];
        var re = list[i][1];
        if (start < re && end > rs) {
            return false;
        }
    }
    return true;
}

function func2(services, start, end, criteria, bookings) {
    criteria = criteria.replace(/\s+/g, "");
    var chosen = null;

    if (criteria.indexOf(">=") !== -1) {
        var parts1 = criteria.split(">=");
        var field1 = parts1[0];
        var value1 = parseFloat(parts1[1]);
        if (field1 !== "r" && field1 !== "c") {
            console.log("Sorry");
            return;
        }
        var bestDiff1 = Infinity;
        for (var i = 0; i < services.length; i++) {
            var rs1 = services[i];
            if (!availableTime(rs1.name, start, end, bookings)) continue;
            var v1 = rs1[field1];
            if (v1 >= value1) {
                var diff1 = v1 - value1;
                if (diff1 < bestDiff1) {
                    bestDiff1 = diff1;
                    chosen = rs1;
                }
            }
        }
    } else if (criteria.indexOf("<=") !== -1) {
        var parts2 = criteria.split("<=");
        var field2 = parts2[0];
        var value2 = parseFloat(parts2[1]);
        if (field2 !== "r" && field2 !== "c") {
            console.log("Sorry");
            return;
        }
        var bestDiff2 = Infinity;
        for (var j = 0; j < services.length; j++) {
            var rs2 = services[j];
            if (!availableTime(rs2.name, start, end, bookings)) continue;
            var v2 = rs2[field2];
            if (v2 <= value2) {
                var diff2 = value2 - v2;
                if (diff2 < bestDiff2) {
                    bestDiff2 = diff2;
                    chosen = rs2;
                }
            }
        }
    } else if (criteria.indexOf("=") !== -1) {
        var parts3 = criteria.split("=");
        var field3 = parts3[0];
        var value3 = parts3[1];
        if (field3 !== "name") {
            console.log("Sorry");
            return;
        }
        for (var k = 0; k < services.length; k++) {
            var rs3 = services[k];
            if (rs3.name === value3 && availableTime(rs3.name, start, end, bookings)) {
                chosen = rs3;
                break;
            }
        }
    }

    if (chosen) {
        console.log(chosen.name);
        bookings[chosen.name].push([start, end]);
    } else {
        console.log("Sorry");
    }
}

var services = [
    { name: "S1", r: 4.5, c: 1000 },
    { name: "S2", r: 3.0, c: 1200 },
    { name: "S3", r: 3.8, c: 800 }
];

var bookings = {
    "S1": [],
    "S2": [],
    "S3": []
};

func2(services, 15, 17, "c>=800", bookings);
func2(services, 11, 13, "r<=4", bookings);
func2(services, 10, 12, "name=S3", bookings);
func2(services, 15, 18, "r>=4.5", bookings);
func2(services, 16, 18, "r>=4", bookings);
func2(services, 13, 17, "name=S1", bookings);
func2(services, 8, 9, "c<=1500", bookings);
