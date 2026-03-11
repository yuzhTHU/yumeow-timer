"""
Unit tests for yumeow_timer serialization and timing functionality.
"""
import pytest
import time
from yumeow_timer import Timer, NamedTimer, ParallelTimer


class TestTimerSerialization:
    """Tests for Timer.to_dict() and Timer.from_dict()."""

    def test_timer_to_dict(self):
        """Test Timer.to_dict() returns correct structure."""
        timer = Timer()
        timer.add(10)

        data = timer.to_dict()

        assert '_count' in data
        assert '_time' in data
        assert 'unit' in data
        assert data['unit'] == 'iter'
        assert data['_count'] == 10

    def test_timer_from_dict(self):
        """Test Timer.from_dict() restores state correctly."""
        original = Timer(unit='step')
        original.clear()  # 清空后开始计时（用户典型用法）
        time.sleep(0.01)
        original.add(100)

        restored = Timer.from_dict(original.to_dict())

        assert restored.count == original.count
        assert restored.unit == original.unit
        assert restored.time > 0

    def test_timer_roundtrip(self):
        """Test Timer serialization roundtrip preserves state."""
        original = Timer(unit='batch')
        original.add(50)
        time.sleep(0.01)
        original.add(50)

        restored = Timer.from_dict(original.to_dict())

        assert restored.count == 100
        assert restored.unit == 'batch'


class TestNamedTimerSerialization:
    """Tests for NamedTimer serialization."""

    def test_named_timer_to_dict(self):
        """Test NamedTimer.to_dict() returns correct structure."""
        timer = NamedTimer()
        timer.add('prepare', 10)
        timer.add('forward', 5)

        data = timer.to_dict()

        assert '_count' in data
        assert isinstance(data['_count'], dict)
        assert 'prepare' in data['_count']
        assert 'forward' in data['_count']

    def test_named_timer_from_dict(self):
        """Test NamedTimer.from_dict() restores state correctly."""
        original = NamedTimer()
        original.add('step1', 10)
        original.add('step2', 20)
        time.sleep(0.01)

        restored = NamedTimer.from_dict(original.to_dict())

        assert restored.names == original.names
        assert restored.count == original.count

    def test_named_timer_continue_timing(self):
        """Test that restored NamedTimer can continue timing."""
        original = NamedTimer()
        original.add('prepare', 10)
        time.sleep(0.05)
        original.add('forward', 5)

        restored = NamedTimer.from_dict(original.to_dict())
        restored.add('prepare', 10)  # Add more work

        assert restored.get_named_count('prepare') == 20
        assert restored.get_named_count('forward') == 5


class TestParallelTimerSerialization:
    """Tests for ParallelTimer serialization."""

    def test_parallel_timer_to_dict(self):
        """Test ParallelTimer.to_dict() returns correct structure."""
        timer = ParallelTimer()
        timer.add('process', 10)
        timer.add('render', 5)

        data = timer.to_dict()

        assert '_count' in data
        assert isinstance(data['_count'], dict)
        assert '_time' in data

    def test_parallel_timer_from_dict(self):
        """Test ParallelTimer.from_dict() restores state correctly."""
        original = ParallelTimer()
        original.add('compute', 100)
        original.add('io', 50)
        time.sleep(0.01)

        restored = ParallelTimer.from_dict(original.to_dict())

        assert restored.count == original.count
        assert restored.names == original.names


class TestTimerFunctionality:
    """Tests for basic timer functionality."""

    def test_timer_add(self):
        """Test Timer.add() increments count and time."""
        timer = Timer()
        timer.add(10)

        assert timer.count == 10
        assert timer.time >= 0

    def test_timer_clear(self):
        """Test Timer.clear() resets state."""
        timer = Timer()
        timer.add(100)
        timer.clear()

        assert timer.count == 0
        assert timer.time == 0

    def test_named_timer_multiple_names(self):
        """Test NamedTimer tracks multiple names separately."""
        timer = NamedTimer()
        timer.add('forward', 10)
        timer.add('backward', 5)

        assert timer.get_named_count('forward') == 10
        assert timer.get_named_count('backward') == 5
        assert timer.count == 15

    def test_timer_to_str(self):
        """Test Timer.to_str() with different modes."""
        timer = Timer()
        timer.add(100)

        assert 'iter' in timer.to_str('count')
        assert 's' in timer.to_str('time')
