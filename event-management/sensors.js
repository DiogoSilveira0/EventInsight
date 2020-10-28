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
//  const jsonTest = '[ {"eventID": 1, "name": "Rolling Loud", "local": [25.7,24.3]}, {"eventID": 2, "name": "MEO Sudoeste", "local": [36.7,42.3]} ]';
//  const json_parsed = JSON.parse(jsonTest);

  const eventsList = document.getElementById("eventsList"); //Lista dos resultados

  //Obter JSON da API
  const url = "http://localhost:8080/dashboard/config/events/all";
  const json_parsed = await APIJson(url);

  //Preparar a div
  while(eventsList.firstChild){
    eventsList.removeChild(eventsList.firstChild);
  }

  for (var eventInfo of json_parsed) {
    //Novo evento
    let newEvent = document.createElement("li");
    newEvent.classList.add("list-group-item");

    //Row contendo a informação
    let row = document.createElement("div");
    row.classList.add("row");

    //Placehold do nome do evento
    let pName = document.createElement("p");
    pName.classList.add("col-xl-2", "text-right");
    pName.innerText = "Name:"
    row.appendChild(pName);

    //Nome do evento
    let name = document.createElement("p");
    name.classList.add("col-xl-8");
    name.innerText = eventInfo.event_name;
    row.appendChild(name);

    //Botão para os sensores
    let btn = document.createElement("button");
    btn.type = "button";
    btn.classList.add("btn", "btn-primary", "col-xl-1");
    let sensorsInput = "showSensors(\"" + eventInfo.eventID + "\")";
    btn.setAttribute("onclick", sensorsInput);
    btn.value = eventInfo.eventID;
    btn.innerText = "Sensores";
    let spanSensores = document.createElement("span");
    spanSensores.classList.add("fa", "fa-angle-down");
    spanSensores.setAttribute("aria-hidden", 'true');
    btn.appendChild(spanSensores);
    row.appendChild(btn);

    //Botão para adicionar
    let btn2 = document.createElement("button");
    btn2.type = "button";
    btn2.classList.add("btn", "btn-dark", "col-xl-1");
    btn2.setAttribute("data-toggle", "modal");
    btn2.setAttribute("data-target", "#sensorSubmitModal");
    btn2.setAttribute("onclick", 'let modalSubmit=document.getElementById("sensorSubmitModal"); modalSubmit.setAttribute("value", "' + eventInfo.eventID + '");')
    let spanSensores2 = document.createElement("span");
    spanSensores2.classList.add("fa", "fa-plus");
    spanSensores2.setAttribute("aria-hidden", 'true');
    spanSensores2.style.color = "white";
    btn2.appendChild(spanSensores2);
    row.appendChild(btn2);

    //Placehold da localização do evento
    let pLocation = document.createElement("p");
    pLocation.classList.add("col-xl-2", "text-right");
    pLocation.innerText = "Location:";
    row.appendChild(pLocation);

    //Localização do evento
    let location = document.createElement("p");
    location.classList.add("col-xl-10");
    location.innerText = eventInfo.lat + " , " + eventInfo.lon;
    row.appendChild(location);

    //Adicionar evento à Row e à Lista
    newEvent.appendChild(row);
    eventsList.appendChild(newEvent);

    let sensoresDiv = document.createElement("div");
    sensoresDiv.id = eventInfo.eventID;
    sensoresDiv.style.display = "none";
    newEvent.appendChild(sensoresDiv);
  }

}


