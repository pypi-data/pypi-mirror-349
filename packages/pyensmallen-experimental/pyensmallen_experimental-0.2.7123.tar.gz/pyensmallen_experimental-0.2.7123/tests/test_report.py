import numpy as np
import pyensmallen as pye

def square(x):
    return x@x

def objective_function(x, grad):
    grad[:] = 2*x
    return square(x)
   
# Initial guess
initial_x = np.array([-1000, 1000.0])

def test_report_is_optional():
	optimizer = pye.L_BFGS()
	# Run optimization without passing a report
	result_ens = optimizer.optimize(objective_function, initial_x)
	expected_coordinates = np.array([-1.13686838e-13, 1.13686838e-13])
	assert np.allclose(result_ens, expected_coordinates, atol=1e-6)


def test_report():
	# pyensmallen solution
	optimizer = pye.L_BFGS()
	res = {}
	report = pye.Report(res, disableOutput=True)
	result_ens = optimizer.optimize(objective_function, initial_x, report=report)
    # Expected values
    expected_coordinates = np.array([-1.13686838e-13, 1.13686838e-13])
    expected_obj = 2.5849394142282115e-26
    expected_iters = 2
    expected_evals = 10
    expected_grads = 10

    # Check objective value is close enough
    assert abs(res['objective_value'] - expected_obj) < 1e-6
    # should match exactly
    assert res['iterations'] == expected_iters
    assert res['evaluate_calls'] == expected_evals
    assert res['gradient_calls'] == expected_grads
    # Check final coordinates are close enough
    assert np.allclose(result_ens, expected_coordinates, atol=1e-6)
