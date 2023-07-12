from enum import Enum


class Gender(str, Enum):
    Male = "male"
    Female = "female"


class Role(str, Enum):
    AI = "AI"
    Admin = "admin"
    User = "user"
    Super = "super"
