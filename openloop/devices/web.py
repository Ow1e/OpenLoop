from openloop.crossweb import *

def view_groups():
    p = Page()
    p.append(Heading("Device / Instance Groups", 0))

    c = Card("Groups", 12)
    
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
    c.append(Button("success", "fas fa-plus", href="/api/create", text="Create"))
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

def prompt_name(name):
    p = Page()
    c = Card("Prompt", 6)
    c.append(Heading(f"Are you sure you want to delete {name}?", 4))
    c.append(Text("This cannot be undone and can only be operated by admins.", "danger"))
    form = HTML_Form("")
    form.append(Form_Button("Confirm", "danger"))
    c.append(form)
    p.append(c)   
    return p.export() 

def create_group_prompt():
    p = Page()
    p.append(Heading("Create Group", 0))
    c = Card("Create Group", 6)
    c.append(Text("This action can only be used by admins.", "danger"))
    form = HTML_Form("")
    
    name = Form_Element()
    name.append(Label("Name"))
    name.append(Input("name", required=True))

    form.append(name)
    form.append(Form_Button())
    c.append(form)
    p.append(c)
    return p.export()

def create_api_prompt():
    p = Page()
    p.append(Heading("Create Device", 0))

    c = Card("Create Device")
    form = Form()
    
    name = Form_Element()
    name.append(Label("Name"))
    name.append(Input("name"))
    form.append(name)

    
    