class Element(list):
    """Base class for Elements"""
    def __init__(self):
        super().__init__()
        self.outer = "<p flow>{}</p>"
        self.flow = ""
    
    def add_flow(self, serv, time = None, type = None):
        self.flow = "reflow "
        self.flow += f'flow-serv="'+serv+'"'
        if time != None:
            self.flow += f'flow-time="'+str(time)+'"'
        if type != None:
            self.flow += f'flow-type="'+type+'"'
        

    def export(self):
        export = ""
        for i in self:
            if type(i) == int or type(i) == str:
                export += str(i)
            else:
                export += i.export()
        return self.outer.replace("flow", self.flow).format(export)

class Page(Element):
    """This will organize Cards and export them, no html actually defined"""
    def __init__(self):
        super().__init__()
        self.outer = '<div class="row">{}</div>'

class Heading(Element):
    def __init__(self, title, size=1):
        super().__init__()
        if size!=0:
            self.outer = '<h{} flow>{}</h{}>'.format(size, "{}", size)
        else:
            self.outer = '<div class="d-sm-flex justify-content-between align-items-center mb-4"><h3 class="text-dark mb-0" flow>{}</h3></div>'
        self.append(title)

class Card(Element):
    def __init__(self, title, size):
        super().__init__()
        self.outer = '''<div class="col-md-{}"><div class="card shadow mb-4"><div class="card-header py-3"><h6 class="text-primary m-0 fw-bold">{}</h6></div><div class="card-body" flow>{}</div></div></div>'''.format(size, title, "{}")

package = {
    "Element": Element,
    "Page": Page,
    "Heading": Heading,
    "Card": Card
}