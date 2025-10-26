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
