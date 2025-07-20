import re
import logging
from rest_framework import serializers

logger = logging.getLogger("library")


class ISBNValidator:
    ISBN_PATTERN = r"^(97[89])?\d{9}[\dX]$"

    @classmethod
    def validate_isbn(cls, value):
        """Валидация ISBN: регулярка + контрольная сумма"""
        logger.debug(f"Проверка ISBN: {value}")

        if not re.match(cls.ISBN_PATTERN, value):
            logger.warning(f"Неверный формат ISBN: {value}")
            raise serializers.ValidationError("Некорректный формат ISBN")

        if len(value) == 10:
            if not ISBNValidator.check_isbn10(value):
                logger.warning(f"Неверная контрольная сумма для ISBN-10: {value}")
                raise serializers.ValidationError(
                    "Некорректный ISBN-10 (ошибка контрольной суммы)"
                )
        elif len(value) == 13:
            if not ISBNValidator.check_isbn13(value):
                logger.warning(f"Неверная контрольная сумма для ISBN-13: {value}")
                raise serializers.ValidationError(
                    "Некорректный ISBN-13 (ошибка контрольной суммы)"
                )
        else:
            logger.warning(f"Недопустимая длина ISBN: {value}")
            raise serializers.ValidationError("ISBN должен содержать 10 или 13 символов")

        logger.debug(f"ISBN прошел валидацию: {value}")
        return value

    @staticmethod
    def check_isbn10(isbn):
        """Контрольная сумма ISBN-10"""
        total = 0
        for i, digit in enumerate(isbn[:9]):
            total += (i + 1) * int(digit)
        check_digit = total % 11
        result = str(check_digit) if check_digit != 10 else "X"
        return result == isbn[-1]

    @staticmethod
    def check_isbn13(isbn):
        """Контрольная сумма ISBN-13"""
        total = sum(
            (1 if i % 2 == 0 else 3) * int(digit)
            for i, digit in enumerate(isbn[:12])
        )
        check_digit = (10 - (total % 10)) % 10
        return str(check_digit) == isbn[-1]
