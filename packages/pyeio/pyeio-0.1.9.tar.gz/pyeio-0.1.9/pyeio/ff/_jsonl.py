import typically as t

M = t.TypeVar("M", bound=t.Model)

class jsonl:
    @t.overload
    @staticmethod
    def load(
        path: t.ConvertibleToPath,
    ) -> list[t.Any]: ...
    @t.overload
    @staticmethod
    def load(
        path: t.ConvertibleToPath,
        model: type[M],
    ) -> list[M]: ...
    @staticmethod
    def load(
        path: t.ConvertibleToPath,
        model: type[M] | None = None,
    ) -> list[t.Any] | list[M]:
        """ """
        ...

    @staticmethod
    def save(
        data: list[t.Any],
        path: t.ConvertibleToPath,
        overwrite: bool = False,
    ) -> None:
        """ """
        ...

    @staticmethod
    def append(data: t.Any): ...

    @staticmethod
    def insert(data): ...

    @staticmethod
    def delete(data): ...


# def parse(): ...


# def serialize(): ...


# def open(): ...


# def read(): ...


# def save(): ...


# def load(): ...


# def stream(): ...


# def download(): ...


# def append(): ...


# def prepend(): ...


# def walk(): ...


# import orjson
# from pyeio.types import FilePath


# def stream(): ...


# # import json
# # from pathlib import Path
# # from .core import io


# # def load(path: str | Path) -> list | dict:
# #     return json.loads(io.load_text(path))


# # def save(): ...


# # todo
# # def stream(
# #     path: str | Path,
# #     validator,
# #     handler,
# # ): ...


# # # same as stream except operation is done on each element
# # def stream_ingest(
# #     path,
# #     validator,
# #     handler,
# #     errors,  # raise or log
# # ): ...
