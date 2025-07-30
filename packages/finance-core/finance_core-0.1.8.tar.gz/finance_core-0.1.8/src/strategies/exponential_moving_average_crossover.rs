use pyo3::{exceptions::PyValueError, prelude::*};

use crate::traits::{Next, Reset};

use crate::ExponentialMovingAverage;

use crate::Signal;

#[pyclass]
pub struct ExponentialMovingAverageCrossover {
    short_sma: ExponentialMovingAverage,
    long_sma: ExponentialMovingAverage,
}

#[pymethods]
impl ExponentialMovingAverageCrossover {
    #[new]
    pub fn new(short_period: usize, long_period: usize) -> PyResult<Self> {
        if short_period >= long_period {
            return Err(PyValueError::new_err(
                "Short period must be less than long period."
            ))
        }

        Ok(Self {
            short_sma: ExponentialMovingAverage::new(short_period)?,
            long_sma: ExponentialMovingAverage::new(long_period)?,
        })
    }

    pub fn next(&mut self, input: f64) -> Signal {
        Next::next_rs(self, input)
    }

    pub fn reset(&mut self) {
        Reset::reset_rs(self);
    }
}

impl Next<f64> for ExponentialMovingAverageCrossover {
    type Output = Signal;

    fn next_rs(&mut self, input: f64) -> Self::Output {

        let crossover = self.short_sma.next(input) - self.long_sma.next(input);

        if crossover > 0.0 {
            return Signal::BUY
        } else if crossover < 0.0 {
            return Signal::SELL
        } else {
            return Signal::HOLD
        }

    }
}

impl Reset for ExponentialMovingAverageCrossover {
    fn reset_rs(&mut self) {
        self.short_sma.reset_rs();
        self.long_sma.reset_rs();
    }
}