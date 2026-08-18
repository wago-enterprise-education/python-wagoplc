import time
import heapq

class WatchdogTimeout(RuntimeError):
    """Throw when task cycle exceeds maximum allowed time."""
    pass

class Task:
    def __init__(
        self,
        name: str,
        cycle_ms: int = 100,
        priority: int = 15,
        function: function = None,
        watchdog_ms: int = 400000,      
        sensitivity: int = 0         
    ):
        """
        name:        task name
        cycle_ms:    call cycle time in ms
        priority:    a priority from 1 (highest) to 15
        function:    name of function
        watchdog_ms: maximum runtime in ms before watchdog interrupts
        sensitivity: sensitivity from 0 (highest) to 10
        """
        self.name = name
        if cycle_ms < 1:
            cycle_ms = 1
        elif cycle_ms > 10000:
            cycle_ms = 10000
        self.cycle = cycle_ms / 1000.0
        if priority not in range(1, 16):
            raise ValueError("priority needs to be in range [1..15] (1 = highest priority).")
        self.priority = priority
        self.function = function
        self.next_run = time.time()
        if watchdog_ms < 0:
            watchdog_ms = 0
        elif watchdog_ms > 400000:
            watchdog_ms = 400000
        self.watchdog_ms = watchdog_ms
        if sensitivity not in range(10):
            raise ValueError("sensitivity needs to be in range [0..10] (0 = highest sensitivity).")
        self.sensitivity = sensitivity
        self.watchdog_ms = self.watchdog_ms * (self.sensitivity * 0.05 + 1)
        
    def __lt__(self, other):
        if isinstance(other, Task):
            return self.priority < other.priority

def scheduler(tasks):
    if not tasks:
        return

    while True:
        now = time.time()
        # the tasks queue
        tasks_ready = []
        
        for t in tasks:
            if now >= t.next_run:
                heapq.heappush(tasks_ready, t)
        
        while tasks_ready:
            task = heapq.heappop(tasks_ready)

            if task.function is None:
                task.next_run += task.cycle
                continue

            start_perf = time.perf_counter()
            try:
                task.function()
            except Exception:
                raise
            finally:
                duration_ms = (time.perf_counter() - start_perf) * 1000.0

                # Watchdog-Check
                if duration_ms > task.watchdog_ms:
                    raise WatchdogTimeout(
                        f"Task '{task.name}' has been caught by the watchdog: "
                        f"{duration_ms:.3f} ms > {task.watchdog_ms} ms "
                    )
                # TODO: find out when next cycle should be scheduled:
                # a full cycle after cycle start or finish?
                task.next_run += task.cycle

        # CPU recovery time
        time.sleep(0.0005)

def fast_task():
    print("fast")

def slow_task():
    time.sleep(0.08)
    print("slow")

if __name__ == "__main__":
    tasks = [
        # 10 ms, highest priority, watchdog 50 ms
        Task("fast", cycle_ms=3, priority=1, function=fast_task, watchdog_ms=50),

        # 100 ms, lowest priority, watchdog 80 ms
        Task("slow", cycle_ms=100, priority=15, function=slow_task, watchdog_ms=80, sensitivity=1),
    ]
    
scheduler(tasks)