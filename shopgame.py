import random
import math

Account = 10000
BasicStore = 80
ShopStore = 0
TIME = 0  # Предположим, что TIME – это количество дней или ходов
TransferRate = 150
OptOfferBaseVolume = 40
Max_Demand = 30
MeanDPrice = 100
RentRate = 200
WagesAndTaxes = 500
BasicOptOfferVol = 50
BasicOptOfferPrice = 35

while Account > 0:
    TIME += 1
    print(f"\n--- День {TIME} ---")
    # Выводим данные
    print(f"Состояние расчетного счета: {Account}")
    print(f"Базовый склад (BasicStore): {BasicStore}")
    print(f"Склад магазина (ShopStore): {ShopStore}")
    # Мелкооптовое предложение
    BasicPriceRnd = BasicOptOfferVol * random.uniform(0.7, 1.3)
    AddPriceByTime = (
        BasicOptOfferPrice * 0.03 * TIME
        + BasicOptOfferPrice * 0.01 * TIME * random.uniform(0, 1)
    )
    OfferOnePrice = AddPriceByTime + BasicPriceRnd
    RndOfferVolume = round(OptOfferBaseVolume * random.uniform(0.75, 1.25))
    print(
        f"Мелкооптовое предложение: объем партии {RndOfferVolume}, цена за единицу {OfferOnePrice:.2f}"
    )
    # Расходы
    total_expenses = RentRate + WagesAndTaxes
    print(f"Расходы (аренда и зарплаты): {total_expenses}")

    # Предлагаем пользователю ввести свои данные
    try:
        TransferVol = float(input("Введите объем переноса товара (TransferVol): "))
        TransferDecision_input = input(
            "Принять решение о переносе товара? (TransferDecision) (1 - Да, 0 - Нет): "
        )
        TransferDecision = bool(int(TransferDecision_input))
        OptOfferAcceptDecision_input = input(
            "Принять мелкооптовое предложение? (OptOfferAcceptDecision) (1 - Да, 0 - Нет): "
        )
        OptOfferAcceptDecision = bool(int(OptOfferAcceptDecision_input))
        Ad_Spend = float(input("Введите расходы на рекламу (Ad_Spend): "))
        Ret_Price = float(input("Введите розничную цену (Ret_Price): "))
        STOP_SELL_input = input("Остановить продажи? (STOP_SELL) (1 - Да, 0 - Нет): ")
        STOP_SELL = bool(int(STOP_SELL_input))
    except ValueError:
        print("Неверный ввод. Пожалуйста, введите числовые значения.")
        continue

    # Расчеты
    BasicPriceRnd = BasicOptOfferVol * random.uniform(0.7, 1.3)
    AddPriceByTime = (
        BasicOptOfferPrice * 0.03 * TIME
        + BasicOptOfferPrice * 0.01 * TIME * random.uniform(0, 1)
    )
    OfferOnePrice = AddPriceByTime + BasicPriceRnd

    # TransferActualVol
    if Account >= TransferRate:
        TransferActualVol = min(BasicStore, TransferVol * TransferDecision)
    else:
        TransferActualVol = 0

    # RndOfferVolume
    RndOfferVolume = round(OptOfferBaseVolume * random.uniform(0.75, 1.25))

    # OfferFullPrice
    OfferFullPrice = OfferOnePrice * RndOfferVolume

    # OfferAcceptPossibility
    if Account >= OfferFullPrice:
        OfferAcceptPossibility = 1
    else:
        OfferAcceptPossibility = 0

    # SmallOptIncom
    SmallOptIncom = OfferAcceptPossibility * OptOfferAcceptDecision * RndOfferVolume

    # Ad_Effectiveness
    Ad_Effectiveness = random.uniform(0, 1)

    # Ad_Effect
    Ad_Effect = Ad_Effectiveness * Ad_Spend

    # Demand
    Demand = round(
        Max_Demand
        * (1 - 1 / (1 + math.exp(-0.05 * (Ret_Price - MeanDPrice))))
        * (1 + Ad_Effect / 100)
    )

    # RND_Demand
    RND_Demand = round(Demand * random.uniform(0.7, 1.2))

    # SoldRet
    if STOP_SELL:
        SoldRet = 0
    else:
        SoldRet = min(RND_Demand, ShopStore)

    # GoodsTransfer
    GoodsTransfer = math.trunc(TransferActualVol)

    # Обновление BasicStore
    BasicStore += SmallOptIncom
    BasicStore -= GoodsTransfer

    # Обновление ShopStore
    ShopStore += GoodsTransfer
    ShopStore -= SoldRet

    # Selling
    Selling = SoldRet

    # Sp_Opt_Value
    if OfferAcceptPossibility * OptOfferAcceptDecision > 0:
        Sp_Opt_Value = OfferFullPrice
    else:
        Sp_Opt_Value = 0

    # Income
    Income = Ret_Price * SoldRet

    # Обновление Account
    Account += Income

    # TransSpend
    if TransferActualVol > 0:
        TransSpend = TransferRate
    else:
        TransSpend = 0

    # DailySpending
    DailySpending = min(RentRate + WagesAndTaxes + Ad_Spend, Account)
    Spend_for_Offer = Sp_Opt_Value

    # Обновление Account
    Account -= TransSpend + DailySpending + Spend_for_Offer

    # Вывод результатов
    print(f"Состояние расчетного счета после операций: {Account}")
    print(f"Состояние базового склада: {BasicStore}")
    print(f"Состояние склада магазина: {ShopStore}")
    total_expenses = TransSpend + DailySpending + Spend_for_Offer
    print(f"Общие расходы за день: {total_expenses}")
    print(f"Доход от продаж: {Income}")

    # Проверка баланса счета
    if Account <= 0:
        print("Баланс счета исчерпан. Симуляция завершена.")
        break
