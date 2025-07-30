import typically as t


class binary:
    @staticmethod
    def load(path: t.ConvertibleToPath) -> bytes:
        with open(path, "rb") as f:
            data: bytes = f.read()
        f.close()
        return data

    @staticmethod
    def save(
        data: bytes,
        path: t.ConvertibleToPath,
        overwrite: bool = False,
    ) -> None:
        path = t.verify.path(path, overwritable=overwrite)
        with open(path, "wb") as f:
            f.write(data)
        f.close()
