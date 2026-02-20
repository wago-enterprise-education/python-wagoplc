from wagoplc import main,Task,DigitalInput,DigitalOutput

task = Task()

@task.setup
def setup():
    variables = {"xEndlageS1": DigitalInput(1),"xLuefter": DigitalOutput(1)}
    return variables

@task(cycletime=5)
def loop(xEndlageS1):
        if xEndlageS1:
            xLuefter = True
        return locals()

if __name__ == "__main__":
    main()