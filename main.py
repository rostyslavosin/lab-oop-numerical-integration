"""Головний модуль запуску чисельного інтегрування."""

import math

from integrators import (
    RectangleIntegrator,
    SimpsonIntegrator,
    TrapezoidIntegrator,
)


def target_function(x):
    """Підінтегральна функція згідно з індивідуальним варіантом."""
    if x == 0:
        return -0.5
    return (math.cos(x) - 1)/x**2


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
            print(
                f"  Уточнений результат: {result:.7f} "
                f"(n_min = {n_min}, похибка ≈ {err:.2e})\n"
            )

if __name__ == "__main__":
    main()
