from .base_target import Target, InputType


class FileTarget(Target):

    def _inputs(self) -> None:
        super()._inputs()

        self.path = self.request_attribute(
            "path", 
            InputType.FILE
        )
    
    def _create(self, inputs: dict) -> None:
        self.path = inputs["path"]

    def validator_schema(self) -> dict:
        return {
            "path": {
                "type": "string",
                "required": True,
            }
        }

    def to_yaml(self) -> dict:
        return {
            "path": self.path
        }