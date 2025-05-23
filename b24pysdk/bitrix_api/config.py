from typing import Union


class SdkConfig:
    """This class allows you to configure behaviour of the SDK"""
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.default_timeout = 10
            cls.__instance.max_retries = 20
            cls.__instance.initial_retry_delay = 0.5
            cls.__instance.retry_delay_increment = 0.25

        return cls.__instance

    __default_timeout: Union[int, float, None]
    __max_retries: int
    __initial_retry_delay: float
    __retry_delay_increment: float

    @property
    def default_timeout(self):
        """Default timeout for API calls"""
        return self.__default_timeout

    @default_timeout.setter
    def default_timeout(self, value: Union[int, float, None]):
        assert value is None or isinstance(value, (int, float))
        self.__default_timeout = None if value is None or value < 0 else value

    @property
    def max_retries(self):
        """Maximum number retries that will occur when server is not responding"""
        return self.__max_retries

    @max_retries.setter
    def max_retries(self, value: int):
        assert isinstance(value, int)
        assert value >= 1
        self.__max_retries = value

    @property
    def initial_retry_delay(self):
        """Initial delay between retries in seconds"""
        return self.__initial_retry_delay

    @initial_retry_delay.setter
    def initial_retry_delay(self, value: float):
        assert isinstance(value, (int, float))
        assert value >= 0
        self.__initial_retry_delay = float(value)

    @property
    def retry_delay_increment(self):
        """Amount by which delay between retries will increment after each retry"""
        return self.__retry_delay_increment

    @retry_delay_increment.setter
    def retry_delay_increment(self, value: float):
        assert isinstance(value, (int, float))
        assert value >= 0
        self.__retry_delay_increment = float(value)
