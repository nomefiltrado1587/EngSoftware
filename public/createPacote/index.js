function createPack(){
    let nome = document.getElementById("name").value.trim()
    let dia = document.getElementById("dia").value.trim()
    let preco = document.getElementById("preco").value.trim()

    let body = {
        nome,
        dia,
        preco,
    }

    if(window.sessionStorage.getItem("AllAtOnce")){
        window.sessionStorage.setItem("packData",JSON.stringify(body))
        routerManager(4)
        
    }
    else{
        const options = {
            method: 'POST',
            url: 'http://127.0.0.1:5000/criar',
            headers: {'Content-Type': 'application/json'},
            data: {pacote:body}
            };
        
            axios.request(options).then(function (response) {
                id =response.data.created_id
                if(id===-1 || id===-2){
                    window.alert("there is alredy a package  with this data registered in the database, please change package data and try again")
                }
                else{
                    window.alert("package was created")
                    routerManager(0)
                }
                }).catch(function (error) {
                console.error(error);
                });

    }

}