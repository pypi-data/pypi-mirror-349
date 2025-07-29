import numpy as np

class LogisticRegressionRidge:
    def __init__(self, learning_rate=0.01, lambda_=0.1, epochs=1000, fit_intercept=True, verbose=False):
        """
        Параметры:
        -----------
        learning_rate : float, default=0.01
            Скорость обучения для градиентного спуска.
        lambda_ : float, default=0.1
            Коэффициент L2-регуляризации (чем больше, тем сильнее штраф на веса).
        epochs : int, default=1000
            Количество итераций градиентного спуска.
        fit_intercept : bool, default=True
            Добавлять ли свободный член (bias) в модель.
        verbose : bool, default=False
            Выводить ли процесс обучения (потери на каждой 100-й эпохе).
        """
        self.learning_rate = learning_rate
        self.lambda_ = lambda_
        self.epochs = epochs
        self.fit_intercept = fit_intercept
        self.verbose = verbose
        self.weights = None
        self.loss_history = []

    def _add_intercept(self, X):
        """Добавляет столбец единиц для свободного члена (bias)."""
        intercept = np.ones((X.shape[0], 1))
        return np.hstack((intercept, X))

    def _sigmoid(self, z):
        """Сигмоидная функция активации."""
        return 1 / (1 + np.exp(-z))

    def _compute_loss(self, X, y):
        """Вычисляет функцию потерь (Log Loss + L2-регуляризация)."""
        z = np.dot(X, self.weights)
        predictions = self._sigmoid(z)

        # Основная часть лосса (Log Loss)
        loss = -np.mean(y * np.log(predictions + 1e-9) + (1 - y) * np.log(1 - predictions + 1e-9))

        # L2-регуляризация (исключаем bias term w0)
        l2_penalty = (self.lambda_ / 2) * np.sum(self.weights[1:] ** 2)

        return loss + l2_penalty

    def fit(self, X, y):
        """
        Обучает модель логистической регрессии.

        Параметры:
        ----------
        X : ndarray, shape (n_samples, n_features)
            Матрица признаков.
        y : ndarray, shape (n_samples,)
            Вектор целевых значений (0 или 1).
        """
        if self.fit_intercept:
            X = self._add_intercept(X)

        best_loss = float('inf')
        no_improvement = 0

        # Инициализация весов
        self.weights = np.zeros(X.shape[1])

        # Градиентный спуск
        for epoch in range(self.epochs):
            # Прямое распространение
            z = np.dot(X, self.weights)
            predictions = self._sigmoid(z)

            # Обратное распространение (градиент)
            error = predictions - y
            gradient = np.dot(X.T, error) / len(y)

            # Добавляем L2-регуляризацию (кроме bias term w0)
            gradient[1:] += (self.lambda_ / len(y)) * self.weights[1:]

            # Обновляем веса
            self.weights -= self.learning_rate * gradient

            # Сохраняем лосс для истории
            loss = self._compute_loss(X, y)
            self.loss_history.append(loss)

            # Логирование (если verbose=True)
            if self.verbose and (epoch % 100 == 0 or epoch == self.epochs - 1):
                print(f"Epoch {epoch}, Loss: {loss:.4f}")

            if loss < best_loss - 1e-4:  # Порог улучшения
                best_loss = loss
                no_improvement = 0
            else:
                no_improvement += 1
                if no_improvement == 100:
                    break

    def predict_proba(self, X):
        """
        Возвращает вероятности принадлежности к классу 1.

        Параметры:
        ----------
        X : ndarray, shape (n_samples, n_features)
            Матрица признаков.

        Возвращает:
        -----------
        ndarray, shape (n_samples,)
            Вероятности P(y=1|X).
        """
        if self.fit_intercept:
            X = self._add_intercept(X)
        return self._sigmoid(np.dot(X, self.weights))

    def predict(self, X, threshold=0.5):
        """
        Возвращает предсказанные классы (0 или 1).

        Параметры:
        ----------
        X : ndarray, shape (n_samples, n_features)
            Матрица признаков.
        threshold : float, default=0.5
            Порог классификации.

        Возвращает:
        -----------
        ndarray, shape (n_samples,)
            Предсказанные классы.
        """
        return (self.predict_proba(X) >= threshold).astype(int)

    def get_weights(self):
        return self.weights

