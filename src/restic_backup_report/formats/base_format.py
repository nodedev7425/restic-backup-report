from abc import ABC


class Format(ABC):

    pass


class FormatRegister():


    _formats: dict[str, type[Format]] = {}
    
    
    @classmethod
    def register(cls, name: str, format: type[Format]) -> None:
        if name in cls._formats:
            raise ValueError(f"Format '{name}' is already registered")

        if format in cls._formats.values():
            raise ValueError(
                f"Format '{format.__name__}' is already registered"
            )

        cls._formats[name] = format


    @classmethod
    def register_formats(cls, formats: dict[str, type[Format]]):
        for key in formats.keys():
            cls.register(key, formats[key])


    @classmethod
    def get(cls, name: str) -> type[Format]:
        try:
            return cls._formats[name]
        except KeyError:
            raise KeyError(f"Format '{name}' is not registered")


    @classmethod
    def get_name(cls, format: type[Format]) -> str:
        for name, registered_target in cls._formats.items():
            if registered_target is format:
                return name

        raise KeyError(
            f"Format '{format.__name__}' is not registered"
        )


    @classmethod
    def names(cls) -> list[str]:
        return list(cls._formats)


    @classmethod
    def has(cls, name: str) -> bool:
        return name in cls._formats