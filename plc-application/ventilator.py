def fan(xTaster):
    xLuefter = False
    if xTaster:
        xLuefter = not xLuefter

    return dict(xLuefter=xLuefter)
