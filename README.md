# yumeow-timer

Lightweight timing utilities for optional performance diagnostics.

## Installation

```bash
pip install yumeow-timer
```

## Usage

### Basic Timer

```python
from yumeow_timer import Timer

timer = Timer()
for i in range(1000):
    # do something
    timer.add()

print(timer)  # Timer(time=1.23 s, count=1.00 kiter, pace=1.23 ms/iter, speed=813 iter/s)
print(timer.to_str('pace'))  # 1.23 ms/iter
```

### NamedTimer (Multiple Categories)

```python
from yumeow_timer import NamedTimer

timer = NamedTimer()
for i in range(1000):
    if i % 2 == 0:
        timer.add("even")
    else:
        timer.add("odd")

print(timer)  # 1.23 ms/iter (even=1.23 ms/iter[50%]; odd=1.23 ms/iter[50%])
print(timer.to_str('pace', mode_of_detail='pace', mode_of_percent='by_count'))
```

### ParallelTimer (Shared Time)

```python
from yumeow_timer import ParallelTimer

timer = ParallelTimer()
for i in range(1000):
    timer.add("process", n=1)
    timer.add("render", n=1)

print(timer)  # Shows shared time with separate counts
```

### Humanize Functions

```python
from yumeow_timer import humanize_time, humanize_count, humanize_pace, humanize_speed

print(humanize_time(3661))      # 1.02 h
print(humanize_count(1500))     # 1.50 kiter
print(humanize_pace(0.00123))   # 1.23 ms/iter
print(humanize_speed(813))      # 813 iter/s
```

## API Reference

### Timer

Basic timer that tracks time and count.

- `add(n=1, by="increment")` - Add count and elapsed time
- `clear(reset_last_add_time=False)` - Reset timer
- `to_str(mode="pace")` - Get human-readable string
- Properties: `time`, `count`, `pace`, `speed`

### NamedTimer

Extends Timer to track multiple named categories with separate time tracking.

### ParallelTimer

Extends Timer to track multiple named categories with shared time.

## License

MIT License - See LICENSE file for details.
