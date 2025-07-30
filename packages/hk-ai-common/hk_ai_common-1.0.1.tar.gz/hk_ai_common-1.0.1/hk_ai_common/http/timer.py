from logging import getLogger
import time

logger = getLogger(__name__)

class Timer:
    def __init__(self):
        self.start_time = None
        self.elapsed = 0.0

    def start(self):
        """Start the timer."""
        # 如果计时器已经在运行，则不进行任何操作
        if self.start_time is not None:
            logger.warning('Timer已运行中')
            return  # 或者打印一条消息，例如 "Timer is already running."
        self.start_time = time.time()

    def stop(self):
        """Stop the timer."""
        # 如果计时器没有在运行，则不进行任何操作
        if self.start_time is None:
            logger.warning('Timer已停止运行中')
            return  # 或者打印一条消息，例如 "Timer is not running."
        elapsed_time = time.time() - self.start_time
        self.elapsed += elapsed_time
        self.start_time = None  # Reset start time for the next interval

    def reset(self):
        """Reset the timer."""
        self.start_time = None
        self.elapsed = 0.0

    def elapsed_time(self):
        """Get the total elapsed time in seconds."""
        if self.start_time is not None:
            current_time = time.time()
            return self.elapsed + (current_time - self.start_time)
        return self.elapsed

    def is_running(self):
        """Check if the timer is currently running."""
        return self.start_time is not None

# Example usage
if __name__ == "__main__":
    timer = Timer()

    timer.start()
    time.sleep(2)  # Simulate some work
    timer.stop()

    print(f"Elapsed time: {timer.elapsed_time()} seconds")  # Should print around 2 seconds

    timer.start()
    time.sleep(3)  # Simulate more work
    timer.stop()

    print(f"Total elapsed time: {timer.elapsed_time()} seconds")  # Should print around 5 seconds

    # Test cases to show behavior without exceptions
    timer.stop()  # No effect, since the timer is already stopped
    timer.start()  # Start again
    time.sleep(1)
    timer.stop()  # Stop the timer again
    print(f"Elapsed time after additional stop: {timer.elapsed_time()} seconds")  # Should print around 6 seconds
