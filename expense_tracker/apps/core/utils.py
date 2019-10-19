from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage


class Utilities:
    """Utility class that contains helper function"""

    @staticmethod
    def send_email(data,domain=None,intent=None):
        """This function sends email to users."""
        if intent == 'article_reports':
            EmailMessage(data['subject'],body=data['body'],to=[data['to']]).send(fail_silently=False)

        elif intent=='password_rest':
            url = f"{domain}/reset_password/{data[2]}"
            subject = f"[Authors Heaven] {data[3]}"
            body = f"Hello, \
                               \nYou are receiving this e-mail because you have {data[4]}' \
                               '\nClick the click below to verify your account.\n{url}"
            EmailMessage(subject, body, to=[data[5]]).send(fail_silently=False)
        else:
            url = f"http://{get_current_site(data[0]).domain}/api/users/{data[1]}?token={data[2]}"
            subject = f"[Authors Heaven] {data[3]}"
            body = f"Hello, \
                    \nYou are receiving this e-mail because you have {data[4]}' \
                    '\nClick the click below to verify your account.\n{url}"
            EmailMessage(subject, body, to=[data[5]]).send(fail_silently=False)
        return
