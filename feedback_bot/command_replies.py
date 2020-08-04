from dataclasses import dataclass, fields
from pathlib import Path


@dataclass
class Replies:
    """
    Датакласс для ответов бота. По умолчанию есть ответы на start и help ручки.

    Для других ботов можно сделать больше различных ответов.

    Тексты ответов находятся в папке data/replies и их можно загрузить используя метод ``load_from_dir``.

    >>> replies = Replies.load_from_dir(Path("data/replies"))
    """

    start: str = ""
    help: str = ""

    @classmethod
    def load_from_dir(cls, path: Path):
        """
        Загрузить тексты ответов из папки ``path``.

        >>> replies = Replies.load_from_dir(Path("data/replies"))

        :param path: Папка, где находятся ``.md`` файлы с ответами бота.
        :return: ``Replies`` instance
        """
        instance = cls()
        dc_fields = {f.name for f in fields(instance)}
        for p in path.iterdir():
            if p.is_file() and p.stem in dc_fields:
                with p.open() as f:
                    setattr(instance, p.stem, f.read())

        return instance
