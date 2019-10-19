import re

from django.contrib.auth import authenticate

from rest_framework import serializers

from authors.apps.profiles.serializers import ProfileSerializer
from .models import User

from .validators import validate_email


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        error_messages={
            "min_length": "Password should be atleast {min_length} characters"
        }
    )
    token = serializers.CharField(max_length=256, read_only=True)

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email', 'username', 'password', 'token']

    def validate(self, value):
        data = self.get_initial()
        email = data.get("email")
        username = data.get("username")

        # validate that username passed is correct
        if not username.isalnum():
            raise serializers.ValidationError(
                "The username is invalid please use letters and numbers")

        self.user_exists('username', username)

        # validate that the correct email format is used
        if not validate_email(email):
            raise serializers.ValidationError("Enter a valid email address.")
        # Validate email has not been used to create account before
        self.user_exists('email', email)
        return value

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**validated_data)

    def user_exists(self, field, value):
        if(field == 'email' and User.objects.filter(email=value).first() is not None):
            raise serializers.ValidationError(
                "This email has already been used to create a user")
        elif User.objects.filter(username=value).first() is not None:
            raise serializers.ValidationError(
                "This username already exists please choose another one")


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=256, read_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        password = data.get('password', None)

        # As mentioned above, an email is required. Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # As mentioned above, a password is required. Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value. Remember that, in our User
        # model, we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=email, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag to tell us whether the user has been banned
        # or otherwise deactivated. This will almost never be the case, but
        # it is worth checking for. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        # We need to first verify if a users email is verified before we can let them use  the platform

        verified_user = User.objects.filter(email=email).first()
        if not verified_user.is_verified:
            raise serializers.ValidationError(
                'Your email is not verified,please click the link in your mailbox')


        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    # Passwords must be at least 8 characters, but no more than 128
    # characters. These values are the default provided by Django. We could
    # change them, but that would create extra work while introducing no real
    # benefit, so let's just stick with the defaults.
    profile = ProfileSerializer(many=False, read_only=True, required=False)
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'profile', )

        # The `read_only_fields` option is an alternative for explicitly
        # specifying the field with `read_only=True` like we did for password
        # above. The reason we want to use `read_only_fields` here is because
        # we don't need to specify anything else about the field. For the
        # password field, we needed to specify the `min_length` and
        # `max_length` properties too, but that isn't the case for the token
        # field.

    def update(self, instance, validated_data):
        """Performs an update on a User."""

        # Passwords should not be handled with `setattr`, unlike other fields.
        # This is because Django provides a function that handles hashing and
        # salting passwords, which is important for security. What that means
        # here is that we need to remove the password field from the
        # `validated_data` dictionary before iterating over it.
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `User` instance one at a time.
            setattr(instance, key, value)

        if password is not None:
            # `.set_password()` is the method mentioned above. It handles all
            # of the security stuff that we shouldn't be concerned with.
            instance.set_password(password)

        # Finally, after everything has been updated, we must explicitly save
        # the model. It's worth pointing out that `.set_password()` does not
        # save the model.
        instance.save()

        return instance


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)

    class Meta:
        fields = ('email', )


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        fields = ('password', )
