//function re(){
//   window.document.location.reload()
//}

function sendit(){
   var url = "http://127.0.0.1:1029/api/convoy";

   var xhr = new XMLHttpRequest();
   xhr.open("POST", url);
   xhr.setRequestHeader("Content-Type", "application/json");
   xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
         console.log(xhr.status);
         console.log(xhr.responseText);
      }};

   var data = `{
     "address": "http://127.0.0.1:1031/"
   }`;

   xhr.send(data);
}

function accelerate(){
   var url = "http://127.0.0.1:1029/api/accelerate";

   var xhr = new XMLHttpRequest();
   xhr.open("POST", url);
   xhr.setRequestHeader("Content-Type", "application/json");
   xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
         console.log(xhr.status);
         console.log(xhr.responseText);
      }};
   var a= document.getElementById("accelerate_Feld").value
   var b= document.getElementById("target_Feld").value
   var data = `{
    "id":`+a+`,
    "acceleration": 2.5,
    "targetSpeed": `+b+`
   }`;
   xhr.send(data);
}

function decelerate(){
   var url = "http://127.0.0.1:1029/api/accelerate";
   var xhr = new XMLHttpRequest();
   xhr.open("POST", url);
   xhr.setRequestHeader("Content-Type", "application/json");
   xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
         console.log(xhr.status);
         console.log(xhr.responseText);
      }};
   var a= document.getElementById("decelerate_Feld").value

   var data = `{
    "id":`+a+`,
    "acceleration": -2.5,
    "targetSpeed": 0.0
   }`;
   xhr.send(data);
}

function destroy(){
   var url = "http://127.0.0.1:1029/api/intact";
   var xhr = new XMLHttpRequest();
   xhr.open("DELETE", url);
   xhr.setRequestHeader("Content-Type", "application/json");
   xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
         console.log(xhr.status);
         console.log(xhr.responseText);
      }};
   var a= document.getElementById("destroy_Feld").value
   var data = `{
    "id":`+a+`
   }`;
   xhr.send(data);
}

function repair(){
   var url = "http://127.0.0.1:1029/api/intact";
   var xhr = new XMLHttpRequest();
   xhr.open("POST", url);
   xhr.setRequestHeader("Content-Type", "application/json");
   xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
         console.log(xhr.status);
         console.log(xhr.responseText);
      }};
   var a= document.getElementById("repair_Feld").value
   var data = `{
    "id":`+a+`
   }`;
   xhr.send(data);
}

function joinConvoy(){
   var url = "http://127.0.0.1:1029/api/convoy";
   var xhr = new XMLHttpRequest();
   xhr.open("POST", url);
   xhr.setRequestHeader("Content-Type", "application/json");
   xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
         console.log(xhr.status);
         console.log(xhr.responseText);
      }};
   var a= document.getElementById("join_Feld").value
   var data = `{
    "id":`+a+`
   }`;
   xhr.send(data);
}

function leaveConvoy(){
   var url = "http://127.0.0.1:1029/api/convoy";
   var xhr = new XMLHttpRequest();
   xhr.open("DELETE", url);
   xhr.setRequestHeader("Content-Type", "application/json");
   xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
         console.log(xhr.status);
         console.log(xhr.responseText);
      }};
   var a= document.getElementById("leave_Feld").value
   var data = `{
    "id":`+a+`
   }`;
   xhr.send(data);
}

function hartInitialization(){
   var url = "http://127.0.0.1:1029/api/inject";
   var xhr = new XMLHttpRequest();
   xhr.open("POST", url);
   xhr.setRequestHeader("Content-Type", "application/json");
   xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
         console.log(xhr.status);
         console.log(xhr.responseText);
      }};
   var a= document.getElementById("join_Feld").value
   var data = `{
    "interval": 0.1,
    "count": 0,
    "broker_address": "127.0.0.1",
    "broker_port": 1883,
    "broker_username": "testUser",
    "broker_password": "test",
    "broker_channel": "truckChannel"
}`;
   xhr.send(data);
}
function hartflat(){
   var url = "http://127.0.0.1:1029/api/inject";
   var xhr = new XMLHttpRequest();
   xhr.open("DELETE", url);
   xhr.setRequestHeader("Content-Type", "application/json");
   xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
         console.log(xhr.status);
         console.log(xhr.responseText);
      }};
   xhr.send();
}