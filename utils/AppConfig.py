import os
import threading
from dotenv import load_dotenv


class AppConfig:
    """
    Thread-safe Singleton class to manage application configuration.
    """

    _instance = None
    _lock = threading.Lock()  # Lock object to synchronize threads

    def __new__(cls):
        """
        Override __new__ to implement thread-safe singleton pattern.
        """
        if cls._instance is None:
            with cls._lock:  # Ensure only one thread can initialize the instance
                if cls._instance is None:  # Check again to ensure only one object is created
                    cls._instance = super(AppConfig, cls).__new__(cls)
                    cls._instance._init()
        return cls._instance

    def _init(self):
        """
        Initialize the AppConfig instance by loading environment variables.
        This method is called only once during the lifetime of the singleton.
        """
        load_dotenv(override=True)

        self.groq_api_key = os.getenv("GROQ_API_KEY")

    def get_groq_api_key(self):
        return self.groq_api_key


# Example usage
if __name__ == "__main__":
    config1 = AppConfig()
    config2 = AppConfig()

    # Both config1 and config2 should refer to the same singleton instance
    print(config1 is config2)  # Should print: True
    print(config1.get_groq_api_key())
