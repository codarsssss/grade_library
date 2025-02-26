import re
from rest_framework import serializers


class ISBNValidator:
    ISBN_PATTERN = r"^(97[89])?\d{9}[\dX]$"

    @classmethod
    def validate_isbn(cls, value):
        """Валидация ISBN: регулярное выражение + контрольная сумма"""
        if not re.match(cls.ISBN_PATTERN, value):
            raise serializers.ValidationError("Некорректный формат ISBN")

        if len(value) == 10:
            if not ISBNValidator.check_isbn10(value):
                raise serializers.ValidationError("Некорректный ISBN-10 (ошибка контрольной суммы)")
        elif len(value) == 13:
            if not ISBNValidator.check_isbn13(value):
                raise serializers.ValidationError("Некорректный ISBN-13 (ошибка контрольной суммы)")
        else:
            raise serializers.ValidationError("ISBN должен содержать 10 или 13 символов")

        return value

    @staticmethod
    def check_isbn10(isbn):
        """Проверка контрольной суммы для ISBN-10"""
        total = 0
        for i, digit in enumerate(isbn[:9]):
            total += (i + 1) * int(digit)
        check_digit = total % 11
        return str(check_digit) if check_digit != 10 else "X" == isbn[-1]

    @staticmethod
    def check_isbn13(isbn):
        """Проверка контрольной суммы для ISBN-13"""
        total = sum((1 if i % 2 == 0 else 3) * int(digit) for i, digit in enumerate(isbn[:12]))
        check_digit = (10 - (total % 10)) % 10
        return str(check_digit) == isbn[-1]
