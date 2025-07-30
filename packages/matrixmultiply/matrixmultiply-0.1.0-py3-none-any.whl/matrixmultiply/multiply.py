def validate_matrix(matrix):
    if not matrix or not isinstance(matrix, list):
        raise ValueError("Matrix must be a non-empty list of lists.")
    row_length = len(matrix[0])
    for row in matrix:
        if not isinstance(row, list) or len(row) != row_length:
            raise ValueError("All rows must be lists of the same length.")


def multiply_matrices(A, B):
    validate_matrix(A)
    validate_matrix(B)

    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])

    if cols_A != rows_B:
        raise ValueError("Number of columns in A must equal number of rows in B.")

    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]

    return result
