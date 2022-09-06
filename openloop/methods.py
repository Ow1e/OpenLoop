"""For functions like parsing"""

import openloop

class Methods:
    def __init__(self, shared) -> None:
        self.__shared = shared
        self.len = len
        self.name = shared.config["Customize"].get("name", "OpenLoop")
        self.theme = shared.config["Customize"].get("theme", "primary")
        self.experimental = openloop.experimental
        self.version = f"{openloop.num}-{openloop.code}"
    
    def plugins(self):
        pr = {"PLUGINS": []}
        for i in self.__shared.plugins.enviroments:
            if not i.hidden:
                if len(i.pages)>1:
                    pr[str(i.name).capitalize()] = list(i.pages)
                else:
                    for l in i.pages:
                        pr["PLUGINS"].append(i.name)
        return pr