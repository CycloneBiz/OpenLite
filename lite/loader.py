import dotenv

dotenv.load_dotenv()

class Loader:
    def __init__(self, flask, logging) -> None:
        self.logging = logging
        self.app = flask