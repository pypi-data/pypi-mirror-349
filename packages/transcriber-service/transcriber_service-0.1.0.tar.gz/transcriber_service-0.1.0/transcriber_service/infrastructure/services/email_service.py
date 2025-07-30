import smtplib
from email.message import EmailMessage

from ...domain.interfaces import IEmailService


class EmailService(IEmailService):
    def __init__(
        self, smtp_server: str, smtp_port: int, sender_email: str, sender_password: str
    ):
        """
        Initializes the email services for sending recovery emails using an SMTP server.

        :param smtp_server: The SMTP server address (e.g., smtp.gmail.com).
        :param smtp_port: Port number for the SMTP server (commonly 465 for SSL or 587 for TLS).
        :param sender_email: Email address of the sender (used for authentication and sending).
        :param sender_password: Password or app token for the sender's email account.
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_recovery_email(self, target_email: str, temp_password: str):
        """
        Sends a password recovery email containing the temporary password.

        :param target_email: Recipient's email address.
        :param temp_password: The generated temporary password to include in the email.
        :raises Exception: If there is an error during the sending process.
        """
        message = EmailMessage()
        message["Subject"] = "Password Recovery"
        message["From"] = self.sender_email
        message["To"] = target_email

        message.set_content(
            f"""
        You have requested to recover your account password.
        Your temporary password is: {temp_password}

        Please log in using this password and change it immediately to ensure security.

        Best regards,
        Support Team
        
        Здравствуйте!
        
        Вы отправили запрос на восстановление пароля.
        Ваш временный пароль: {temp_password}.
        
        Войдите, используя этот пароль, и поменяйте его как можно скорее.
        
        Пожалуйста, проигнорируйте данное письмо, если оно попало к Вам по ошибке.
        
        --
        С уважением,
        Служба поддержки
        """
        )

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.ehlo()

            if self.smtp_port == 587:
                server.starttls()

            server.login(self.sender_email, self.sender_password)
            server.send_message(message)
