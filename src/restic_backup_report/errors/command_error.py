class CommandError(Exception):

    def __init__(
        self,
        cli_message: str,
        log_message: str | None = None
    ) -> None:

        self.cli_message = cli_message
        self.log_message = log_message or cli_message

        super().__init__(self.log_message)