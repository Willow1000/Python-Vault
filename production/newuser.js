const newUser = ()=>{
    const fs = require("fs")
    const fsPromises = require("fs/promises")
    const myInput = require("prompt-sync")()
    const name = myInput("Enter your name: ".toUpperCase())
    const {lock} = require('./cryptotest')
    const password = myInput("Set Your Vault password: ".toUpperCase())
    let confPassword = myInput("Confirm Your Password: ".toUpperCase())
    let count = 3
    while ((confPassword !== password) && (count > 0)) {
        count--;
        console.log(`Password mismatch ${count} more trials remaining`);
        confPassword = myInput("Confirm Your Password: ".toUpperCase())

        if (count === 0) {
            console.log("Maximum number of attempts reached please try again later");
            break;
        }
    }
    if(password === confPassword){
        console.log("Answer the following emergency questions to finish")
        const city = myInput("in which city were you born? ".toUpperCase())
        const nickname = myInput("what was your childhood nickname? ".toUpperCase())
        const color = myInput("what is your favourite color? ".toUpperCase())
        const securityInfo = [{name: name,passwd:password,city:city,nickname:nickname,color:color}]
        fsPromises.mkdir("./VAULT")
        lock(securityInfo)
    }

    

    
}

exports.newUser = newUser