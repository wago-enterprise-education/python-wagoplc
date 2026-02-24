from wagoplc import main, Task

task = Task()

@task(
    cycletime=4,
    watchdog=10
)
def loop(io):
    print(io.digitalRead(1))
    io.digitalWrite(3, True)
    io.digitalWrite(4, True)

if __name__ == "__main__":
    main()