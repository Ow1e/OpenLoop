console.log("Running ReflowJS wrapper V1")

async function reflow(req, type, elem){
    let response = await fetch("/reflow/"+req);
    if (response.ok) { // if HTTP-status is 200-299
        // get the response body (the method explained below)
        let json = await response.json();
        if (type=="innerHTML"){
            elem.innerHTML = json["value"]
        }
      } else {
        alert("HTTP-Error: " + response.status);
    }
}

document.addEventListener('DOMContentLoaded', function() {

	var serverd = document.querySelectorAll('[reflow-serv]');

	for (var serve of serverd) {
		var time = serve.getAttribute("reflow-time")
        var req = serve.getAttribute("reflow-serv")
        var type = serve.getAttribute("reflow-type")

        if (type==null){
            var type = "innerHTML"
        }
        
        if (time==null){
            var time = 1000
        }

        reflow(req, type, serve)
        setInterval(reflow, time, req, type, serve)
	}
}, false);