use pyo3::{exceptions::PyValueError, prelude::*};

use crate::traits::{Next, Period, Reset};

#[pyclass]
pub struct SimpleMovingAverage {
    period: usize,
    index: usize,
    count: usize,
    sum: f64,
    deque: Vec<f64>,
}

#[pymethods]
impl SimpleMovingAverage {
    #[new]
    pub fn new(period: usize) -> PyResult<Self> {
        match period {
            0 => Err(PyValueError::new_err("Period cannot be 0.")),
            _ => Ok(Self {
                period,
                index: 0,
                count: 0,
                sum: 0.0,
                deque: vec![0.0; period],
            })
        }
    }

    pub fn period(&mut self) -> usize {
        Period::period_rs(self)
    }

    pub fn next(&mut self, input: f64) -> f64 {
        Next::next_rs(self, input)
    }

    pub fn reset(&mut self) {
        Reset::reset_rs(self)
    }
}

impl Period for SimpleMovingAverage {
    fn period_rs(&self) -> usize {
        self.period
    }
}

impl Next<f64> for SimpleMovingAverage {
    type Output = f64;

    fn next_rs(&mut self, input: f64) -> Self::Output {
        let old_value = self.deque[self.index];
        self.deque[self.index] = input;

        self.index = if self.index + 1 < self.period {
            self.index + 1
        } else {
            0
        };

        if self.count < self.period {
            self.count += 1
        };

        self.sum += input - old_value;
        self.sum / self.count as f64
    }
}

impl Reset for SimpleMovingAverage {
    fn reset_rs(&mut self) {
        self.index = 0;
        self.count = 0;
        self.sum = 0.0;
        for i in 0..self.period {
            self.deque[i] = 0.0;
        }
    }
}
