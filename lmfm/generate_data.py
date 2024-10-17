import pandas as pd
import numpy as np


import argparse


def generate_data(
    n_samples=100,
    n_factors=3,
    coefficients=None,
    noise_level=1.0,
    output_file="data.csv",
    new_data_file="new_data.csv",
    n_new_samples=10,
    random_state=None,
):
    """
    Генерация синтетических данных для линейной многофакторной модели.

    Параметры:
    - n_samples (int): Количество наблюдений.
    - n_factors (int): Количество факторов.
    - coefficients (list или array): Коэффициенты для факторов. Длина должна быть равна n_factors.
                                       Если None, коэффициенты генерируются случайно.
    - noise_level (float): Стандартное отклонение шума.
    - output_file (str): Имя выходного файла для исходных данных.
    - new_data_file (str): Имя выходного файла для новых данных.
    - n_new_samples (int): Количество новых наблюдений для предсказания.
    - random_state (int или None): Сид для генератора случайных чисел для воспроизводимости.

    Возвращает:
    - None
    """
    if random_state is not None:
        np.random.seed(random_state)

    # Генерация коэффициентов, если они не заданы
    if coefficients is None:
        coefficients = np.random.uniform(1, 10, size=n_factors)
    else:
        coefficients = np.array(coefficients)
        if len(coefficients) != n_factors:
            raise ValueError("Длина списка коэффициентов должна совпадать с n_factors.")

    # Генерация факторов X
    X = np.random.uniform(0, 10, size=(n_samples, n_factors))
    X_df = pd.DataFrame(X, columns=[f"X{i+1}" for i in range(n_factors)])

    # Генерация отклика y
    y = X @ coefficients + np.random.normal(0, noise_level, size=n_samples)
    data = pd.concat([pd.Series(y, name="y"), X_df], axis=1)

    # Сохранение исходных данных
    data.to_csv(output_file, index=False)
    print(f"Исходные данные сохранены в файл '{output_file}'.")

    # Генерация новых данных для предсказания
    X_new = np.random.uniform(0, 10, size=(n_new_samples, n_factors))
    X_new_df = pd.DataFrame(X_new, columns=[f"X{i+1}" for i in range(n_factors)])
    X_new_df.to_csv(new_data_file, index=False)
    print(f"Новые данные для предсказания сохранены в файл '{new_data_file}'.")

    # Дополнительно: вывод коэффициентов для справки
    print("Использованные коэффициенты модели:")
    for i, coef in enumerate(coefficients, start=1):
        print(f"X{i}: {coef:.4f}")
    print(f"Уровень шума (стд. отклонение): {noise_level}")


def main():
    parser = argparse.ArgumentParser(
        description="Линейная Многофакторная Модель (ЛМФМ)"
    )
    parser.add_argument(
        "--generate", action="store_true", help="Сгенерировать синтетические данные."
    )
    parser.add_argument(
        "--n_samples",
        type=int,
        default=100,
        help="Количество наблюдений для исходных данных.",
    )
    parser.add_argument("--n_factors", type=int, default=3, help="Количество факторов.")
    parser.add_argument(
        "--coefficients", type=float, nargs="+", help="Коэффициенты для факторов."
    )
    parser.add_argument("--noise_level", type=float, default=1.0, help="Уровень шума.")
    parser.add_argument(
        "--output_file",
        type=str,
        default="data.csv",
        help="Имя файла для исходных данных.",
    )
    parser.add_argument(
        "--new_data_file",
        type=str,
        default="new_data.csv",
        help="Имя файла для новых данных.",
    )
    parser.add_argument(
        "--n_new_samples",
        type=int,
        default=10,
        help="Количество новых наблюдений для предсказания.",
    )
    parser.add_argument(
        "--random_state",
        type=int,
        default=None,
        help="Сид для генератора случайных чисел.",
    )

    args = parser.parse_args()

    if args.generate:
        generate_data(
            n_samples=args.n_samples,
            n_factors=args.n_factors,
            coefficients=args.coefficients,
            noise_level=args.noise_level,
            output_file=args.output_file,
            new_data_file=args.new_data_file,
            n_new_samples=args.n_new_samples,
            random_state=args.random_state,
        )
        return


if __name__ == "__main__":
    main()
