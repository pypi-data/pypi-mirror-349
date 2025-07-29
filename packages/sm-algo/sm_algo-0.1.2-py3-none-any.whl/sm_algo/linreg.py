import numpy as np


class LinearRegression:
    """A linear regression model trained using gradient descent.

    Attributes:
        learning_rate (float): The step size used for updating parameters during gradient descent.
        epochs (int): The number of iterations over the training data.
        weights (ndarray): The coefficients for the linear regression features.
        bias (float): The intercept term for the linear regression.
    """

    def __init__(self, learning_rate=0.01, epochs=1000):
        """Initializes the LinearRegression model.

        Args:
            learning_rate (float, optional): The step size for gradient descent. Defaults to 0.01.
            epochs (int, optional): The number of training iterations. Defaults to 1000.
        """
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        """Trains the linear regression model on the given data.

        Args:
            X (ndarray): Training data of shape (n_samples, n_features).
            y (ndarray): Target values of shape (n_samples,).
        """
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        for _ in range(self.epochs):
            y_pred = np.dot(X, self.weights) + self.bias

            dw = (1 / n_samples) * np.dot(X.T, (y_pred - y))
            db = (1 / n_samples) * np.sum(y_pred - y)

            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def predict(self, X):
        """Predicts target values for the given input data.

        Args:
            X (ndarray): Input data of shape (n_samples, n_features).

        Returns:
            ndarray: Predicted target values of shape (n_samples,).
        """
        return np.dot(X, self.weights) + self.bias