
//task1 

function way(p1, p2) {
    return Math.abs(p1[0] - p2[0]) + Math.abs(p1[1] - p2[1]);
}

function func1(begin) {
    const points = {
        "貝吉塔": [-4, -1],
        "悟空": [0, 0],
        "辛巴": [-3, 3],
        "特南克斯": [1, -2],
        "弗利沙": [4, -1],
        "丁滿": [-1, 4]
    };


    const groupA = ["貝吉塔", "悟空", "特南克斯", "辛巴"];
    const groupB = ["弗利沙", "丁滿"];


    if (!(begin in points)) {
        console.log("錯誤！請輸入以下角色之一：", Object.keys(points));
        return;
    }


    const distance = {};

    for (let name in points) {
        const d = way(points[begin], points[name]);

        let adjusted = d;

        if ((groupA.includes(begin) && groupB.includes(name)) ||
            (groupB.includes(begin) && groupA.includes(name))) {
            adjusted += 2;
        }

        distance[name] = adjusted;
    }


    let minDist = null;
    let maxDist = null;
    let closestNames = [];
    let farthestNames = [];

    for (let name in distance) {
        if (name === begin) continue;

        const d = distance[name];


        if (minDist === null || d < minDist) {
            minDist = d;
            closestNames = [name];
        } else if (d === minDist) {
            closestNames.push(name);
        }


        if (maxDist === null || d > maxDist) {
            maxDist = d;
            farthestNames = [name];
        } else if (d === maxDist) {
            farthestNames.push(name);
        }
    }


    const closestStr = closestNames.join("、");
    const farthestStr = farthestNames.join("、");

    console.log(`最遠${farthestStr},最近${closestStr}`);
}


func1("辛巴"); // print 最遠弗利沙；最近丁滿、⾙吉塔
func1("悟空"); // print 最遠丁滿、弗利沙；最近特南克斯
func1("弗利沙"); // print 最遠⾟巴，最近特南克斯
func1("特南克斯"); // print 最遠丁滿，最近悟空



//task2
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



//task3

function func3(index) {
    let nums = [25];
    let dif = [-2, -3, 1, 2];

    for (let i = 0; i < index; i++) {
        let d = dif[i % 4];
        nums.push(nums[nums.length - 1] + d);
    }

    console.log(nums[index]);
}


func3(1); // print 23
func3(5); // print 21
func3(10); // print 16
func3(30); // print 6


//task4

function func4(sp, stat, n) {
    function difference(value) {
        return Math.abs(value - n);
    }

    let available = [];
    for (let i = 0; i < sp.length; i++) {
        if (stat[i] === "0") {
            available.push(sp[i]);
        }
    }

    if (available.length === 0) {
        console.log("No available car");
        return;
    }

    let ans = available[0];
    for (let i = 1; i < available.length; i++) {
        if (difference(available[i]) < difference(ans)) {
            ans = available[i];
        }
    }


    let car = sp.indexOf(ans);
    console.log(car);
}


func4([3, 1, 5, 4, 3, 2], "101000", 2);
func4([1, 0, 5, 1, 3], "10100", 4);
func4([4, 6, 5, 8], "1000", 4);
