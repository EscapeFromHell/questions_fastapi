from requests import Session


class Repository:
    def __init__(self, db: Session):
        self.db: Session = db
