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