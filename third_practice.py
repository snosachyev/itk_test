"""Напиcать параметризованный декоратор @retry(max_attempts=3, delay=1)"""
import time

from functools import wraps


def retry(max_attempts=3, delay=1):
    """Декоратор перехватывает любые исключения (Exception)."""
    def decorator_retry(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = max_attempts

            while attempts > 0:
                try:
                    # Возвращаем результат, если функция выполнилась успешно
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts -= 1
                    # Если попыток больше не осталось, пробросить последнее исключение дальше
                    if attempts == 0:
                        raise e

                    print(f"Ошибка! Осталось попыток: {attempts}. Ждем {delay} сек...")
                    time.sleep(delay)
        return wrapper
    return decorator_retry

@retry()
def test_sum(a, b):
    """функция сложения"""
    return a + b

try:
    test_sum(1, "один")
    # Если функция выполнилась
    assert False, "Ошибка TypeError не вылетела наружу!"
except TypeError:
    # Ошибка вылетела, как мы и ожидали. Тест успешно пройден.
    pass 


# Тесты

assert test_sum.__doc__ == "функция сложения"


call_count = 0

def unstable_func():
    """Функция, которая падает первые 2 раза, а на 3-й раз выполняется успешно"""
    global call_count
    call_count += 1
    if call_count < 3:
        raise ValueError("Временный сбой")
    return "Успех"


@retry(max_attempts=2)
def normal_func():
    """normal_func"""
    return 42

assert normal_func() == 42, "Тест 1 провален: декоратор сломал успешную функцию"


@retry(max_attempts=2, delay=0.1)
def always_fails():
    """always_fails"""
    raise KeyError("Критическая ошибка")

try:
    always_fails()
    assert False, "Тест 2 провален: исключение не вылетело наружу"
except KeyError as e:
    # Проверяем, что вылетело именно наше оригинальное исключение
    assert str(e) == "'Критическая ошибка'"

call_count = 0  # Сбрасываем счетчик перед тестом
test_retry = retry(max_attempts=3, delay=0.01)(unstable_func)

assert test_retry() == "Успех", "Тест 3 провален: функция не восстановилась на 3-й попытке"
assert call_count == 3, "Тест 3 провален: функция была вызвана не 3 раза"
