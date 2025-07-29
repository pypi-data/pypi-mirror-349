use numpy::{PyArray2, PyReadonlyArray2, ToPyArray};
use pyo3::prelude::*;

const K_B: f64 = 8.617_330_337_217_213e-5;

#[pyfunction]
pub fn log_fermi_spherical_wall_potential<'py>(
    _py: Python<'py>,
    positions: PyReadonlyArray2<f64>,
    radius: f64,
    temperature: f64,
    beta: f64,
) -> (f64, Bound<'py, PyArray2<f64>>) {
    let eps = 1e-9;
    let dists = positions
        .as_matrix()
        .map(|x| x.powi(2))
        .column_sum()
        .map(f64::sqrt);
    let exp_term = (beta * (&dists.add_scalar(-radius))).map(f64::exp);
    let k_t = K_B * temperature;
    let e_i = k_t * (exp_term.add_scalar(1.0)).map(f64::ln);
    let e = e_i.sum();
    let grad_multiplier = (k_t * beta * &exp_term)
        .component_div(&((&dists * &exp_term.add_scalar(1.0)).add_scalar(eps)));
    // Multiply each element of grad_multiplier by the corresponding row of positions
    let mut e_grad = (positions.as_matrix()).into_owned().clone();
    for (i, mut row) in e_grad.row_iter_mut().enumerate() {
        row *= grad_multiplier[i];
    }
    (e, e_grad.to_pyarray(_py))
}
