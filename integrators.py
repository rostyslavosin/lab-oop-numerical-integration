"""Модуль реалізації класів чисельного інтегрування."""


class BaseIntegrator:
    """Базовий клас для чисельного обчислення визначених інтегралів."""

    order = 1
    method_name = "Базовий метод"

    def __init__(self, func, a, b):
        """Ініціалізує підінтегральну функцію та межі інтегрування."""
        self.validate_bounds(a, b)
        self.func = func
        self.a = float(a)
        self.b = float(b)

    @classmethod
    def from_dict(cls, func, params):
        """Альтернативний конструктор для створення інтегратора зі словника."""
        return cls(func, params["a"], params["b"])

    @staticmethod
    def validate_bounds(a, b):
        """Перевіряє коректність меж інтегрування."""
        if a >=b:
            raise ValueError("Нижня межа a повинна бути меншою за верхню межу b.")

    def integrate(self, n):
        """Обчислює наближене значення інтеграла для n розбиттів."""
        raise NotImplementedError

    def adaptive_integrate(self, eps=1e-4, initial_n=2):
        """Знаходить інтеграл із заданою точністю eps за правилом Рунге."""
        if eps <= 0:
            raise ValueError("Точність eps повинна бути додатньою.")
        if initial_n < 2 or initial_n % 2 != 0:
            raise ValueError("Початкова кількість розбиттів initial_n повинна бути додатньою.")

        n = initial_n
        i_h = self.integrate(n)
        divisor = (2 ** self.order) - 1

        while True:
            n_next = n*2
            i_h2 = self.integrate(n_next)
            error = abs(i_h2 - i_h) / divisor

            if error < eps:
                refined_i = i_h2 + (i_h2 - i_h) / divisor
                return refined_i, n_next, error

            n = n_next
            i_h = i_h2

    def __str__(self):
        """Повертає рядкове представлення об'єкта інтегратора."""
        return (
            f"{self.method_name} на відрізку: [{self.a}, {self.b}]"
            f"(порядок точності: {self.order})"
        )


class RectangleIntegrator(BaseIntegrator):
    """Обчислення інтеграла складеною формулою середніх прямокутників."""

    order = 2
    method_name = "Формула прямокутників"

    def __init__(self, func, a, b):
        """Запускає інтегратор середніх прямокутників."""
        super().__init__(func, a, b)

    def integrate(self, n):
        """Обчислення інтеграла за формулою середніх прямокутників."""
        if n <= 0 or n % 2 != 0:
            raise ValueError("Кількість розбиттів n повинна бути додатньою та парною.")

        h = (self.b - self.a) / n
        total = sum(self.func(self.a + (i + 0.5) * h) for i in range(n))
        return h * total


class TrapezoidIntegrator(BaseIntegrator):
    """Обчислення інтеграла складеною формулою трапецій."""

    order = 2
    method_name = "Формула трапецій"

    def __init__(self, func, a, b):
        """Запускає інтегратор трапецій."""
        super().__init__(func, a, b)

    def integrate(self, n):
        """Обчислення інтеграла за формулою трапецій."""
        if n <= 0 or n % 2 != 0:
            raise ValueError("Кількість розбиттів n повинна бути додатньою та парною.")

        h = (self.b - self.a) / n
        endpoints = 0.5 * (self.func(self.a) + self.func(self.b))
        interior = sum(self.func(self.a + i * h) for i in range(1, n))
        return h * (endpoints + interior)


class SimpsonIntegrator(BaseIntegrator):
    """Обчислення інтеграла складеною формулою Сімпсона."""

    order = 4
    method_name = "Формула Сімпсона"

    def __init__(self, func, a, b):
        """Запускає інтегратор Сімпсона."""
        super().__init__(func, a, b)

    def integrate(self, n):
        """Обчислення інтеграла за формулою Сімпсона."""
        if n <= 0 or n % 2 != 0:
            raise ValueError("Кількість розбиттів n повинна бути додатньою та парною.")

        h = (self.b - self.a) / n
        odd_sum = sum(self.func(self.a + i*h) for i in range(1, n, 2))
        even_sum = sum(self.func(self.a + i*h) for i in range(2, n-1, 2))
        return (h/3) * (self.func(self.a) + self.func(self.b) + 4*odd_sum + 2*even_sum)
