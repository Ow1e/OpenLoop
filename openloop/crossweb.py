import os

if os.getenv("OPENLOOP_FLOWLOW"):
    flow_time_def = 5000
else:
    flow_time_def = 1000

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
        self.flow_enabled = True
        self.flow = ""

    def add_flow(self, serv, time=flow_time_def, type=None):
        self.flow = "reflow "
        if time==False:
            self.flow += f'flow="'+serv+'"'
        else:
            self.flow += f'flow-serv="'+serv+'"'
        if time != None and time!=False:
            self.flow += f'flow-time="'+str(time)+'"'
        if type != None:
            self.flow += f'flow-type="'+type+'"'

    def export(self):
        export = ""
        for i in self:
            if type(i) == int or type(i) == str:
                export += str(i).replace("\n", "<br>")
            else:
                export += i.export()

        if self.flow_enabled:
            s = self.outer.replace("flow", self.flow).format(export)
            s = s.replace("flot", self.flow.replace('flow-type="width"', ""))
            return s
        else:
            return self.outer.format(export)


class Page(Element):
    """This will organize Cards and export them, no html actually defined"""

    def __init__(self):
        super().__init__()
        self.outer = '<div class="row">{}</div>'


class Heading(Element):
    def __init__(self, title="", size=1, color=None):
        super().__init__()
        if size != 0:
            if color:
                self.outer = '<h{} flow class="text-{}">{}</h{}>'.format(size, color, "{}", size)
            else:
                self.outer = '<h{} flow>{}</h{}>'.format(size, "{}", size)
        else:
            self.outer = '<div class="d-sm-flex justify-content-between align-items-center mb-4"><h3 class="text-dark mb-0" flow>{}</h3></div>'

        if title != "" and title != None:
            self.append(title)


class Card(Element):
    def __init__(self, title, size):
        super().__init__()
        self.outer = '''<div class="col-md-{}"><div class="card shadow mb-4"><div class="card-header py-3"><h6 class="text-primary m-0 fw-bold">{}</h6></div><div class="card-body" flow>{}</div></div></div>'''.format(
            size, title, "{}")


class Row(Element):
    def __init__(self) -> None:
        """
        Bootstrap Studio Row
        """
        super().__init__()
        self.outer = '<div class="row">{}</div>'


class Feature(Element):
    def __init__(self, title, icon="fab fa-superpowers", inner="Nothing", color="primary", size=6, bar=False):
        super().__init__()
        if not bar:
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
        else:
            html = """
<div class="col-md-{} col-xl-3 mb-4">
    <div class="card shadow border-start-info py-2">
        <div class="card-body">
            <div class="row align-items-center no-gutters">
                <div class="col me-2">
                    <div class="text-uppercase text-{} fw-bold text-xs mb-1"><span>{}</span></div>
                    <div class="row g-0 align-items-center">
                        <div class="col-auto">
                            <div class="text-dark fw-bold h5 mb-0 me-3"><span flot>{}</span></div>
                        </div>
                        <div class="col">
                            <div class="progress progress-sm">
                                <div class="progress-bar bg-{}" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width: 0%;" flow><span class="visually-hidden"></span></div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-auto"><i class="{} fa-2x text-gray-300"></i></div>
            </div>
        </div>
    </div>
</div>
"""
            self.outer = condense(html).format(size, color, title, inner, color, icon)


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
        self.outer = "<th>{}</th>"
        if text!="":
            self.append(text)


class Icon(Element):
    "Icon"

    def __init__(self, classes=""):
        super().__init__()
        self.outer = '<i flow class="'+classes+'"></i>'


class Button(Element):
    """Button with Flow Support"""

    def __init__(self, color="primary", icon="fas fa-flag", flow="", text="", href=""):
        super().__init__()
        self.flow_enabled = False
        self.html = '''
<a class="btn btn-{} btn-icon-split" role="button" flow-click="{}" href="{}">
    <span class="text-white-50 icon">
        <i class="{}"></i>
    </span>
    <span class="text-white text">{}</span>
</a>
'''.format(color, flow, href, icon, "{}")
        self.outer = condense(self.html)
        if text != "":
            self.append(text)


