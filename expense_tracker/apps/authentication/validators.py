import re

from django.shortcuts import get_object_or_404

from rest_framework import serializers

<<<<<<< HEAD
<<<<<<< HEAD
from expense_tracker.apps.authentication.models import User
=======
from authors.apps.authentication.models import User
>>>>>>> feat(accounts): Implement Account management
=======
from expense_tracker.apps.authentication.models import User
>>>>>>> ch(access): Implement Access control

def validate_email(email):
    check_email = User.objects.filter(email=email)
    email_regex = r'^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$'
    if not re.search(email_regex, email):
        raise serializers.ValidationError("Incorrect email format please try again")
    if check_email.exists():
        raise serializers.ValidationError("This email has already been used to create a user")
    return email
