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