import numpy as np


class SimplexMethod:
    """
    Реализация симплекс-метода для решения задач линейного программирования.

    Класс предоставляет улучшенную реализацию симплекс-метода с обработкой
    линейно зависимых ограничений и использованием правила Бланда для предотвращения
    зацикливания.

    Attributes:
        c (numpy.ndarray): Вектор коэффициентов целевой функции (размер n).
        A (numpy.ndarray): Матрица ограничений (размер m x n).
        b (numpy.ndarray): Вектор правых частей ограничений (размер m).

    Args:
        c (list or numpy.ndarray): Коэффициенты целевой функции.
        A (list or numpy.ndarray): Матрица коэффициентов ограничений.
        b (list or numpy.ndarray): Правые части ограничений.

    Raises:
        ValueError: Если размерности входных данных не согласованы.
    """

    def __init__(self, c, A, b):
        """
        Инициализирует экземпляр класса SimplexMethod.

        Преобразует входные данные в numpy массивы и проверяет их согласованность.
        """
        self.c = np.array(c, dtype=float)
        self.A = np.array(A, dtype=float)
        self.b = np.array(b, dtype=float)

        # Проверка размерностей
        if len(self.A.shape) != 2:
            raise ValueError("A must be a 2D array")
        if len(self.b.shape) != 1:
            raise ValueError("b must be a 1D array")
        if len(self.c.shape) != 1:
            raise ValueError("c must be a 1D array")
        if self.A.shape[0] != self.b.shape[0]:
            raise ValueError("Number of rows in A must match length of b")
        if self.A.shape[1] != self.c.shape[0]:
            raise ValueError("Number of columns in A must match length of c")

    def solve(self):
        """
        Решает задачу линейного программирования симплекс-методом.

        Returns:
            dict: Словарь с результатами решения, содержащий:
                - 'success' (bool): Флаг успешности решения
                - 'message' (str): Сообщение о результате
                - 'x' (numpy.ndarray or None): Вектор решения (если успешно)
                - 'value' (float or None): Значение целевой функции (если успешно)

        Процесс решения включает следующие шаги:
        1. Удаление линейно зависимых ограничений
        2. Добавление slack-переменных для приведения к стандартной форме
        3. Построение начальной симплекс-таблицы
        4. Итеративное выполнение симплекс-метода с правилом Бланда
        5. Извлечение решения из финальной симплекс-таблицы

        Raises:
            ValueError: Если задача неограничена или достигнуто максимальное число итераций.
        """
        m, n = self.A.shape

        # Удаляем линейно зависимые ограничения
        A_clean, b_clean = self._remove_redundant_constraints()
        m_clean = A_clean.shape[0]

        # Добавляем slack переменные
        c_simplex = np.hstack([self.c, np.zeros(m_clean)])
        A_simplex = np.hstack([A_clean, np.eye(m_clean)])
        basis = list(range(n, n + m_clean))  # Начальный базис

        # Формируем симплекс-таблицу
        tableau = np.vstack([
            np.hstack([A_simplex, b_clean.reshape(-1, 1)]),
            np.hstack([-c_simplex, 0])
        ])

        max_iterations = 1000
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            objective_row = tableau[-1, :-1]
            if all(objective_row >= -1e-10):
                break

            # Правило Бланда для выбора входящей переменной
            entering = None
            for j in range(len(objective_row)):
                if objective_row[j] < -1e-10:
                    entering = j
                    break

            if entering is None:
                break

            # Вычисляем отношения с учетом численной стабильности
            ratios = np.full(m_clean, np.inf)
            for i in range(m_clean):
                if tableau[i, entering] > 1e-10:
                    ratios[i] = tableau[i, -1] / tableau[i, entering]

            if all(np.isinf(ratios)):
                return {
                    'success': False,
                    'message': 'Problem is unbounded',
                    'x': None,
                    'value': None
                }

            # Выбираем исключаемую переменную по правилу Бланда
            min_ratio = np.min(ratios)
            leaving_candidates = np.where(np.abs(ratios - min_ratio) < 1e-10)[0]
            leaving_pos = min(leaving_candidates)
            leaving = basis[leaving_pos]

            basis[leaving_pos] = entering

            # Нормализуем ведущую строку
            pivot = tableau[leaving_pos, entering]
            tableau[leaving_pos, :] /= pivot

            # Исключаем ведущую переменную из других уравнений
            for i in range(m_clean + 1):
                if i != leaving_pos:
                    tableau[i, :] -= tableau[i, entering] * tableau[leaving_pos, :]

        if iteration >= max_iterations:
            return {
                'success': False,
                'message': 'Maximum iterations reached',
                'x': None,
                'value': None
            }

        x = np.zeros(n + m_clean)
        for i in range(m_clean):
            if basis[i] < n:
                x[basis[i]] = tableau[i, -1]

        solution = x[:n]
        value = tableau[-1, -1]

        return {
            'success': True,
            'message': 'Optimal solution found',
            'x': solution,
            'value': value
        }

    def _remove_redundant_constraints(self):
        """
        Удаляет линейно зависимые ограничения из системы.

        Метод использует метод Гаусса для приведения матрицы ограничений к ступенчатому виду
        и идентификации линейно зависимых строк.

        Returns:
            tuple: Кортеж из двух элементов:
                - A_clean (numpy.ndarray): Очищенная матрица ограничений
                - b_clean (numpy.ndarray): Соответствующий вектор правых частей

        Note:
            Метод является внутренним (private) и не предназначен для прямого вызова.
            Он автоматически вызывается методом solve() перед началом решения.
        """
        A = self.A.copy()
        b = self.b.copy()
        m, n = A.shape

        # Приводим матрицу к ступенчатому виду
        for i in range(min(m, n)):
            # Ищем строку с максимальным элементом в текущем столбце
            max_row = i
            for k in range(i + 1, m):
                if abs(A[k, i]) > abs(A[max_row, i]):
                    max_row = k

            A[[i, max_row]] = A[[max_row, i]]
            b[[i, max_row]] = b[[max_row, i]]

            # Если ведущий элемент почти нулевой, пропускаем столбец
            if abs(A[i, i]) < 1e-10:
                continue

            # Обнуляем элементы ниже ведущего
            for k in range(i + 1, m):
                factor = A[k, i] / A[i, i]
                A[k, i:] -= factor * A[i, i:]
                b[k] -= factor * b[i]

        # Определяем ненулевые строки
        non_zero_rows = []
        for i in range(m):
            if not all(np.abs(A[i]) < 1e-10):
                non_zero_rows.append(i)

        return A[non_zero_rows], b[non_zero_rows]