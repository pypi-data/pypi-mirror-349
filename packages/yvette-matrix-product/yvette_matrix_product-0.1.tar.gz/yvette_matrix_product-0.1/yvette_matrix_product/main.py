def matrixtproduct(A, B):
    """
    Multiplies two matrices a and b.
    :param a: First matrix
    :param b: Second matrix
    :return: Resultant matrix after multiplication
    """
    if len(A[0]) != len(B):
        raise ValueError("""Number of columns in A must be equal to number
                         of rows in B""")

    result = [[0 for j in range(len(B[0]))] for i in range(len(A))]

    for row in range(len(A)):
        for col in range(len(B[0])):
            sum = 0
            for value in range(len(B)):
                sum += A[row][value] * B[value][col]
        result[row][col] = sum
    return result
