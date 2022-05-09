"""For functions like parsing"""

class Methods:
    def __init__(self, shared) -> None:
        self.shared = shared
    
    def plugins(self):
        pr = {"PLUGINS": []}
        for i in self.shared.plugins.enviroments:
            if len(i.pages)>1:
                pr[str(i.name).capitalize()] = list(i.pages)
            else:
                for l in i.pages:
                    pr["PLUGINS"].append(i.name)
        return pr