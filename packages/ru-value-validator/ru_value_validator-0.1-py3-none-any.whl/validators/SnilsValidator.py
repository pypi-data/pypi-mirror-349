import re

class SnilsValidator:
    """Класс для валидации СНИЛС"""

    @staticmethod
    def _clean_snils(snils: str) -> str:
        """Удаление всех нецифровых символов из СНИЛС"""
        return re.sub(r'[^\d]', '', snils)

    @staticmethod
    def _validate_checksum(clean_snils: str) -> bool:
        """Проверка контрольной суммы СНИЛС"""

        if len(clean_snils) != 11:
            return False

        number = clean_snils[:9]
        checksum = int(clean_snils[-2:])

        total = 0
        for i in range(9):
            digit = int(number[i])
            total += digit * (9 - i)

        calculated_checksum = total % 101
        if calculated_checksum == 100:
            calculated_checksum = 0

        return checksum == calculated_checksum

    @classmethod
    def validate(cls, snils: str, logging: bool = False) -> bool:
        """
        Проверка валидности СНИЛС

        :param snils: СНИЛС для проверки (может быть с разделителями или без)
        :param logging: Вывод подробности проверки
        :return: True если СНИЛС валиден, иначе False
        """
        if not isinstance(snils, str):
            if logging:
                print("Ошибка: СНИЛС должен быть строкой")
            return False

        clean_snils = cls._clean_snils(snils)

        if logging:
            print(f"Очищенный СНИЛС: {clean_snils}")

        if len(clean_snils) != 11:
            if logging:
                print("Ошибка: СНИЛС должен содержать 11 цифр")
            return False

        is_valid = cls._validate_checksum(clean_snils)

        if logging:
            if is_valid:
                print("СНИЛС валиден")
            else:
                print("Ошибка: неверная контрольная сумма")

        return is_valid