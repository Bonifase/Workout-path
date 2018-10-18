user_data = {
    "first_name": "username",
    "last_name": "lastname",
    "last_name": "lastname",
    "units": "64kg",
    "email": "user@gmail.com",
    "password": "user123"}

new_user = dict(
    first_name="Bill",
    last_name="Bill",
    units="65kg",
    email="bill@gmail.com",
    password="123456")

wrong_email = dict(email="user3@gmail.com", password="user123")

unregistered_user = dict(
    email="notregistered@email.com",
    username="someuser",
    password="someuser123")

wrong_password = dict(
    first_name="Bill",
    last_name="Bill",
    units="65kg",
    email="bill@gmail.com",
    password="123")

new_location = dict(
    name="Kisumu",
    country="Kenya",
    description="Third bigest")