from dataclasses import asdict, dataclass
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    INFO_OF_TRAINING: str = ('Тип тренировки: {training_type}; '
                             'Длительность: {duration:.3f} ч.; '
                             'Дистанция: {distance:.3f} км; '
                             'Ср. скорость: {speed:.3f} км/ч; '
                             'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.INFO_OF_TRAINING.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float

    MIN_IN_HOURS = 60
    M_IN_KM: int = 1000
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
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIES_1 = 18
    COEFF_CALORIES_2 = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_CALORIES_1
                * self.get_mean_speed()
                - self.COEFF_CALORIES_2)
                * self.weight
                / self.M_IN_KM
                * self.duration * self.MIN_IN_HOURS)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIES_1 = 0.035
    COEFF_CALORIES_2 = 0.029

    height: float

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.COEFF_CALORIES_1
                * self.weight
                + (self.get_mean_speed() ** 2
                 // self.height)
                * self.COEFF_CALORIES_2
                * self.weight)
                * (self.duration * self.MIN_IN_HOURS))


class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: int
    count_pool: int

    LEN_STEP: float = 1.38
    COEFF_CALORIES_1 = 1.1
    COEFF_CALORIES_2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed()
                + self.COEFF_CALORIES_1)
                * self.COEFF_CALORIES_2
                * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    workout_dict: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in workout_dict:
        raise ValueError('Тип тренировки отсутствует в словаре')
    return workout_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
