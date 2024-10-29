from requests import post


url = "http://127.0.0.1:8000/users/register/"
data = {
    "username": "John",
    "email": "john.doe@example.com",
    "bio" : "Some bio",
}


response = post(url, data=data)


if response.status_code == 201:
    print("User created successfully:", response.json())
else:
    print("Error:", response.json())