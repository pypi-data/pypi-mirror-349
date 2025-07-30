import finance_core as fc
import pytest


def test_init():

    with pytest.raises(ValueError, match="Short period must be less than long period."):
        fc.SimpleMovingAverageCrossover(2, 1)


def test_next():

    sma_crossover = fc.SimpleMovingAverageCrossover(1, 2)

    assert sma_crossover.next(1.0) == fc.Signal.HOLD
    assert sma_crossover.next(2.0) == fc.Signal.BUY


def test_reset():

    sma_crossover = fc.SimpleMovingAverageCrossover(1, 2)

    assert sma_crossover.next(1.0) == fc.Signal.HOLD

    sma_crossover.reset()
    assert sma_crossover.next(2.0) == fc.Signal.HOLD
