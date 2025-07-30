from matrixmultiply import multiply_matrices

def test_multiply():
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    expected = [[19, 22], [43, 50]]
    assert multiply_matrices(A, B) == expected
