class Helper:

    @staticmethod
    def singleton(class_):
        instances = {}

        def get_instance(*args, **kwargs):
            if class_ not in instances:
                instances[class_] = class_(*args, **kwargs)
            return instances[class_]

        return get_instance

    @staticmethod
    def loadEnv():
        from dotenv import load_dotenv
        load_dotenv()

    @staticmethod
    def getEnv(key):
        from os import getenv
        return getenv(key)