console.log("Running FlowJS wrapper V1")

async function flow(req, type, elem){
    let response = await fetch("/flow/refresh/"+req);
    if (response.ok) {
        let json = await response.json();
        if (type=="innerHTML"){
            elem.innerHTML = json["value"]
        } else if (type=="width"){
            elem.style.width = json["value"]
        }
      } else {
        alert("HTTP-Error: " + response.status);
    }
}

document.addEventListener('DOMContentLoaded', function() {

	var serverd = document.querySelectorAll('[flow-serv]');

	for (var serve of serverd) {
		var time = serve.getAttribute("flow-time")
        var req = serve.getAttribute("flow-serv")
        var type = serve.getAttribute("flow-type")

        if (type==null){
            var type = "innerHTML"
        }
        
        if (time==null){
            var time = 1000
        }
        flow(req, type, serve)
        setInterval(flow, time, req, type, serve)
	}
}, false);