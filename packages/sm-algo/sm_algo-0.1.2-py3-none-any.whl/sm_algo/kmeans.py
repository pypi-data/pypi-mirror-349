import numpy as np
from scipy.spatial.distance import cdist


class KMeans:
    """K-Means clustering algorithm.

    Parameters
    ----------
    n_clusters : int, default=8
        The number of clusters to form as well as the number of centroids to generate.
    max_iter : int, default=300
        Maximum number of iterations of the k-means algorithm for a single run.
    tol : float, default=1e-4
        Relative tolerance with regards to Frobenius norm of the difference
        in the cluster centers of two consecutive iterations to declare convergence.
    random_state : int, optional
        Determines random number generation for centroid initialization. Use an int
        to make the randomness deterministic.

    Attributes
    ----------
    centroids : ndarray of shape (n_clusters, n_features)
        Coordinates of cluster centers.
    labels_ : ndarray of shape (n_samples,)
        Labels of each point.
    """

    def __init__(self, n_clusters=8, max_iter=300, tol=1e-4, random_state=None):
        """Initialize KMeans instance with given parameters."""

        if n_clusters <= 0:
            raise ValueError("n_clusters must be > 0")
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state
        self.centroids = None
        self.labels_ = None

    def _initialize_centroids(self, X):
        """Initialize centroids using k-means++ algorithm.

        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            The input data.

        Raises
        ------
        ValueError
            If n_clusters > number of samples.
        """
        if self.n_clusters > X.shape[0]:
            raise ValueError("n_clusters cannot be > number of samples")

        np.random.seed(self.random_state)
        centroids = [X[np.random.randint(X.shape[0])]]

        for _ in range(1, self.n_clusters):
            distances = np.min(cdist(X, centroids, 'sqeuclidean'), axis=1)
            prob = distances / distances.sum()
            next_centroid = X[np.random.choice(X.shape[0], p=prob)]
            centroids.append(next_centroid)

        self.centroids = np.array(centroids)

    def _compute_distances(self, X):
        """Compute Euclidean distances between points and centroids.

        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            The input data.

        Returns
        -------
        ndarray of shape (n_samples, n_clusters)
            Array of distances from each point to each centroid.
        """
        return cdist(X, self.centroids, 'euclidean')

    def fit(self, X):
        """Compute k-means clustering.

        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            Training instances to cluster.

        Returns
        -------
        self : object
            Fitted estimator.

        Raises
        ------
        ValueError
            If X is empty.
        """
        if len(X) == 0:
            raise ValueError("X cannot be empty")

        self._initialize_centroids(X)

        for _ in range(self.max_iter):
            distances = self._compute_distances(X)
            self.labels_ = np.argmin(distances, axis=1)

            new_centroids = []
            for i in range(self.n_clusters):
                cluster_points = X[self.labels_ == i]
                if len(cluster_points) == 0:
                    new_centroids.append(self.centroids[i])  # Keep old centroid
                else:
                    new_centroids.append(cluster_points.mean(axis=0))

            new_centroids = np.array(new_centroids)

            if np.allclose(self.centroids, new_centroids, atol=self.tol):
                break

            self.centroids = new_centroids
        return self

    def predict(self, X):
        """Predict the closest cluster each sample in X belongs to.

        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            New data to predict.

        Returns
        -------
        labels : ndarray of shape (n_samples,)
            Index of the cluster each sample belongs to.

        Raises
        ------
        ValueError
            If the model is not fitted yet.
        """
        if self.centroids is None:
            raise ValueError("Model not fitted yet. Call fit() first.")
        return np.argmin(self._compute_distances(X), axis=1)