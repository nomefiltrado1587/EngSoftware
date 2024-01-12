function createLocal(){
    let nome = document.getElementById("name").value.trim()
    let pais = document.getElementById("pais").value.trim()
    let estado = document.getElementById("estado").value.trim()
    let cidade = document.getElementById("cidade").value.trim()
    let rua = document.getElementById("rua").value.trim()
    let numero = document.getElementById("numero").value.trim()
    let complemento = document.getElementById("complemento").value.trim()

    let body = {
        nome,
        pais,
        estado,
        cidade,
        rua,
        numero,
        complemento
    }
    if(window.sessionStorage.getItem("AllAtOnce")){
        window.sessionStorage.setItem("localData",JSON.stringify(body))
        routerManager(3)
        
    }
    else{
        const options = {
            method: 'POST',
            url: 'http://127.0.0.1:5000/criar',
            headers: {'Content-Type': 'application/json'},
            data: {local:body}
            };
        
            axios.request(options).then(function (response) {
            id =response.data.created_id
            if(id===-1 || id===-2){
                window.alert("there is alredy a place register in this address, please change address data and try again")
            }
            else{
                window.alert("place was created")
                routerManager(0)
            }
            }).catch(function (error) {
            console.error(error);
            });
            

    }
}