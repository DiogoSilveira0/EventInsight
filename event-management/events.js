window.onload = function() {
  results();
}

/* Processamento dos resultados - API */

/**
  * Função que faz chamadas à API
  *
  * @param {String} url URL para fazer chamada à API
  * @return {String} json_parsed Parsed Json
*/
async function APIJson(url) {
  let json = await fetch(url)
    .then((response) => response.text())
    .then(data => {
      return data;
    })
    .catch(error => {
      console.error(error);
      return null;
    });
  let json_parsed = JSON.parse(json);
  return json_parsed;
}

/**
  * Função que apresenta os resultados
  *
*/
async function results() {
//  const jsonTest = '[ {"eventID": 1, "name": "Rolling Loud", "lat": 25.7, "lon": 24.3, "address":"Praia da Rocha, Portimão, Algarve", "open_at": "8/7/2020", "close_at": "8/7/2020"}, {"eventID": 2, "name": "Rolling Loud", "lat": 25.7, "lon": 24.3, "address":"Praia da Rocha, Portimão, Algarve", "open_at": "8/7/2020", "close_at": "8/7/2020"} ]';
//  const json_parsed = JSON.parse(jsonTest);

  const eventsList = document.getElementById("eventsList"); //Lista dos resultados

  //Obter JSON da API
  const url = "http://localhost:8080/dashboard/config/events/all";
  const json_parsed = await APIJson(url);

  //Preparar a div
  while(eventsList.firstChild){
    eventsList.removeChild(eventsList.firstChild);
  }

  for(var eventInfo of json_parsed) {
    //Novo evento
    let newEvent = document.createElement("li");
    newEvent.classList.add("list-group-item");
    newEvent.id = "event" + eventInfo.eventID;

    //Row contendo a informação
    let row = document.createElement("div");
    row.classList.add("row");

    //Placehold do nome do evento
    let pName = document.createElement("p");
    pName.classList.add("col-xl-2", "text-right");
    pName.innerText = "Name:";
    row.appendChild(pName);

    //Nome do evento
    let name = document.createElement("p");
    name.classList.add("col-xl-2");
    name.innerText = eventInfo.event_name;
    row.appendChild(name);

    //Placehold da address do evento
    let pAddress = document.createElement("p");
    pAddress.classList.add("col-xl-2", "text-right");
    pAddress.innerText = "Address:"
    row.appendChild(pAddress);

    //Address do evento
    let address = document.createElement("p");
    address.classList.add("col-xl-5");
    address.innerText = eventInfo.address;
    row.appendChild(address);

    //Botão para editar
    let btn = document.createElement("button");
    btn.type = "button";
    btn.classList.add("btn", "btn-danger", "col-xl-1");
    btn.setAttribute("onclick", "confirmRemove(" + eventInfo.eventID + ")")
    let spanRemove = document.createElement("span");
    spanRemove.classList.add("fa", "fa-trash");
    spanRemove.setAttribute("aria-hidden", 'true');
    btn.appendChild(spanRemove);
    row.appendChild(btn);

    //Placehold da localização do evento
    let pLocation = document.createElement("p");
    pLocation.classList.add("col-xl-2", "text-right");
    pLocation.innerText = "Location:";
    row.appendChild(pLocation);

    //Localização do evento
    let location = document.createElement("p");
    location.classList.add("col-xl-2");
    location.innerText = eventInfo.lat + " , " + eventInfo.lon;
    row.appendChild(location);

    //Placehold da opening do evento
    let pOpening = document.createElement("p");
    pOpening.classList.add("col-xl-2", "text-right");
    pOpening.innerText = "Opening:";
    row.appendChild(pOpening);

    //Opening do evento
    let opening = document.createElement("p");
    opening.classList.add("col-xl-1");
    opening.innerText = eventInfo.open_at;
    row.appendChild(opening);

    //Placehold do ending do evento
    let pEnding = document.createElement("p");
    pEnding.classList.add("col-xl-2", "text-right");
    pEnding.innerText = "Ending:";
    row.appendChild(pEnding);

    //Ending do evento
    let ending = document.createElement("p");
    ending.classList.add("col-xl-2");
    ending.innerText = eventInfo.close_at;
    row.appendChild(ending);

    //Adicionar informação à lista
    newEvent.appendChild(row);
    eventsList.appendChild(newEvent);
  }

}

function confirmRemove(eventID) {
  var r = confirm("Are you sure?");
  if (r == true) {
    const Http = new XMLHttpRequest();
    const url='http://localhost:8080/dashboard/config/events/remove?event=' + eventID;

    Http.open("DELETE", url);
    Http.send();

    Http.onreadystatechange = (e) => {
      console.log(Http.responseText)
    }
  }
}


async function submitEvent() {
  const Http = new XMLHttpRequest();
  const url='http://localhost:8080/dashboard/config/events/add';

  const newEventName = document.getElementById("submitEventName").value;
  const newEventLocal = document.getElementById("submitEventLocal").value;
  const newEventLat = document.getElementById("submitEventLat").value;
  const newEventLon = document.getElementById("submitEventLon").value;
  const newEventAddress = document.getElementById("submitEventAddress").value;
  const newEventOpen = document.getElementById("submitEventOpen").value;
  const newEventClose = document.getElementById("submitEventClose").value;

  const jsonSubmit = '{"event_name":"' + newEventName + '",' +
                      '"local":"' + newEventLocal + '",' +
                      '"lat":' + newEventLat + ',' +
                      '"lon":' + newEventLon + ',' +
                      '"address":"' + newEventAddress + '",' +
                      '"open_at":"' + newEventOpen + '",' +
                      '"close_at":"' + newEventClose + '"}';
  console.log(jsonSubmit);

  Http.open("POST", url);
  Http.send(jsonSubmit);

  Http.onreadystatechange = (e) => {
    console.log(Http.responseText)
  }

}
