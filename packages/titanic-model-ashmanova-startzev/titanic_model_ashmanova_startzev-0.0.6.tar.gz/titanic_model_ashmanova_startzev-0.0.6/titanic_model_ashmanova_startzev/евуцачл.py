import pandas as pd
import numpy as np

from titanic_model_ashmanova_startzev.predict import make_prediction



# Вариант 3: Тестирование с одним пассажиром
single_passenger = {
    "PassengerId": [6],
    "Pclass": [1],
    "Name": ["Alice Wilson"],
    "Sex": ["female"],
    "Age": [30.0],
    "SibSp": [1],
    "Parch": [0],
    "Ticket": ["113803"],
    "Fare": [53.10],
    "Cabin": ["C123"],
    "Embarked": ["S"]
}
result_single = make_prediction(input_data=single_passenger)
print("\nResults for single passenger:")
print(result_single)