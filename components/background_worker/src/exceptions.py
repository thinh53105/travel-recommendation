class RecordNotExists(Exception):
    pass


class UpstreamServiceUnavailable(Exception):

    def __init__(self, name) -> None:
        self.name = name
