var content = ""
content += "Window: "+window.innerHeight+"x"+window.innerWidth+"<br>"
content += "Flow Version: "+"V1<br>"
content += "WPA Capable: "+window.isSecureContext

document.getElementById("debug").innerHTML = content