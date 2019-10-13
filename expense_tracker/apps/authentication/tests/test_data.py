"""
authentication test data
"""
valid_user = {

        "username": "CryceTruly",
        "email": "aacryce@gmail.com",
        "password": "Password123"

}

valid_login = {

        "email": "aacryce@gmail.com",
        "password": "Password123"

}

valid_user_two = {

        "username": "crycetruly",
        "email": "crycetruly@gmail.com",
        "password": "xvq6thcuzy"

}


valid_login_two = {

        "email": "crycetruly@gmail.com",
        "password": "xvq6thcuzy"

}

wrong_password = {

        "email": "aacryce@gmail.com",
        "password": "Password12"

}

wrong_email = {

        "email": "bagenda@gmail.com",
        "password": "Password123"

}

missing_password_data = {

        "email": "Password123"

}
missing_email_data = {

        "password": "Password123"

}
empty_username = {

        "username": "",
        "email": "aacryce@gmail.com",
        "password": "Password123"

}
empty_email = {

        "username": "Bagzie",
        "email": "",
        "password": "Password123"

}
empty_password = {

        "username": "Bagzie",
        "email": "aacryce@gmail.com",
        "password": ""

}
invalid_user_email = {

        "username": "Bagzie",
        "email": "bagendadegmail.com",
        "password": "Password123"

}

short_password = {

        "username": "Bagzie",
        "email": "aacryce@gmail.com",
        "password": "Pass"

}

missing_username_key = {

        "email": "aacryce@gmail.com",
        "password": "Password123"

}


invalid_token = "eyJ0eXiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IkFoZWJ3YTEiLCJlbWFpbCI6ImNyeWNldHJ1bHlAZ21haWwuY29tIiwiZXhwIjoxNTUxNzc2Mzk0fQ.PFimaBvSaxR_cKwLmeRMod7LHkhNTcem22IXTrrg7Ko"
expired_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IkFoZWJ3YTEiLCJlbWFpbCI6ImNyeWNldHJ1bHlAZ21haWwuY29tIiwiZXhwIjoxNTUxNzc2Mzk0fQ.PFimaBvSaxR_cKwLmeRMod7LHkhNTcem22IXTrrg7Ko"

invalid_username = {

        "username": "testus i",
        "email": "testuser@gmail.com",
        "password": "testing123"

}

invalid_password = {

        "username": "testuser12",
        "email": "testuser@gmail.com",
        "password": "testingui"

}

same_email = {

        "username": "roy12",
        "email": "aacryce@gmail.com",
        "password": "Password123"

}

same_username = {

        "username": "CryceTruly",
        "email": "roywaisibani@gmail.com",
        "password": "Password123"

}

responses = {
    'test_login_with_invalid_user_fails':{
            "errors": {
                "error": [
                    "A user with this email and password was not found."
                ]
            }
        },

    'invalid_username':{
        "errors":{
            "username": [
                "Username cannot contain special characters."
            ]
        }
    },

    'invalid_email':{
        "errors":{
            "email": [
                "Enter a valid email address."
            ]
        }
    },


    'test_login_with_missing_email_fails': {
            "errors": {
                "error": [
                    "A user with this email and password was not found."
                ]
            }
        },
    'email_already_exists':{
            "errors": {
                "email": [
                    "user with this email already exists."
                ]
            }
        },
    'password_is_too_short': {
            "errors": {
                "password": [
                    "Password should be atleast 8 characters"
                ]
            }
        },
    'password_is_weak':  {
            "errors": {
                "password": [
                    "Password should at least contain a number, capital and small letter."
                ]
            }
        },
    'username_already_exists': {
            "errors": {
                "username": [
                    "user with this username already exists."
                ]
            }
        }
}
