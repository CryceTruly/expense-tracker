"""
authentication test data
"""
valid_user = {

        "username": "CryceTruly",
<<<<<<< HEAD
        "email": "crycetruly@gmail.com",
=======
        "email": "aacryce@gmail.com",
>>>>>>> feat(accounts): Implement Account management
        "password": "Password123"

}

valid_login = {

<<<<<<< HEAD
        "email": "crycetruly@gmail.com",
=======
        "email": "aacryce@gmail.com",
>>>>>>> feat(accounts): Implement Account management
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

<<<<<<< HEAD
        "email": "crycetruly@gmail.com",
=======
        "email": "aacryce@gmail.com",
>>>>>>> feat(accounts): Implement Account management
        "password": "Password12"

}

wrong_email = {

<<<<<<< HEAD
        "email": "cryce@gmail.com",
=======
        "email": "bagenda@gmail.com",
>>>>>>> feat(accounts): Implement Account management
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
<<<<<<< HEAD
        "email": "crycetruly@gmail.com",
=======
        "email": "aacryce@gmail.com",
>>>>>>> feat(accounts): Implement Account management
        "password": "Password123"

}
empty_email = {

<<<<<<< HEAD
        "username": "Chryce",
=======
        "username": "Bagzie",
>>>>>>> feat(accounts): Implement Account management
        "email": "",
        "password": "Password123"

}
empty_password = {

<<<<<<< HEAD
        "username": "Chryce",
        "email": "crycetruly@gmail.com",
=======
        "username": "Bagzie",
        "email": "aacryce@gmail.com",
>>>>>>> feat(accounts): Implement Account management
        "password": ""

}
invalid_user_email = {

<<<<<<< HEAD
        "username": "Chryce",
        "email": "crycedegmail.com",
=======
        "username": "Bagzie",
        "email": "bagendadegmail.com",
>>>>>>> feat(accounts): Implement Account management
        "password": "Password123"

}

short_password = {

<<<<<<< HEAD
        "username": "Chryce",
        "email": "crycetruly@gmail.com",
=======
        "username": "Bagzie",
        "email": "aacryce@gmail.com",
>>>>>>> feat(accounts): Implement Account management
        "password": "Pass"

}

missing_username_key = {

<<<<<<< HEAD
        "email": "crycetruly@gmail.com",
=======
        "email": "aacryce@gmail.com",
>>>>>>> feat(accounts): Implement Account management
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
<<<<<<< HEAD
        "email": "crycetruly@gmail.com",
=======
        "email": "aacryce@gmail.com",
>>>>>>> feat(accounts): Implement Account management
        "password": "Password123"

}

same_username = {

        "username": "CryceTruly",
<<<<<<< HEAD
        "email": "aacryce@gmail.com",
=======
        "email": "roywaisibani@gmail.com",
>>>>>>> feat(accounts): Implement Account management
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
