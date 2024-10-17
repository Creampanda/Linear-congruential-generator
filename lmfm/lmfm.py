import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error
from math import sqrt
import sys



def read_data(file_path):
    """
    Чтение данных из текстового файла.
    Предполагается, что первый столбец — отклик y,
    а остальные — факторы X1, X2, ..., Xn.
    """
    try:
        data = pd.read_csv(
            file_path, sep=None, engine="python"
        )  # Автоматическое определение разделителя
        return data
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        sys.exit(1)


def estimate_parameters(X, y):
    """
    Оценка параметров модели с помощью МНК.
    """
    X = sm.add_constant(X)  # Добавление свободного члена
    model = sm.OLS(y, X).fit()
    return model


def select_significant_factors(model, significance_level):
    """
    Отбор значимых факторов по статистической значимости.
    Возвращает список значимых факторов.
    """
    p_values = model.pvalues
    significant = p_values[p_values < significance_level].index.tolist()
    if "const" in significant:
        significant.remove("const")
    return significant


def check_multicollinearity(X, threshold=0.8):
    """
    Проверка мультиколлинеарности между факторами.
    Возвращает пары факторов с коэффициентом корреляции выше порога.
    """
    corr_matrix = X.corr().abs()
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    high_corr = [
        (column, row)
        for column in upper.columns
        for row in upper.index
        if upper.loc[row, column] > threshold
    ]
    return high_corr


def evaluate_model_adadequacy(model, X, y):
    """
    Оценка адекватности модели.
    Возвращает информацию о R^2, F-статистике и RMSE.
    """
    r_squared = model.rsquared
    f_stat = model.fvalue
    f_pvalue = model.f_pvalue
    predictions = model.predict(X)
    rmse = sqrt(mean_squared_error(y, predictions))
    return r_squared, f_stat, f_pvalue, rmse


def special_metrics(y, predictions):
    """
    Вычисление специальных показателей.
    Здесь можно добавить любые дополнительные метрики.
    """
    relative_error = np.mean(np.abs((y - predictions) / y))
    return relative_error


def predict_new(model, new_data_path):
    """
    Предсказание новых значений отклика на основе введённых факторов.
    """
    try:
        new_data = pd.read_csv(new_data_path, sep=None, engine="python")
        X_new = sm.add_constant(new_data)
        predictions = model.predict(X_new)
        return predictions
    except Exception as e:
        print(f"Ошибка при чтении файла с новыми данными: {e}")
        sys.exit(1)


def main():

    # Пути к файлам (можно заменить на ввод пользователя)
    data_file = "data.csv"  # Входные данные: первый столбец y, остальные X
    new_data_file = "new_data.csv"  # Новые факторы для предсказания
    output_file = "output.txt"  # Файл для сохранения результатов

    # Чтение данных
    data = read_data(data_file)
    y = data.iloc[:, 0]
    X = data.iloc[:, 1:]

    # Ввод уровня значимости
    try:
        significance_level = float(
            input("Введите уровень значимости (например, 0.05): ")
        )
    except ValueError:
        print("Некорректный ввод. Используется уровень значимости 0.05.")
        significance_level = 0.05

    # Оценка параметров модели
    model = estimate_parameters(X, y)
    print("Параметры модели:\n", model.summary())

    # Отбор значимых факторов
    significant_factors = select_significant_factors(model, significance_level)
    print(f"Значимые факторы (p < {significance_level}): {significant_factors}")

    # Проверка мультиколлинеарности
    if significant_factors:
        high_corr = check_multicollinearity(X[significant_factors])
        if high_corr:
            print("Факторы с высокой корреляцией между собой:")
            for pair in high_corr:
                print(f"{pair[0]} и {pair[1]}")
        else:
            print("Мультиколлинеарности между факторами не обнаружено.")
    else:
        print("Нет значимых факторов для проверки мультиколлинеарности.")

    # Оценка адекватности модели
    X_with_const = sm.add_constant(X)
    r2, f_stat, f_pval, rmse = evaluate_model_adadequacy(model, X_with_const, y)
    print(f"Коэффициент детерминации R^2: {r2}")
    print(f"F-статистика: {f_stat}, p-значение: {f_pval}")
    print(f"RMSE: {rmse}")

    if f_pval < significance_level:
        print("Модель адекватна.")
    else:
        print("Модель неадекватна.")

    # Вычисление специальных показателей
    predictions = model.predict(X_with_const)
    rel_error = special_metrics(y, predictions)
    print(f"Относительная ошибка: {rel_error}")

    # Предсказание на новых данных
    user_choice = (
        input("Хотите выполнить предсказание на новых данных? (да/нет): ")
        .strip()
        .lower()
    )
    if user_choice == "да":
        predictions_new = predict_new(model, new_data_file)
        print("Предсказанные значения для новых данных:")
        print(predictions_new)
    else:
        print("Предсказание не выполнено.")

    # Сохранение результатов в файл
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("Параметры модели:\n")
        f.write(model.summary().as_text())
        f.write("\nЗначимые факторы:\n")
        f.write(
            ", ".join(significant_factors)
            if significant_factors
            else "Нет значимых факторов."
        )
        f.write("\nМультиколлинеарность:\n")
        if significant_factors and high_corr:
            for pair in high_corr:
                f.write(f"{pair[0]} и {pair[1]}\n")
        elif significant_factors:
            f.write("Мультиколлинеарность не обнаружена.\n")
        else:
            f.write("Нет значимых факторов для проверки мультиколлинеарности.\n")
        f.write(f"\nКоэффициент детерминации R^2: {r2}\n")
        f.write(f"F-статистика: {f_stat}, p-значение: {f_pval}\n")
        f.write(f"RMSE: {rmse}\n")
        f.write(f"Относительная ошибка: {rel_error}\n")
        if user_choice == "да":
            f.write("\nПредсказанные значения для новых данных:\n")
            f.write(predictions_new.to_string())
    print(f"Результаты сохранены в файл '{output_file}'.")


if __name__ == "__main__":
    main()
