from datetime import datetime

def convert_zones(datetype : datetime):
    rel = datetype
    now = datetime.utcnow()
    change = now-rel
    ans = ""
    
    days = change.days
    if days == 0:
        secs = change.total_seconds()
        if secs < 60: # Totals one minute
            return f"{int(secs)} second ago."
        elif secs < 3600: # Totals one hour
            return f"{int(secs/60)} minutes ago."
        elif int(secs/3600)==1:
            return "1 hour ago."
        else:
            return f"{int(secs/3600)} hours ago."
    elif days == 1:
        return "Yesterday"
    else:
        month = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"][rel.month]
        day = ["Monday", "Tuesday", "Wendsday", "Thursday", "Friday", "Saturday", "Sunday"][rel.weekday()]
        return f"{day}, {month} {rel.day} {rel.year}"