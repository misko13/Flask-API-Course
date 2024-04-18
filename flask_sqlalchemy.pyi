from sqlalchemy.ext.declarative import DeclarativeMeta

class Model:
    pass

class ModelType(DeclarativeMeta):
    pass

class SQLAlchemy:
    def __init__(self, app=None, use_native_unicode=True, session_options=None, metadata=None):
        pass

    def init_app(self, app):
        pass

    def create_all(self):
        pass

    def drop_all(self):
        pass

    def session(self):
        pass

db: SQLAlchemy