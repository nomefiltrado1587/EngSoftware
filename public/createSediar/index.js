if(window.sessionStorage.getItem("AllAtOnce")){
    var createdEvent = JSON.parse(window.sessionStorage.getItem("eventData"))
    var createdLocal = JSON.parse(window.sessionStorage.getItem("localData"))
    var createdPack = JSON.parse(window.sessionStorage.getItem("packData"))
    console.log(createdEvent)
    console.log(createdLocal)
    console.log(createdPack)
    container = document.getElementById("container-info")
    console.log(container)
    container.appendChild(ObjctToElement(createdEvent,"event Data"))
    container.appendChild(ObjctToElement(createdLocal,"local Data"))
    container.appendChild(ObjctToElement(createdPack,"pack Data"))
    
}
else{
    form = document.getElementById("Form")
    let eventId = document.createElement("input")
    eventId.required = true
    eventId.type="text"
    eventId.id="eventId"
    eventId.placeholder="eventId"
    form.appendChild(eventId)
    let placeId = document.createElement("input")
    placeId.type="text"
    placeId.required=true
    placeId.id="placeId"
    placeId.placeholder="PlaceId"
    form.appendChild(placeId)
    let packId = document.createElement("input")
    packId.type="text"
    packId.required=true
    packId.id="packId"
    packId.placeholder="packId"
    form.appendChild(packId)
    let containerInfo = document.getElementById("container-info")
    containerInfo.className="column"
    let localContainer = document.createElement("div")
    let eventContainer = document.createElement("div")
    let packageContainer = document.createElement("div")
    eventContainer.id="event-container"
    packageContainer.id="package-container"
    localContainer.id="local-container"
    containerInfo.appendChild(eventContainer)
    containerInfo.appendChild(localContainer)
    containerInfo.appendChild(packageContainer)
    getEvents(eventContainer)
    getLocais(localContainer)
    getPackages(packageContainer)

}


async function hostEvent() {
    let eventId,localId,packId
    if(window.sessionStorage.getItem("AllAtOnce")){
        const eventData = {
            method: 'POST',
            url: 'http://127.0.0.1:5000/criar',
            headers: {'Content-Type': 'application/json'},
            data: {evento:createdEvent}
            };
            const localData = {
                method: 'POST',
                url: 'http://127.0.0.1:5000/criar',
                headers: {'Content-Type': 'application/json'},
                data: {local:createdLocal}
                };
            const packData = {
                method: 'POST',
                url: 'http://127.0.0.1:5000/criar',
                headers: {'Content-Type': 'application/json'},
                data: {pacote:createdPack}
                };

            try{
                eventResponse = await axios.request(eventData)
                eventId = eventResponse.data.created_id
                if(eventId===-1){
                    window.alert("there is alredy an event registered with  this data, please change event data and try again")
                }
                console.log(eventId)
                localResponse = await axios.request(localData)
                localId = localResponse.data.created_id
                if(localId===-1){
                    window.alert("there is alredy a place register in this address, please change address data and try again")
                }
                console.log(localId)
                packResponse = await axios.request(packData)
                packId = packResponse.data.created_id
                if(packId===-1){
                    window.alert("there is alredy a package  with this data registered in the database, please change package data and try again")
                }
                console.log(packId)
                      
            }
            catch(error){
                console.log(error)
            }
            
 
    }
    else{
        eventId = document.getElementById("eventId").value
        localId = document.getElementById("placeId").value
        packId = document.getElementById("packId").value
    }

    const sediarData = {
        method: 'POST',
        url: 'http://127.0.0.1:5000/criar',
        headers: {'Content-Type': 'application/json'},
        data: {Sediar: {event_id: eventId.toString(), pack_id: packId.toString(), local_id: localId.toString()}}
        };
    response = await axios.request(sediarData).catch(function (error) {
        console.error(error);
        });
    console.log(response.data)
    window.alert("Evento foi sediado com sucesso")
    routerManager(0)
}



