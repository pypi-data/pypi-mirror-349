use pyo3::prelude::*;

mod traits;
pub use crate::traits::*;

mod indicators;
pub use crate::indicators::{
    AverageTrueRange,
    ExponentialMovingAverage, 
    Maximum, 
    Minimum, 
    MovingAverageConvergenceDivergence,
    RateOfChange,
    RelativeStrengthIndex,
    SharpeRatio,
    SimpleMovingAverage, 
    StandardDeviation,
    TrueRange
};

mod strategies;
pub use crate::strategies::{
    ExponentialMovingAverageCrossover,
    SimpleMovingAverageCrossover
};

mod bar;
pub use crate::bar::Bar;

mod signal;
pub use crate::signal::Signal;

/// A Python module implemented in Rust.
#[pymodule]
fn _finance_core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // models
    m.add_class::<Bar>()?;
    m.add_class::<Signal>()?;
    
    // indicators
    m.add_class::<AverageTrueRange>()?;
    m.add_class::<ExponentialMovingAverage>()?;    
    m.add_class::<Maximum>()?;
    m.add_class::<Minimum>()?;
    m.add_class::<MovingAverageConvergenceDivergence>()?;
    m.add_class::<RateOfChange>()?;
    m.add_class::<RelativeStrengthIndex>()?;
    m.add_class::<SharpeRatio>()?;
    m.add_class::<SimpleMovingAverage>()?;
    m.add_class::<StandardDeviation>()?;
    m.add_class::<TrueRange>()?;

    // strategies
    m.add_class::<ExponentialMovingAverageCrossover>()?;
    m.add_class::<SimpleMovingAverageCrossover>()?;
    Ok(())
}
