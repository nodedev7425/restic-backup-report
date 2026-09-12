from restic_backup_report.utils.console import request_attribute

from .base_target import Target, InputType


class FileTarget(Target):


    def _inputs(self) -> None:
        super()._inputs()

        self.path = request_attribute(
            "path", 
            InputType.FILE
        )

    
    def _create(self, definition: dict) -> None:
        super()._create(definition)

        self.path = definition["config"]["path"]


    def validator_schema(self) -> dict:
        return {
            "path": {
                "type": "string",
                "required": True,
            }
        }


    def send(self) -> None:
        print("send")


    def encrypted_fields() -> dict[str, str]:
        return {}        


    def to_dict(self) -> dict:
        return {
            "path": self.path
        }