class Form(Element):
    """CrossWeb Form, use with a Row and a Form Element"""

    def __init__(self, flow_path):
        super().__init__()
        self.flow_enabled = False
        self.outer = '<form action="/flow/refresh/{}" method="post">{}</form>'.format(flow_path, "{}")
        self.append('<input type="hidden" location name="formLocation" value="">')

class HTML_Form(Element):
    """HTML CrossWeb Form, use with a Row and a Form Element"""

    def __init__(self, path):
        super().__init__()
        self.flow_enabled = False
        self.outer = '<form action="{}" method="post">{}</form>'.format(path, "{}")
        self.append('<input type="hidden" location name="formLocation" value="">')

class Form_Element(Element):
    """Element that wraps around Label/Input"""

    def __init__(self):
        super().__init__()
        self.outer = '<div class="col"><div class="mb-3">{}</div></div>'


class Label(Element):
    """Label for Input"""

    def __init__(self, text=None, to=""):
        super().__init__()
        self.outer = '<label class="form-label" for="{}"><strong>{}</strong></label>'.format(
            to, "{}")
        if text != None:
            self.append(text)


class Input(Element):
    """Input for form"""
    def __init__(self, name, type="text", placeholder="", required = False):
        super().__init__()
        if required == True:
            required = "required"
        else:
            required = ""
        self.outer = f'<input class="form-control" type="{type}" placeholder="{placeholder}" name="{name}" {required} />'

class Form_Button(Element):
    """Button for Form"""
    def __init__(self, text="Submit", color="primary"):
        super().__init__()
        self.outer = '<button class="btn btn-{} btn-sm" type="submit" style="margin-top: 10px;">{}</button>'.format(color, "{}")
        if text!=None:
            self.append(text)

class Form_Check(Element):
    """Check Button for form"""
    def __init__(self, text, name, checked = False):
        super().__init__()
        if checked == True:
            checked = "checked"
        else:
            checked = ""
        self.outer = '<div class="form-check form-switch"><input class="form-check-input" type="checkbox" name="{}" {} /><label class="form-check-label"><strong>{}</strong></label></div>'.format(name, checked, text)

class Image(Element):
    """HTML image"""
    def __init__(self, src, height, width=None):
        super().__init__()
        if width==None:
            self.outer = f'<img src="{src}" height="{height}" style="margin: 10px;">'
        else:
            self.outer = f'<img src="{src}" width="{width}" height="{height}" style="margin: 10px;">'

class Text(Element):
    def __init__(self, text=None, color=None, traditional=False):
        super().__init__()
        if color:
            self.outer = '<p class="text-{}">{}</p>'.format(color, "{}")
        else:
            if traditional:
                self.outer = "<p>{}</p>"
            else:
                self.outer = "{}"
        if text!=None:
            self.append(text)

class Link(Element):
    def __init__(self, link, text=None):
        super().__init__()
        self.outer = '<a href="{}">{}</a>'.format(link, "{}")
        if text!=None:
            self.append(text)

class Div(Element):
    def __init__(self):
        super().__init__()
        self.outer = "<div flow>{}</div>"

class Graph(Element):
    def __init__(self, flow):
        super().__init__()
        self.flow_enabled = False
        self.outer = f'<div flow="{flow}" flow-type="graph"></div>'

class Code(Element):
    def __init__(self, text=""):
        super().__init__()
        self.outer = '<div style="background: var(--bs-gray);padding: 10px;border-radius: 5px;margin-bottom:10px;"><code style="color: var(--bs-white);" flow>{}</code></div>'
        if text!="":
            self.append(text)

class Integrate(Element):
    def __init__(self, flow):
        super().__init__()
        self.flow_enabled = False
        self.outer = f'<div flow="{flow}" class="row"></div>'

class Collapsable(Element):
    def __init__(self, title):
        super().__init__()
        self.outer = condense('''<div class="shadow card"><a class="btn btn-link text-start card-header fw-bold" data-bs-toggle="collapse" aria-expanded="true" aria-controls="collapse-4" href="#collapse-4" role="button">{}</a>
                        <div class="collapse show" id="collapse-4" style="">
                            <div class="card-body" flow>{}</div>
                        </div>
                    </div>''').format(title, "{}")
        