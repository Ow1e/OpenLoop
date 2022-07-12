console.log("Running FlowJS wrapper V2.2")

window.addEventListener("load", () => {
    registerSW()
})

var offline = false;

async function registerSW(){
    if ("serviceWorker" in navigator){
        console.info("PWA is enabled. With this URL you can access full PWA\nhttps://docs.cyclone.biz/using-pwas")
        try {
            await navigator.serviceWorker.register("./sw.js")
        } catch (e) {
            console.log("Flow Service Worker Failed")
        }
    } else {
        console.info("PWA is disabled, Service Workers only work with HTTPS and Localhost")
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
        if (response.ok){
            let json = await response.json();
            if (type=="innerHTML"){
                elem.innerHTML = json["value"]
            } else if (type=="width"){
                elem.style.width = json["value"]
            } else if (type=="graph"){
                Plotly.newPlot(elem, json["value"]["data"], json["value"]["layout"])
            } else {
                return json["value"]
            }
        } else {
            if (response.status == 401){
                console.error("Switching...")
                window.location.href = "/reload"
            } else {console.error("HTTP-Error: " + response.status);}
            
        }
        show_net()
    } catch (error) {
        hide_net()
        var offline = true;
        console.warn("OpenLoop tried to update via Flow, but is offline = "+offline)
        await new Promise(r => setTimeout(r, 10000));
        location.reload()
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

async function flow_pack(package){
    var url = new URL(window.location.origin+"/flow/package");

    var data = [];

    for (var i in package){
        // Maybe check for duplicates in the future, I dunno
        data.push(package[i]["serve"])
    }

    for (let k in data) { url.searchParams.append(data[k], ""); }
    const request = await fetch(url)

    if (request.ok){
        const json = await request.json()

        for (var server in package){
            var concur = package[server]
            var value = json["data"][concur["serve"]]["value"]
            var type = concur["type"]
            var elem = concur["object"]

            if (type=="innerHTML"){
                elem.innerHTML = value
            } else if (type=="width"){
                elem.style.width = value
            } else if (type=="graph"){
                Plotly.newPlot(elem, value["data"], value["layout"])
            } else {
                elem.innerHTML = value
            }
        }
    } else {
        if (response.status == 401){
            console.error("Switching...")
            window.location.href = "/reload"
        } else {console.error("HTTP-Error: " + response.status);}
        
    }
}

function start_flow(){

	var serverd = document.querySelectorAll('[flow-serv]');
    var times = {};

    for (var serve of serverd) {
        times[serve.getAttribute("flow-time")] = []
    }

	for (var serve of serverd) {
		var time = serve.getAttribute("flow-time")
        var req = serve.getAttribute("flow-serv")
        var type = serve.getAttribute("flow-type")
        
        times[time].push({
            "serve": req,
            "type": type,
            "object": serve
        })
	}
    for (var key in times){
        console.log(times[key])
        setInterval(flow_pack, key, times[key])
    }
}

async function set_onclick(serve){
    serve.onclick = async function (){
        var id = serve.getAttribute("flow-click")
        let response = await fetch("/flow/refresh/"+id);
        if (response.ok) {
            let json = await response.json();
            if (json["value"].startsWith("http") || json["value"].startsWith("/")){
                location.href = json["value"]
            }
          } else {
            alert("Error pressing button!");
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {

	var serverd = document.querySelectorAll('[flow-click]');

	for (var serve of serverd) {
        console.log(serve)
        set_onclick(serve)
	}
}, false);

document.addEventListener('DOMContentLoaded', function() {

	var serverd = document.querySelectorAll('[location]');

	for (var serve of serverd) {
        serve.value = window.location.href
	}
}, false);

console.log("Completed FlowJS Start")

console.log(
    "%cStop!",
    "color:#4E73DF;font-family:system-ui;font-size:4rem;-webkit-text-stroke: 1px black;font-weight:bold"
);

console.log(
    "%cNever put something in the console unless you are a Developer and know what your doing. The console could allow attackers to use a XSS vulneralbility and hack your OpenLoop account.",
    "font-family:system-ui;font-size:large;"
)