import sys
import numpy as np

def purity_score(clusters, classes):
    """
    Calculate the purity score for the given cluster assignments and ground truth classes
    
    :param clusters: the cluster assignments array
    :type clusters: numpy.array
    
    :param classes: the ground truth classes
    :type classes: numpy.array
    
    :returns: the purity score
    :rtype: float
    """
    
    A = np.c_[(clusters,classes)]

    n_accurate = 0.

    for j in np.unique(A[:,0]):
        z = A[A[:,0] == j, 1]
        x = np.argmax(np.bincount(z))
        n_accurate += len(z[z == x])

    return n_accurate / A.shape[0]

ground_label = sys.argv[1]
pred_label = sys.argv[2]
labels = np.loadtxt(ground_label, dtype='int32')
preds = np.loadtxt(pred_label, dtype='int32')
print 'The purity is: ', purity_score(preds, labels)