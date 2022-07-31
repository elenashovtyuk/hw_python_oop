from typing import Dict


class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type};'
                f'Длительность: {self.duration:.3f} ч.;'
                f'Дистанция: {self.distance:.3f} км.;'
                f'Ср. скорость: {self.speed:.3f} км/ч;'
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    M_IN_KM: float = 1000
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight


    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        dist_m = self.action * self.LEN_STEP / self.M_IN_KM
        return dist_m

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        main_speed = self.get_distance() / self.duration
        return main_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass
        
    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(self.training_type,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories()
                              )


class Running(Training):
    """Тренировка: бег."""
    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    # def get_distance(self) -> float:
    #     """Получить дистанцию в км."""
    #     dist_m = self.action * self.LEN_STEP / self.M_IN_KM
    #     return dist_m
    #
    # def get_mean_speed(self) -> float:
    #     """Получить среднюю скорость движения."""
    #     main_speed = self.get_distance() / self.duration
    #     return main_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calories_1: float = 18
        coeff_calories_2: float = 20
        spent_calories = (coeff_calories_1 * self.get_mean_speed() - coeff_calories_2) * self.weight / self.M_IN_KM * self.duration
        return spent_calories

    # def show_training_info(self) -> InfoMessage:
    #     """Вернуть информационное сообщение о выполненной тренировке."""
    #     pass


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float

    def __init__(self, action: int, duration: float, weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    # def get_distance(self) -> float:
    #     """Получить дистанцию в км."""
    #     dist_m = self.action * self.LEN_STEP / self.M_IN_KM
    #     return dist_m
    #
    # def get_mean_speed(self) -> float:
    #     """Получить среднюю скорость движения."""
    #     main_speed = self.get_distance() / self.duration
    #     return main_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calories_1: float = 0.035
        coeff_calories_2: float = 0.029
        spent_calories = (coeff_calories_1 * self.weight + (self.get_mean_speed() ** 2 // self.height) * coeff_calories_2 * self.weight) * self.duration
        return spent_calories

    # def show_training_info(self) -> InfoMessage:
    #     """Вернуть информационное сообщение о выполненной тренировке."""
    #     pass

class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: float
    LEN_STEP: float = 1.38

    def __init__(self, action: int, duration: float, weight: float, length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool
        self.count_pool = count_pool

    # def get_distance(self) -> float:
    #     """Получить дистанцию в км."""
    #     dist_m = self.action * self.LEN_STEP / self.M_IN_KM
    #     return dist_m
    #
    # def get_mean_speed(self) -> float:
    #     """Получить среднюю скорость движения."""
    #     main_speed = self.lenght_pool * self.count_pool / self.M_IN_KM / self.duration
    #     return main_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calories_1: float = 1.1
        coeff_calories_2: float = 2
        spent_calories = (self.get_mean_speed() + coeff_calories_1) * coeff_calories_2 * self.weight
        return spent_calories
        
    
def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_dict: Dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return 
    pass


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())
    
    pass

if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

