<div align="center">

# ⏱️ yumeow-timer

[![PyPI - Version](https://img.shields.io/pypi/v/yumeow-timer?style=flat&logo=pypi&logoColor=white)](https://pypi.org/project/yumeow-timer/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/yumeow-timer?style=flat&logo=pypi&logoColor=white)](https://pypi.org/project/yumeow-timer/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/yumeow-timer?style=flat&logo=python&logoColor=white)](https://pypi.org/project/yumeow-timer/)
[![GitHub License](https://img.shields.io/github/license/yuzhTHU/yumeow-timer?style=flat&logo=github)](https://github.com/yuzhTHU/yumeow-timer)
[![GitHub Stars](https://img.shields.io/github/stars/yuzhTHU/yumeow-timer?style=flat&logo=github&logoColor=white)](https://github.com/yuzhTHU/yumeow-timer)
[![Tests](https://img.shields.io/github/actions/workflow/status/yuzhTHU/yumeow-timer/test.yml?style=flat&logo=pytest&logoColor=white)](https://github.com/yuzhTHU/yumeow-timer)

**Lightweight timing utilities for performance diagnostics**

*Perfect for tracking training loops, API calls, and token usage in ML workflows*

</div>

---

## ✨ Features

- 🎯 **Three timer types** - `Timer`, `NamedTimer`, `ParallelTimer` for different use cases
- 📊 **Human-readable output** - Auto-scales to μs, ms, s, min, h, day with smart formatting
- 💾 **Serialization** - Save/restore timer state for checkpoint-resume workflows
- 🧪 **Tested** - Full unit test coverage with pytest
- 🚀 **Zero dependencies** - Only requires `numpy` and `pandas`

## 📦 Installation

```bash
pip install yumeow-timer
```

## 🚀 Quick Start

### Basic Timer

```python
from yumeow_timer import Timer

timer = Timer()
for i in range(1000):
    # do something
    timer.add()

print(timer)              # Timer(time=1.23 s, count=1.00 kiter, pace=1.23 ms/iter, speed=813 iter/s)
print(timer.to_str('pace'))  # 1.23 ms/iter
```

### NamedTimer - Training Loop Example

Track time spent in each phase of your training loop:

```python
from yumeow_timer import NamedTimer

timer = NamedTimer()
for epoch in range(num_epochs):
    timer.clear()  # Reset for this epoch

    timer.add('prepare_data')
    data = load_data()

    timer.add('forward')
    loss = model(data)

    timer.add('backward')
    loss.backward()

    timer.add('optimizer')
    optimizer.step()

    print(f"Epoch {epoch}: {timer.to_str('pace', mode_of_detail='pace', mode_of_percent='by_time')}")
```

Output: `2.34 s/iter (forward=1.20 s/iter[51%]; backward=0.80 s/iter[34%]; prepare_data=0.24 s/iter[10%]; optimizer=0.10 s/iter[5%])`

### ParallelTimer - Token Usage Counter

Track token usage across different categories with shared timing:

```python
from yumeow_timer import ParallelTimer

token_counter = ParallelTimer(unit='token')

# After each API call
token_counter.add('reasoning', n=reason_tokens)
token_counter.add('prompt', n=prompt_tokens)
token_counter.add('answer', n=answer_tokens)

print(f"Total: {token_counter.count:,} tokens")
print(f"Speed: {token_counter.speed:.0f} tokens/s")
print(f"Breakdown: {token_counter.to_str(mode_of_detail='count', mode_of_percent='by_count')}")
```

Output: `1.50 ktoken (answer=1.00 ktoken[67%]; prompt=400 tokens[27%]; reasoning=100 tokens[7%])`

### Checkpoint/Resume Support

Save and restore timer state across training sessions:

```python
import torch
from yumeow_timer import NamedTimer

# Save checkpoint
torch.save({
    'model': model.state_dict(),
    'optimizer': optimizer.state_dict(),
    'timer': timer.to_dict(),  # Persist timer state
}, 'checkpoint.pth')

# Resume training
checkpoint = torch.load('checkpoint.pth')
timer = NamedTimer.from_dict(checkpoint['timer'])  # Continue from saved state
```

## 📖 API Reference

### Timer

| Method | Description |
|--------|-------------|
| `__init__(unit="iter")` | Initialize timer with custom unit name |
| `add(n=1, by="increment")` | Add count and elapsed time |
| `clear(reset_last_add_time=True)` | Reset timer state |
| `to_str(mode="pace")` | Get human-readable string |

**Modes**: `time`, `count`, `pace`, `speed`

**Properties**: `time`, `count`, `pace`, `speed`, `time_str`, `count_str`, `pace_str`, `speed_str`

### NamedTimer

Extends `Timer` with **per-category time tracking**. Each `add(name, n)` call tracks time and count separately for each named category.

### ParallelTimer

Extends `Timer` with **per-category count** but **shared time**. Perfect for token counters where all categories share the same time window.

## 🧪 Running Tests

```bash
pip install pytest
pytest tests/ -v
```

## 📄 License

[MIT License](LICENSE) - © 2024 YuMeow

---

<div align="center">

[Report Bug](https://github.com/yuzhTHU/yumeow-timer/issues) · [Request Feature](https://github.com/yuzhTHU/yumeow-timer/issues) · [View on PyPI](https://pypi.org/project/yumeow-timer/)

</div>
