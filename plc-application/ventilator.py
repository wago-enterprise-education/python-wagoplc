from wagoplc import Tasks, main, DI, DO

tasks = Tasks()

@tasks.register
def fan(xTaster):
    if xTaster:
        if xLuefter:
            xLuefter = False
        else:
            xLuefter = True

    return locals()
