class OgrnValidator:
    """Класс для валидации ОГРН и ОГРНИП"""

    @staticmethod
    def _clean_ogrn(ogrn: str) -> str:
        """Удаление всех нецифровых символов из ОГРН/ОГРНИП"""
        return ''.join(filter(str.isdigit, str(ogrn)))

    @staticmethod
    def validate_ogrn(ogrn: str, logging: bool = False) -> bool:
        """
        Проверка валидности ОГРН

        :param ogrn: ОГРН для проверки
        :param logging: Вывод подробности проверки
        :return: True если ОГРН валиден, иначе False
        """
        clean_ogrn = OgrnValidator._clean_ogrn(ogrn)

        if logging:
            print(f"Проверка ОГРН: {ogrn}")
            print(f"Очищенный ОГРН: {clean_ogrn}")

        if len(clean_ogrn) != 13:
            if logging:
                print("Ошибка: ОГРН должен содержать 13 цифр")
            return False

        num = clean_ogrn[:-1]
        checksum = int(clean_ogrn[-1])
        calculated_checksum = int(num) % 11 % 10

        is_valid = checksum == calculated_checksum

        if logging:
            print(f"Контрольная цифра: {checksum}")
            print(f"Рассчитанная контрольная цифра: {calculated_checksum}")
            if is_valid:
                print("ОГРН валиден")
            else:
                print("Ошибка: неверная контрольная цифра")

        return is_valid

    @staticmethod
    def validate_ogrnip(ogrnip: str, logging: bool = False) -> bool:
        """
        Проверка валидности ОГРНИП

        :param ogrnip: ОГРНИП для проверки
        :param logging: Вывод подробности проверки
        :return: True если ОГРНИП валиден, иначе False
        """
        clean_ogrnip = OgrnValidator._clean_ogrn(ogrnip)

        if logging:
            print(f"Проверка ОГРНИП: {ogrnip}")
            print(f"Очищенный ОГРНИП: {clean_ogrnip}")

        if len(clean_ogrnip) != 15:
            if logging:
                print("Ошибка: ОГРНИП должен содержать 15 цифр")
            return False

        num = clean_ogrnip[:-1]
        checksum = int(clean_ogrnip[-1])
        calculated_checksum = int(num) % 13 % 10

        is_valid = checksum == calculated_checksum

        if logging:
            print(f"Контрольная цифра: {checksum}")
            print(f"Рассчитанная контрольная цифра: {calculated_checksum}")
            if is_valid:
                print("ОГРНИП валиден")
            else:
                print("Ошибка: неверная контрольная цифра")

        return is_valid

    @classmethod
    def validate(cls, number: str, logging: bool = False) -> bool:
        """
        Проверка валидности ОГРН/ОГРНИП

        :param number: ОГРН или ОГРНИП для проверки
        :param logging: Вывод подробности проверки
        :return: True если номер валиден, иначе False
        """
        clean_number = cls._clean_ogrn(number)

        if len(clean_number) == 13:
            return cls.validate_ogrn(number, logging)
        elif len(clean_number) == 15:
            return cls.validate_ogrnip(number, logging)
        else:
            if logging:
                print("Ошибка: номер должен содержать 13 (ОГРН) или 15 (ОГРНИП) цифр")
            return False