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