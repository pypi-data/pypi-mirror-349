import numpy as np

def tau_ap(x, y):
    """
    Compute the Tau AP correlation coefficient as defined in:
    Yilmaz, E., Aslam, J. A., & Robertson, S. (2008). A new rank correlation coefficient for information retrieval.
    In Proceedings of the 31st annual international ACM SIGIR conference on Research and development in information retrieval.

    DOI: https://doi.org/10.1145/1390334.139043

    Assumes no ties in the data.
    """
    assert len(x) == len(y), "Input lists must have the same length"
    n = len(x)
    sum_term = 0.0
    for i in range(1, n):
        inner_sum = 0
        for j in range(i):
            if np.sign(x[i] - x[j]) == np.sign(y[i] - y[j]):
                inner_sum += 1
        sum_term += inner_sum / i
    return (2 / (n - 1)) * sum_term - 1
