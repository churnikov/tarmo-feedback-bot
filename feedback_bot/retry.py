from loguru import logger
from telegram.error import TimedOut


class Retry:
    """Класс для создания повторных попыток запустить функцию."""

    def __init__(self, retry_count: int, function, function_kwargs: dict):
        """
        Создание обернутой функции.

        :param retry_count: Сколько раз попытаться повторить функцию
        :param function: Оборачиваемая функция
        :param function_kwargs: Аргументы функции
        """
        self.function_kwargs = function_kwargs
        self.function = function
        self.retry_count = retry_count

    def retry(self):
        """
        Начать выполнение функции для которой надо уметь делать повторные запросы.

        :return: результат выполнения функции
        """
        raise NotImplementedError()


class TelegramTimedOutRetry(Retry):
    def retry(self):
        try:
            return self.function(**self.function_kwargs)
        except TimedOut as e:
            if self.retry_count > 0:
                logger.warning("Got timeout. Retrying.")
                self.retry_count -= 1
                return self.retry()
            else:
                logger.error(
                    "Raising 'TimedOut' exception, because maximum number of reties reached."
                )
                raise e
