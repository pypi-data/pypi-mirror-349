import machinic.types as t
from machinic.guard import verify


class text:
    @staticmethod
    def load(path: t.ConvertibleToPath) -> str:
        with open(path, "r") as f:
            data = f.read()
        f.close()
        return data

    @staticmethod
    def save(
        data: str,
        path: t.ConvertibleToPath,
        overwrite: bool = False,
    ) -> None:
        path = verify.path(path, exists=overwrite)
        with open(path, "w") as f:
            f.write(data)
        f.close()
