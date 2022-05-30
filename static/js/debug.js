var content = ""
content += "Window: "+window.innerHeight+"x"+window.innerWidth+"<br>"
content += "Flow Version: "+"V3<br>"
content += "PWA Capable: "+window.isSecureContext+"<br>"
content += "Cookies: "+navigator.cookieEnabled+"<br>"
content += "Running on a "+navigator.platform+"<br>"
content += "Online: "+navigator.onLine+"<br>"

document.getElementById("debug").innerHTML = content

console.info("Loaded Client Debug Helper")

function erase_pwa(){
    navigator.serviceWorker.getRegistrations().then(function(registrations) {
        for(let registration of registrations) {
         registration.unregister()
    } })
    alert("Erased cache")
}