async function showSensors(elementID) {
//  const jsonTest = '[ {"eventID": 1, "sensorID": 1, "type": "Camera", "zone": "2"}, {"eventID": 1, "sensorID": 2, "type": "Camera", "zone": "3"} ]';
//  const json_parsed = JSON.parse(jsonTest);

  const url = "http://localhost:8080/dashboard/config/sensors/in_event?event=" + elementID;
  const json_parsed = await APIJson(url);

  var sensorsResults = document.getElementById(elementID);

  if (sensorsResults.style.display === "none") {

    //Obter JSON da API
  //  const url = "";
  //  const json_parsed = await APIJson(url);

    //Preparar a div
    while(sensorsResults.firstChild){
      sensorsResults.removeChild(sensorsResults.firstChild);
    }

    for (var sensorInfo of json_parsed) {
      //Line
      let line = document.createElement("hr");
      line.style.border = "1px solid black";
      sensorsResults.appendChild(line);

      //Row
      let row = document.createElement("div");
      row.classList.add("row");

      //Placehold do ID
      let pID = document.createElement("p");
      pID.classList.add("col-xl-1", "offset-xl-1", "text-right");
      pID.innerText = "ID:"
      row.appendChild(pID);

      //ID
      let sensorID = document.createElement("p");
      sensorID.classList.add("col-xl-1");
      sensorID.innerText = sensorInfo.sensorID;
      row.appendChild(sensorID);

      //Placehold do Type
      let pType = document.createElement("p");
      pType.classList.add("col-xl-1", "text-right");
      pType.innerText = "Type:"
      row.appendChild(pType);

      //Type
      let sensorType = document.createElement("p");
      sensorType.classList.add("col-xl-1");
      sensorType.id = "sensorType" + sensorInfo.eventID + sensorInfo.sensorID;
      sensorType.innerText = sensorInfo.type;
      row.appendChild(sensorType);

      //Placehold da Zone
      let pZone = document.createElement("p");
      pZone.classList.add("col-xl-1", "offset-xl-1", "text-right");
      pZone.innerText = "Zone:"
      row.appendChild(pZone);

      //Zone
      let sensorZone = document.createElement("p");
      sensorZone.classList.add("col-xl-2");
      sensorZone.id = "sensorZone" + sensorInfo.eventID + sensorInfo.sensorID;;
      sensorZone.innerText = sensorInfo.zone;
      row.appendChild(sensorZone);

      //Botão para editar
      let btn = document.createElement("button");
      btn.type = "button";
      btn.classList.add("btn", "btn-outline-dark", "col-xl-1", "offset-xl-1");
      btn.setAttribute("data-toggle", "modal");
      btn.setAttribute("data-target", "#sensorEditModal");
      btn.setAttribute("onclick", 'let modalEdit=document.getElementById("sensorEditModal"); modalEdit.setAttribute("value", "' + sensorInfo.sensorID + '"); let eventEdit=document.getElementById("editSensorEvent"); eventEdit.setAttribute("value", "' + sensorInfo.eventID + '")');
      btn.innerText = "Edit";
      row.appendChild(btn);

      //Botão para editar
       let btn2 = document.createElement("button");
       btn2.type = "button";
       btn2.classList.add("btn", "btn-danger", "col-xl-1");
       btn2.setAttribute("onclick", "removeSensor(" + sensorInfo.sensorID + ")")
       let spanRemove = document.createElement("span");
       spanRemove.classList.add("fa", "fa-trash");
       spanRemove.setAttribute("aria-hidden", 'true');
       btn2.appendChild(spanRemove);
       row.appendChild(btn2);

      //Juntar sensor à lista
      sensorsResults.appendChild(row)

      sensorsResults.style.display = "block";
    }

   }  else {sensorsResults.style.display = "none";}

}
function removeSensor(sensorID) {
  var r = confirm("Are you sure?");
  if (r == true) {
    const Http = new XMLHttpRequest();
    const url='http://localhost:8080/dashboard/config/sensors/remove?sensor=' + sensorID;

    Http.open("DELETE", url);
    Http.send();

    Http.onreadystatechange = (e) => {
      console.log(Http.responseText)
    }
  }
}

function editSensor() {

  let sensorID = document.getElementById("sensorEditModal").getAttribute("value");
  let newSensorZone = document.getElementById("editSensorZone");
  let newSensorEvent = document.getElementById("editSensorEvent");


  const Http = new XMLHttpRequest();
  const url= 'http://localhost:8080/dashboard/config/sensors/edit';

  const jsonSubmit = '{"eventID":"' + newSensorEvent.value + '",' +
                      '"zone":"' + newSensorZone.value + '",'+
                      '"sensorID":"' + sensorID + '"}';

  Http.open("PUT", url);
  console.log(jsonSubmit)
  Http.send(jsonSubmit);

  Http.onreadystatechange = (e) => {
    console.log(Http.responseText)
  }

}

async function addSensor() {

  let newSensorType = document.getElementById("addSensorType");
  let eventID = document.getElementById("sensorSubmitModal").getAttribute("value");


  const Http = new XMLHttpRequest();
  const url= 'http://localhost:8080/dashboard/config/sensors/add';

  Http.open("POST", url);
  const jsonSubmit0 = '{"type": "' + newSensorType.value + '"}';
  Http.send(jsonSubmit0 );

  Http.onreadystatechange = (e) => {
    console.log(Http.responseText)
  }

  const url2 = "http://localhost:8080/dashboard/config/sensors/all" ;
  const json_parsed = await APIJson(url2);

  const sensor = json_parsed[json_parsed.length - 1];

  const Http2 = new XMLHttpRequest();
  const url3='http://localhost:8080/dashboard/config/sensors/add/to_location';

  const jsonSubmit = '{"sensorID":"' + sensor.sensorID + '",' +
                      '"eventID":"' + eventID + '",' +
                      '"zone":" "}';

  Http.open("POST", url3);
  Http.send(jsonSubmit);

  Http.onreadystatechange = (e) => {
    console.log(Http.responseText)
  }


}
