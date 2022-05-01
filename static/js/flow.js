console.log("Running FlowJS wrapper V1")

window.addEventListener("load", () => {
    registerSW()
})

async function registerSW(){
    if ("serviceWorker" in navigator){
        console.log("Service Worker Detected")
        try {
            await navigator.serviceWorker.register("./sw.js")
        } catch (e) {
            console.log("Flow Service Worker Failed")
        }
    }
}

function show_net(){
    document.getElementById('offline').style.display='none'
}

function hide_net(){
    document.getElementById('offline').style.display='block'
    document.getElementById("offline").removeAttribute("hidden")
}

async function flow(req, type, elem){
    try {
        let response = await fetch("/flow/refresh/"+req);
        if (response.ok) {
            let json = await response.json();
            if (type=="innerHTML"){
                elem.innerHTML = json["value"]
            } else if (type=="width"){
                elem.style.width = json["value"]
            } else {
                return json["value"]
            }
          } else {
            alert("HTTP-Error: " + response.status);
        }
        show_net()
    } catch (error) {
        hide_net()
    }
}

if (document.getElementById("page")!=null){
    console.log("Detected Flow Page...")
    var page = document.getElementById("page")
    if (document.getElementById("refresh")!=null){
        console.log("Found Button")
        var ref = document.getElementById("refresh")
        ref.onclick = function(){
            flow(page.getAttribute("flow"), "innerHTML", page)
        } 
    } else {
        console.log("Could not find button")
    }
}

document.addEventListener('DOMContentLoaded', function() {

	var serverd = document.querySelectorAll('[flow]');

	for (var serve of serverd) {
        var req = serve.getAttribute("flow")
        var type = serve.getAttribute("flow-type")
        console.log(serve)
        if (type==null){
            var type = "innerHTML"
        }
        
        flow(req, type, serve)
	}

    start_flow()
}, false);

function start_flow(){

	var serverd = document.querySelectorAll('[flow-serv]');

	for (var serve of serverd) {
		var time = serve.getAttribute("flow-time")
        var req = serve.getAttribute("flow-serv")
        var type = serve.getAttribute("flow-type")
        console.log(serve)
        if (type==null){
            var type = "innerHTML"
        }
        
        if (time==null){
            var time = 1000
        }
        flow(req, type, serve)
        setInterval(flow, time, req, type, serve)
	}
}

async function set_onclick(serve){
    serve.onclick = async function (){
        var id = serve.getAttribute("flow-click")
        let response = await fetch("/flow/refresh/"+id);
        if (response.ok) {
            let json = await response.json();
            if (json["value"]!=null && json["value"]!="None"){
                window.location = json["value"]
            }
          } else {
            alert("HTTP-Error: " + response.status);
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {

	var serverd = document.querySelectorAll('[flow-click]');

	for (var serve of serverd) {
        set_onclick(serve)
	}
}, false);

console.log("Completed FlowJS Start")
