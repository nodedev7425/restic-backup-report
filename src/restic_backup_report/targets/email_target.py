import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from restic_backup_report.reports.base_report import Report
from restic_backup_report.targets.base_target import Target
from restic_backup_report.utils.console import InputType, request_attribute


class EmailTarget(Target):

    def _inputs(self) -> None:
        super()._inputs()

        self.sender = request_attribute(
            "sender", 
            InputType.TEXT
        )

        self.password = request_attribute(
            "password",
            InputType.PASSWORD
        )

        self.recipient = request_attribute(
            "recipient",
            InputType.TEXT
        )

        self.smtp_server = request_attribute(
            "smtp_server",
            InputType.TEXT
        )

        self.smtp_port = request_attribute(
            "smtp_port",
            InputType.SELECT,
            values=[587, 465, 25, 2525]
        )

        # TODO: Add TLDR und EMAIL 

    
    def _create(self, definition: dict) -> None:
        super()._create(definition)

        self.sender = definition["config"]["sender"]
        self.password = definition["config"]["password"]
        self.recipient = definition["config"]["recipient"]
        self.smtp_server = definition["config"]["smtp_server"]
        self.smtp_port = definition["config"]["smtp_port"]


    def validator_schema(self) -> dict:
        return {}


    def send(self, report: Report) -> None:
        super().send(report)

        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = self.recipient
        msg['Subject'] = 'Test'

        body = report.render()
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        # TODO: Support different formats

        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
            server.login(self.sender, self.password)
            server.send_message(msg)
            server.close()


    @staticmethod
    def encrypted_fields() -> dict[str, str]:
        return {  
            "password": "password"
        } 


    def to_dict(self) -> dict:
        return {
            "sender": self.sender,
            "password": self.password,
            "recipient": self.recipient,
            "smtp_server": self.smtp_server,
            "smtp_port": self.smtp_port
        }