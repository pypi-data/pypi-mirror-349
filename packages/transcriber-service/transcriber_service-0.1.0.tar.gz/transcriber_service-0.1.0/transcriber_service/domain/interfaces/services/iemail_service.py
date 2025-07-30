from abc import ABC, abstractmethod


class IEmailService(ABC):
    @abstractmethod
    def send_recovery_email(self, target_email: str, temp_password: str): ...
