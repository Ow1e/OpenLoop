var content = ""
content += "Window: "+window.innerHeight+"x"+window.innerWidth+"<br>"
content += "Flow Version: "+"V2<br>"
content += "PWA Capable: "+window.isSecureContext+"<br>"
content += "Cookies: "+navigator.cookieEnabled+"<br>"
content += "Running on a "+navigator.platform+"<br>"
content += "Online: "+navigator.onLine+"<br>"

document.getElementById("debug").innerHTML = content

function erase_pwa(){
    navigator.serviceWorker.getRegistrations().then(function(registrations) {
        for(let registration of registrations) {
         registration.unregister()
    } })
    console.info("Unregistered Workers")
}