from openloop.crossweb import *

def view_groups():
    p = Page()
    p.append(Heading("Device / Instance Groups", 0))

    c = Card("Groups", 8, padding=False)
    
    table = Table()

    header = Table_Header()
    row = Table_Row()

    row.append(Table_Cell("Name"))
    row.append(Table_Cell("Devices"))
    row.append(Table_Cell("Instances"))
    row.append(Table_Cell("Options"))
    header.append(row)

    table.append(header)
    body = Table_Body()
    body.add_flow("pages.devices.groups")
    table.append(body)
    
    c.append(table)
    p.append(c)
    return p.export()

def prompt():
    p = Page()
    c = Card("Prompt", 6)
    c.append(Heading("Are you sure you want to delete this group?", 4))
    c.append(Text("This cannot be undone and can only be operated by admins.", "danger"))
    form = HTML_Form("")
    form.append(Form_Button("Confirm", "danger"))
    c.append(form)
    p.append(c)
    return p.export()