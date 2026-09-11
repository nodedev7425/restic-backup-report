from restic_backup_report.utils.console import request_attribute

from .base_target import Target, InputType


class FileTarget(Target):


    def _inputs(self) -> None:
        super()._inputs()

        self.path = request_attribute(
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


    def send(self) -> None:
        print("send")


    def encrypted_fields(self) -> dict[str, str]:
        return {}        


    def to_dict(self) -> dict:
        return {
            "path": self.path
        }