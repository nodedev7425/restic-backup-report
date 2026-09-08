from .target import Target, InputType


class FileTarget(Target):

    def validator_schema(self) -> dict:
        return {
            "path": {
                "type": "string",
                "required": True,
            }
        }

    def _inputs(self) -> None:
        super()._inputs()

        self.path = self.request_attribute(
            "path", 
            InputType.FILE
        )

    def _create(self, inputs: dict) -> None:
        raise NotImplementedError