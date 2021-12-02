if(document.getElementById("btn-encrypt")) {
    document.getElementById("btn-encrypt").addEventListener("click", async (event)=>{
        console.log("click encrypt");
        let file = globalThis.clickFunctions.chooseAnyFile();
        let res = await file;
        let path =  await res.filePaths;
        const isCanceled = await res.canceled ; 
        if(!isCanceled) {
            globalThis.clickFunctions.encrypt(path[0]);
            globalThis.clickFunctions.onMessage((msg) => {
                const infoArr = msg.split('\n\n');
                document.getElementById("info").innerHTML = `${infoArr[0]}</br>`;
                if(infoArr[1]){
                    document.getElementById("info").innerHTML += `${infoArr[1]}`
                }
            });
            
        }
    })

    document.getElementById("btn-decrypt").addEventListener("click", async()=>{
        console.log("click decrypt");
        
        let file = globalThis.clickFunctions.chooseFilterFile();
        let res = await file;
        let path =  await res.filePaths;
        const isCanceled = await res.canceled ; 
        if(!isCanceled) {
            globalThis.clickFunctions.decrypt(path[0]);
            globalThis.clickFunctions.onMessage((msg) => {
                const infoArr = msg.split('\n\n');
                document.getElementById("info").innerHTML = `${infoArr[0]}</br>`;
                if(infoArr[1]){
                    document.getElementById("info").innerHTML += `${infoArr[1]}`
                }
            });
        }
    })
}

if(document.getElementById("btn-registrate")) {
    document.getElementById("btn-registrate").addEventListener("click", ()=>{
        console.log("click resistrate");
        globalThis.clickFunctions.registrate();
        document.getElementById("registration-message").innerHTML = "You are registarted";
    
        document.getElementById("registration-message").classList.remove("error");
        document.getElementById("registration-message").classList.add("ok");
    
        document.getElementById("btn-registrate").setAttribute("disabled", "disabled");
        document.getElementById("btn-registrate").classList.remove("yellowButton");
    
        globalThis.clickFunctions.redirect();
    })
    
}

