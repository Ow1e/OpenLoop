class Element(list):
    """Base class for Elements"""
    def __init__(self):
        super().__init__()
        self.outer = "<p>{}</p>"

    def export(self):
        export = ""
        for i in self:
            if type(i) == int or type(i) == str:
                export += str(i)
            else:
                export += i.export()
        return self.outer.format(export)

class Page(Element):
    """This will organize Cards and export them, no html actually defined"""
    def __init__(self):
        super().__init__()
        self.outer = '<div class="row">{}</div>'

class Heading(Element):
    def __init__(self, title, size=1):
        super().__init__()
        self.outer = '<h{}>{}</h{}>'.format(size, "{}", size)
        self.append(title)

class Card(Element):
    def __init__(self, title, size):
        super().__init__()
        self.outer = '''<div class="col-md-{}"><div class="card shadow mb-4"><div class="card-header py-3"><h6 class="text-primary m-0 fw-bold">{}</h6></div><div class="card-body">{}</div></div></div>'''.format(size, title, "{}")

package = {
    "Element": Element,
    "Page": Page,
    "Heading": Heading,
    "Card": Card
}