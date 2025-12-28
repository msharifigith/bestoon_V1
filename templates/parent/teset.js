let now = new Date().getHours()
    let time = prompt("enter tiem :",now.toString())
    const hours = new Date().setHours(+time);
     
    console.log(now)
    if (hours < 12) {
        console.log("god mording  ");
    }
    else if (hours<18){
        console.log("god afternoon")
    }
    else {
        console.log("god night ")
    }
