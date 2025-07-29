#![allow(non_snake_case)]
#![allow(clippy::upper_case_acronyms)]
use nalgebra::{Matrix3, RowVector3};
use numpy::{PyArray2, PyReadonlyArray1, PyReadonlyArray2, ToPyArray};
use pyo3::{prelude::*, types::PyDict};
use std::ops::AddAssign;

fn finc_mic(dR: &RowVector3<f64>, cell: &Matrix3<f64>, pbc: &[bool; 3]) -> RowVector3<f64> {
    let mut inv_cell = cell.try_inverse().unwrap_or(Matrix3::zeros());
    // Mask nonperiodic directions
    pbc.iter()
        .enumerate()
        .filter(|(_, &p)| !p)
        .for_each(|(i, _)| {
            inv_cell.row_mut(i).scale_mut(0.0);
        });
    let offset = (dR * inv_cell).map(|x| x.round()) * cell;
    dR - offset
}

#[pyclass]
#[derive(Clone)]
pub struct SHAKE {
    #[pyo3(get, set)]
    bond_indices: Vec<(usize, usize)>,
    #[pyo3(get, set)]
    bond_lengths: Option<Vec<f64>>,
    #[pyo3(get)]
    max_iter: usize,
    #[pyo3(get)]
    rtol: f64,
}

#[pymethods]
impl SHAKE {
    #[new]
    pub fn new(
        bond_indices: Vec<(usize, usize)>,
        bond_lengths: Option<Vec<f64>>,
        max_iter: usize,
        rtol: f64,
    ) -> Self {
        SHAKE {
            bond_indices,
            bond_lengths,
            max_iter,
            rtol,
        }
    }

    pub fn adjust_positions<'py>(
        &self,
        _py: Python<'py>,
        old_pos: PyReadonlyArray2<f64>,
        new_pos: PyReadonlyArray2<f64>,
        masses: PyReadonlyArray1<f64>,
        cell: PyReadonlyArray2<f64>,
        pbc: [bool; 3],
    ) -> PyResult<Bound<'py, PyArray2<f64>>> {
        let bond_lengths = self.bond_lengths.as_ref().ok_or_else(|| {
            pyo3::exceptions::PyValueError::new_err(
                "bond_lengths must be provided before calling adjust_positions",
            )
        })?;
        let old_pos = old_pos.as_matrix();
        let old_pos = old_pos.fixed_columns::<3>(0);

        let new_pos = new_pos.as_matrix();
        let mut new_pos = new_pos.fixed_columns::<3>(0).into_owned();

        let cell = cell.as_matrix();
        let cell = cell.fixed_columns::<3>(0);
        let cell = cell.fixed_rows::<3>(0);

        for step in 0..self.max_iter {
            let mut converged = true;
            for (n, &(i, j)) in self.bond_indices.iter().enumerate() {
                let r = bond_lengths.get(n).unwrap(); // bond length
                let r0 = old_pos.row(i) - old_pos.row(j);
                let d0 = finc_mic(&r0, &cell.into_owned(), &pbc);
                let d1 = new_pos.row(i) - new_pos.row(j) - r0 + d0;

                let (m_i, m_j) = (masses.get(i).unwrap(), masses.get(j).unwrap());
                let m = 1.0 / (1.0 / m_i + 1.0 / m_j);
                let x = 0.5 * (r.powi(2) - d1.dot(&d1)) / d0.dot(&d1);

                if x.abs() > self.rtol {
                    new_pos.row_mut(i).add_assign(x * m / m_i * d0);
                    new_pos.row_mut(j).add_assign(-x * m / m_j * d0);
                    converged = false;
                }
            }
            if converged {
                break;
            }
            if step == self.max_iter - 1 {
                return Err(pyo3::exceptions::PyRuntimeError::new_err(
                    "SHAKE did not converge",
                ));
            }
        }

        Ok(new_pos.to_pyarray(_py))
    }

    pub fn adjust_momenta<'py>(
        &self,
        _py: Python<'py>,
        old_pos: PyReadonlyArray2<f64>,
        momenta: PyReadonlyArray2<f64>,
        masses: PyReadonlyArray1<f64>,
        cell: PyReadonlyArray2<f64>,
        pbc: [bool; 3],
    ) -> PyResult<Bound<'py, PyArray2<f64>>> {
        let bond_lengths = self.bond_lengths.as_ref().ok_or_else(|| {
            pyo3::exceptions::PyValueError::new_err(
                "bond_lengths must be provided before calling adjust_positions",
            )
        })?;
        let old_pos = old_pos.as_matrix();
        let old_pos = old_pos.fixed_columns::<3>(0);

        let momenta = momenta.as_matrix();
        let mut momenta = momenta.fixed_columns::<3>(0).into_owned();

        let cell = cell.as_matrix();
        let cell = cell.fixed_columns::<3>(0);
        let cell = cell.fixed_rows::<3>(0);

        for step in 0..self.max_iter {
            let mut converged = true;
            for (n, &(i, j)) in self.bond_indices.iter().enumerate() {
                let r = bond_lengths.get(n).unwrap(); // bond length
                let d = old_pos.row(i) - old_pos.row(j);
                let d = finc_mic(&d, &cell.into_owned(), &pbc);

                let dv = momenta.row(i) / *masses.get(i).unwrap()
                    - momenta.row(j) / *masses.get(j).unwrap();

                let (m_i, m_j) = (masses.get(i).unwrap(), masses.get(j).unwrap());
                let m = 1.0 / (1.0 / m_i + 1.0 / m_j);
                let x = -dv.dot(&d) / r.powi(2);

                if x.abs() > self.rtol {
                    momenta.row_mut(i).add_assign(x * m * d);
                    momenta.row_mut(j).add_assign(-x * m * d);
                    converged = false;
                }
            }
            if converged {
                break;
            }
            if step == self.max_iter - 1 {
                return Err(pyo3::exceptions::PyRuntimeError::new_err(
                    "SHAKE did not converge",
                ));
            }
        }

        Ok(momenta.to_pyarray(_py))
    }

    pub fn __deepcopy__(&self, _memo: Py<PyDict>) -> Self {
        self.clone()
    }
}