function ObjctToElement(data,title){
    let div = document.createElement("div");
    div.className="bigData"
    let displayTitle = document.createElement("h2")
    displayTitle.appendChild(document.createTextNode(title))
    div.appendChild(displayTitle)
    Object.keys(data).forEach(element => {
        let innerP = document.createElement("p")
        innerP.className="dataAttribute"
        let div1 = document.createElement("div")
        div1.className="attributeName"
        div1.textContent += element
        let div2 = document.createElement("div")
        div2.className="attributeValue"
        div2.textContent+= data[element]
        innerP.appendChild(div1)
        innerP.appendChild(div2)
        div.appendChild(innerP)
    });
    return div
}

function getEvents(resultContainer){
    const options = {
        method: 'PATCH',
        url: 'http://127.0.0.1:5000/busca',
        headers: {'Content-Type': 'application/json'},
        data: {evento: {nome: '', tipo: '', ev_status: '', avaliacao: '', descricao: ''}}
      };
      
      axios.request(options).then(function (response) {
        console.log(response.data);
        response.data.forEach(queryResult => {
            let dataDiv = document.createElement("div")
            dataDiv.className="box-item"
            let evento = getDataEvento(queryResult)
            dataDiv.appendChild(ObjctToElement(evento,"evento"))
            resultContainer.appendChild(dataDiv)
        });
        }).catch(function (error) {
        console.error(error);
        });
}

function getLocais(resultContainer){
    const options = {
        method: 'PATCH',
        url: 'http://127.0.0.1:5000/busca',
        headers: {'Content-Type': 'application/json'},
        data: {
          local: {
            nome: '',
            pais: '',
            estado: '',
            cidade: '',
            rua: '',
            numero: '',
            complemento: ''
          }
        }
      };
      
      axios.request(options).then(function (response) {
        console.log(response.data);
        response.data.forEach(queryResult => {
            let dataDiv = document.createElement("div")
            dataDiv.className="box-item"
            let local = getDataLocal(queryResult)
            dataDiv.appendChild(ObjctToElement(local,"local"))
            resultContainer.appendChild(dataDiv)
        });
        }).catch(function (error) {
        console.error(error);
        });
}

function getPackages(resultContainer){
    const options = {
        method: 'PATCH',
        url: 'http://127.0.0.1:5000/busca',
        headers: {'Content-Type': 'application/json'},
        data: {pacote: {nome: '', dia: '', preco: ''}}
      };
      
      axios.request(options).then(function (response) {
        console.log(response.data);
        response.data.forEach(queryResult => {
            let dataDiv = document.createElement("div")
            dataDiv.className="box-item"
            let pacotes = getDataPacote(queryResult)
            dataDiv.appendChild(ObjctToElement(pacotes,"pacotes"))
            resultContainer.appendChild(dataDiv)
        });
        }).catch(function (error) {
        console.error(error);
        });
    }

function filtrarNull(obj){
    Object.keys(obj).forEach((key)=>{
        if(obj[key]===null){
            delete obj[key]
        }
    })
}


function getDataEvento(data){
    let evento = {
		avaliacao: data["Det_eventos.avaliacao"],
		descricao: data["Det_eventos.descricao"],
		ev_status: data["Det_eventos.ev_status"],
        id: data["Eventos.event_id"],
		nome: data["Eventos.nome"],
		tipo: data["Det_eventos.tipo"]
	}
    filtrarNull(evento)
    return evento
}

function getDataLocal(data){
    let local= {
        cidade:data["Enderecos.cidade"],
        estado:data["Enderecos.estado"],
        pais:data["Enderecos.pais"],
        id:data["Locais.local_id"],
        rua:data["Enderecos.rua"],
        numero:data["Enderecos.numero"],
        complemento:data["Enderecos.complemento"],
        nome:data["Locais.nome"]
    }
    filtrarNull(local)
    return local
}
function getDataPacote(data){
    let pacote ={
        id:data["Pacotes.pack_id"],
        dia: data["Pacotes.dia"],
        preco: data["Pacotes.preco"],
        nome: data["Pacotes.nome"]
    }
    filtrarNull(pacote)
    return pacote
}