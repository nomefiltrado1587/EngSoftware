function search(){
    let resultContainer = document.getElementById("result")
    resultContainer.innerHTML=''
    let nome = document.getElementById("name_event").value.trim()
    let tipo = document.getElementById("tipo").value.trim()
    let ev_status = document.getElementById("status").value.trim()
    let avaliacao = document.getElementById("avaliacao").value.trim()
    let descricao = document.getElementById("descricao").value.trim()
    let evento = {
        nome,
        tipo,
        ev_status,
        avaliacao,
        descricao,
    }
    let name_place = document.getElementById("name_place").value.trim()
    let pais = document.getElementById("pais").value.trim()
    let estado = document.getElementById("estado").value.trim()
    let cidade = document.getElementById("cidade").value.trim()
    let rua = document.getElementById("rua").value.trim()
    let numero = document.getElementById("numero").value.trim()
    let complemento = document.getElementById("complemento").value.trim()

    let local = {
        nome:name_place,
        pais,
        estado,
        cidade,
        rua,
        numero,
        complemento
    }
    let name_pack = document.getElementById("name_pack").value.trim()
    let dia = document.getElementById("dia").value.trim()
    let preco = document.getElementById("preco").value.trim()

    let pacote = {
        nome:name_pack,
        dia,
        preco,
    }

    let query = {
        evento:evento,
        local:local,
        pacote:pacote
    }

    console.log(query)
    const options = {
        method: 'PATCH',
        url: 'http://127.0.0.1:5000/busca',
        headers: {'Content-Type': 'application/json'},
        data: query
        };

    axios.request(options).then(function (response) {
        console.log(response.data);
        response.data.forEach(queryResult => {
            let EventDiv = document.createElement("div")
            EventDiv.className="box-item"
            local = getDataLocal(queryResult)
            evento = getDataEvento(queryResult)
            pacote = getDataPacote(queryResult)
            EventDiv.appendChild(ObjctToElement(local,"local"))
            EventDiv.appendChild(ObjctToElement(evento,"evento"))
            EventDiv.appendChild(ObjctToElement(pacote,"pacote"))
            resultContainer.appendChild(EventDiv)
        });
        }).catch(function (error) {
        console.error(error);
        });
}

function getDataLocal(data){
    let local= {
        cidade:data["Enderecos.cidade"],
        estado:data["Enderecos.estado"],
        pais:data["Enderecos.pais"],
        rua:data["Enderecos.rua"],
        numero:data["Enderecos.numero"],
        complemento:data["Enderecos.complemento"],
        nome:data["Locais.nome"]
    }
    filtrarNull(local)
    return local
}

function getDataEvento(data){
    let evento = {
		avaliacao: data["Det_eventos.avaliacao"],
		descricao: data["Det_eventos.descricao"],
		ev_status: data["Det_eventos.ev_status"],
		nome: data["Eventos.nome"],
		tipo: data["Det_eventos.tipo"]
	}
    filtrarNull(evento)
    return evento
}
function getDataPacote(data){
    let pacote ={
        dia: data["Pacotes.dia"],
        preco: data["Pacotes.preco"],
        nome: data["Pacotes.nome"]
    }
    filtrarNull(pacote)
    return pacote
}

function filtrarNull(obj){
    Object.keys(obj).forEach((key)=>{
        if(obj[key]===null){
            delete obj[key]
        }
    })
}


function ObjctToElement(data,title){
    let div = document.createElement("div");
    div.className="smallData"
    let displayTitle = document.createElement("h3")
    displayTitle.appendChild(document.createTextNode(title))
    div.appendChild(displayTitle)
    console.log(data)
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