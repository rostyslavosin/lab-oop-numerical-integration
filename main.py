"""Головний модуль запуску чисельного інтегрування."""

import math

from integrators import (
    RectangleIntegrator,
    SimpsonIntegrator,
    TrapezoidIntegrator,
)


def target_function(x):
    """Підінтегральна функція згідно з індивідуальним варіантом."""
    return math.sin(x**4 + 2* x**3 + x**2)


def main():
    """Точка входу програми."""
    bounds = {"a": 0.0, "b": 1.0}
    epsilon = 0.0001

    integrators = [
        RectangleIntegrator.from_dict(target_function, bounds),
        TrapezoidIntegrator.from_dict(target_function, bounds),
        SimpsonIntegrator.from_dict(target_function, bounds),
    ]

    for eps in (epsilon, epsilon*0.1):
        print(f"===Точність похибки = {eps:.0e} ===")
        for integrator in integrators:
            print(integrator)
            result, n_min, err = integrator.adaptive_integrate(eps=eps)
            print(f"Уточнений результат: {result:.8f}")
            print(f"Мінімальна кількість розбиттів: {n_min}")
            print(f"Оцінка похибки: {err:.8e}")

if __name__ == "__main__":
    main()
