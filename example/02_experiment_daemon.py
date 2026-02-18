import daemon

def do_main_program():
    # do stuff...
    import time
    while True:
        print("Hello, World!")
        time.sleep(1)

with daemon.DaemonContext():
    do_main_program()
