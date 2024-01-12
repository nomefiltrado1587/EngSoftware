
if(window.sessionStorage.getItem("AllAtOnce"))
{
    window.sessionStorage.removeItem("AllAtOnce")
}

function createAll(){
    window.sessionStorage.setItem("AllAtOnce",true)
    
    routerManager(1)
}
