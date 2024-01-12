function CreateEvent(){
    let nome = document.getElementById("name").value.trim()
    let tipo = document.getElementById("tipo").value.trim()
    let ev_status = document.getElementById("status").value.trim()
    let avaliacao = document.getElementById("avaliacao").value.trim()
    let descricao = document.getElementById("descricao").value.trim()
    let body = {
        nome,
        tipo,
        ev_status,
        avaliacao,
        descricao,
    }
    if(window.sessionStorage.getItem("AllAtOnce")){
        window.sessionStorage.setItem("eventData",JSON.stringify(body))
        routerManager(2)
        
    }
    else{
        const options = {
            method: 'POST',
            url: 'http://127.0.0.1:5000/criar',
            headers: {'Content-Type': 'application/json'},
            data: {evento:body}
            };
            console.log(body)
            axios.request(options).then(function (response) {
                id =response.data.created_id
                console.log(id)
                if(id===-1){
                    window.alert("there is alredy an event registered with  this data, please change event data and try again")
                }
                else{
                    window.alert("event was created")
                    console.log(id)
                    routerManager(0)

                }
                }).catch(function (error) {
                console.error(error);
                });
    }

}