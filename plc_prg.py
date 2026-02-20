from wagoplc import main, Task

task = Task()

def setup():
    ...

@task(cycletime=5)
def loop(io):
    print(io.digitalRead(1))
    io.digitalWrite(3, True)
    io.digitalWrite(4, True)

if __name__ == "__main__":
    main()