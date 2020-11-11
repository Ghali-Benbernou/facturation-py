def list_display(liste):
    listing = ""
    for i, e in enumerate(liste):
        listing += "N " + str(i + 1) + ": " + str(e)
        if i < len(liste) - 1:
            listing += "\n"
    return listing