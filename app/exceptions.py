class GeneralException(Exception):
    """
    General exception for whole project
    """

    def __init__(
        self,
        public_message: str = "Unknown exception",
        *args,
        **kwargs
    ):
        self.public_message = public_message
        super().__init__(*args, **kwargs)
