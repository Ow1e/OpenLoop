def condense(inp):
    string = ""
    for i in inp.split("\n"):
        new = str(i)
        checking = True
        while checking:
            if new.startswith(" "):
                new = new[1:]
            else:
                checking = False
                string += new
    return string
    
        

class Element(list):
    """A Element"""
    def __init__(self):
        """CrossWeb Element"""
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
    def __init__(self, title = "", size=1):
        super().__init__()
        if size!=0:
            self.outer = '<h{} flow>{}</h{}>'.format(size, "{}", size)
        else:
            self.outer = '<div class="d-sm-flex justify-content-between align-items-center mb-4"><h3 class="text-dark mb-0" flow>{}</h3></div>'
        
        if title != "" and title != None:
            self.append(title)

class Card(Element):
    def __init__(self, title, size):
        super().__init__()
        self.outer = '''<div class="col-md-{}"><div class="card shadow mb-4"><div class="card-header py-3"><h6 class="text-primary m-0 fw-bold">{}</h6></div><div class="card-body" flow>{}</div></div></div>'''.format(size, title, "{}")

class Row(Element):
    def __init__(self) -> None:
        """
        Bootstrap Studio Row
        """
        super().__init__()
        self.outer = '<div class="row">{}</div>'

class Feature(Element):
    def __init__(self, title, icon = "fab fa-superpowers", inner = "Nothing", color = "primary", size=6):
        super().__init__()
        html = """
<div class="col-md-{} col-xl-3 mb-4">
    <div class="card shadow border-start-primary py-2">
        <div class="card-body">
            <div class="row align-items-center no-gutters">
                <div class="col me-2">
                    <div class="text-uppercase text-{} fw-bold text-xs mb-1"><span>{}</span></div>
                    <div class="text-dark fw-bold h5 mb-0"><span flow>{}</span></div>
                </div>
                <div class="col-auto"><i class="{} fa-2x text-gray-300"></i></div>
            </div>
        </div>
    </div>
</div>
"""
        self.outer = condense(html).format(size, color, title, inner, icon)

class Table(Element):
    """Holds table elements"""
    def __init__(self):
        super().__init__()
        self.outer = '<div id="dataTable" class="table-responsive table mt-2" role="grid" aria-describedby="dataTable_info"><table id="dataTable" class="table my-0">{}</table></div>'

class Table_Header(Element):
    """Table header"""
    def __init__(self):
        super().__init__()
        self.outer = '<thead>{}</thead>'

class Table_Body(Element):
    """Table body"""
    def __init__(self):
        super().__init__()
        self.outer = '<tbody>{}</tbody>'

class Table_Row(Element):
    """Table row"""
    def __init__(self):
        super().__init__()
        self.outer = "<tr>{}</tr>"

class Table_Cell(Element):
    """Table cell"""
    def __init__(self, text=""):
        super().__init__()
        self.outer = "<th>"+text+"{}</th>"

class Icon(Element):
    "Icon"
    def __init__(self, classes = ""):
        super().__init__()
        self.outer = '<i class="'+classes+'"></i>'