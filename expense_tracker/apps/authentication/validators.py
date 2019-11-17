from rest_framework import serializers
from validate_email import validate_email
from expense_tracker.apps.authentication.models import User


def validate_user_email(email):
    check_email = User.objects.filter(email=email)
    if not validate_email(email):
        raise serializers.ValidationError(
            "Incorrect email format please try again")
    if check_email.exists():
        raise serializers.ValidationError(
            "This email has already been used to create a user")
    return email
