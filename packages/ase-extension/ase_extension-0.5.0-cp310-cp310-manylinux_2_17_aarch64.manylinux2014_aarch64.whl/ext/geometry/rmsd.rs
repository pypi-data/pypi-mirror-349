#![allow(non_snake_case)]

use nalgebra::{Matrix4, MatrixXx3, Quaternion, UnitQuaternion};
use numpy::{PyArray2, PyReadonlyArray2, ToPyArray};
use pyo3::prelude::*;
use std::ops::AddAssign;

fn subtract_centroid(pos: MatrixXx3<f64>) -> MatrixXx3<f64> {
    let centroid = pos.row_mean();
    let mut result = pos;
    for i in 0..result.nrows() {
        result.row_mut(i).add_assign(-&centroid);
    }
    result
}

fn rmsd(X: &MatrixXx3<f64>, Y: &MatrixXx3<f64>) -> f64 {
    let diff = X - Y;
    diff.map(|x| x * x).column_sum().mean().sqrt()
}

/// The result of the RMSD calculation.
/// Attributes:
///    val: The RMSD value.
///    grad: The gradient of the RMSD value w.r.t the first given position.
///    rotation: The rotation matrix for the second given position.
///    translation: The translation vector which maps to the original positions.
#[pyclass]
pub struct RMSDResult {
    #[pyo3(get)]
    val: f64,
    #[pyo3(get)]
    grad: Py<PyArray2<f64>>,
    #[pyo3(get)]
    rotation: Py<PyArray2<f64>>,
    #[pyo3(get)]
    translation: Py<PyArray2<f64>>,
}

#[pymethods]
impl RMSDResult {
    fn __repr__(&self) -> PyResult<String> {
        Ok(format!(
            "RMSDResult(val={:.6}, grad=..., rotation=..., translation=...)",
            self.val,
        ))
    }
}
/// Computes the root mean square deviation (RMSD) between two sets of positions.
/// Args:
///    pos_1: The first set of positions.
///    pos_2: The second set of positions.
/// Returns:
///    RMSDResult: The result of the RMSD calculation.
#[pyfunction]
#[pyo3(signature = (pos_1, pos_2))]
pub fn compute_rmsd<'py>(
    _py: Python<'py>,
    pos_1: PyReadonlyArray2<f64>,
    pos_2: PyReadonlyArray2<f64>,
) -> RMSDResult {
    // ) -> Bound<'py, PyArray2<f64>> {
    let X = subtract_centroid(pos_1.as_matrix().fixed_columns::<3>(0).into_owned());
    let Y = subtract_centroid(pos_2.as_matrix().fixed_columns::<3>(0).into_owned());

    // Find the optimal rotation matrix
    // 1. Compute the covariance matrix R and "F matrix"
    let R = &X.transpose() * &Y;
    #[rustfmt::skip]
    let F = Matrix4::new(
        R[(0, 0)] + R[(1, 1)] + R[(2, 2)],  R[(1, 2)] - R[(2, 1)],              R[(2, 0)] - R[(0, 2)],              R[(0, 1)] - R[(1, 0)],
        R[(1, 2)] - R[(2, 1)],              R[(0, 0)] - R[(1, 1)] - R[(2, 2)],  R[(0, 1)] + R[(1, 0)],              R[(0, 2)] + R[(2, 0)],
        R[(2, 0)] - R[(0, 2)],              R[(0, 1)] + R[(1, 0)],             -R[(0, 0)] + R[(1, 1)] - R[(2, 2)],  R[(1, 2)] + R[(2, 1)],
        R[(0, 1)] - R[(1, 0)],              R[(0, 2)] + R[(2, 0)],              R[(1, 2)] + R[(2, 1)],             -R[(0, 0)] - R[(1, 1)] + R[(2, 2)],
    );
    // 2. Find rotation matrix U
    let eig = F.symmetric_eigen();
    let q = {
        let q = eig.eigenvectors.column(eig.eigenvalues.imax());
        let q = Quaternion::new(q[0], q[1], q[2], q[3]);
        UnitQuaternion::from_quaternion(q)
    };
    let U = q.to_rotation_matrix();

    // 3. Rotate Y and compute RMSD
    let Y_rot = &Y * U;
    let rmsd_val = rmsd(&X, &Y_rot);

    // 4. Compute gradient
    let denominator = (X.nrows() as f64) * rmsd_val + 1e-12;
    let diff_rot = &X - &Y_rot;
    let rmsd_grad = diff_rot / denominator;

    RMSDResult {
        val: rmsd_val,
        grad: rmsd_grad.to_pyarray(_py).to_owned().unbind(),
        rotation: U.matrix().transpose().to_owned().to_pyarray(_py).unbind(),
        translation: (X.row_mean() - Y.row_mean() * U)
            .to_pyarray(_py)
            .to_owned()
            .unbind(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_subtract_centroid() {
        let pos = MatrixXx3::from_row_slice(&[
            0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0,
        ]);
        let pos_centered = subtract_centroid(pos);
        let centroid = pos_centered.row_mean();

        assert_eq!(centroid, MatrixXx3::from_row_slice(&[0.0, 0.0, 0.0]));
    }
}
