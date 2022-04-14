document.addEventListener('DOMContentLoaded', function() {

	var charts = document.querySelectorAll('[data-bss-chart]');

	for (var chart of charts) {
		chart.chart = new Chart(chart, JSON.parse(chart.dataset.bssChart));
	}
}, false);

document.getElementById("clear").onclick = async function (){
	let response = await fetch("/api/clear_notifications");

	if (response.ok) { // if HTTP-status is 200-299
	// get the response body (the method explained below)
		let json = await response.json();
	} else {
		alert("HTTP-Error: " + response.status);
	}
	document.getElementById("clear-me").innerHTML = ""
	document.getElementById("notnum").innerHTML = ""
}

async function release_function(name, func, send = null, loop = 0){
	var form = new FormData();
	form.append("send", send);
	let response = await fetch("/api/pl/"+name+"/"+func, {method: "POST", body: form});
	let json = await response.json();
	if (response.ok) { // if HTTP-status is 200-299
	// get the response body (the method explained below)
		loop++;
		if (loop == 4){
			var looped = confirm("This page has been doing allot of dialogue!\nDo you want to contiue talking to this plugin?");
			var loop = 0;
		} else {
			var looped = true;
		}
		if (looped==true) {
			if (json["return"]["type"]=="prompt"){
				var msg = prompt(json["return"]["data"]);
				release_function(name, func, msg, loop);
			} else if (json["return"]["data"]!=null){
				alert(json["return"]["data"]);
			}
		}
	} else {
		alert("HTTP-Error: " + response.status + "\n" + json["reason"]);
	}
}

document.getElementById("reload").onclick = function(){
	window.location.reload(true)
}