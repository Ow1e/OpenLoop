var content = ""
content += "Window: "+window.innerHeight+"x"+window.innerWidth+"<br>"
content += "Flow Version: "+"V1<br>"
content += "PWA Capable: "+window.isSecureContext+"<br>"
content += "Cookies: "+navigator.cookieEnabled+"<br>"
content += "Running on a "+navigator.platform+"<br>"
content += "Online: "+navigator.onLine+"<br>"

document.getElementById("debug").innerHTML = content