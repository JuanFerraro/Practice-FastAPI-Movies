# Pydantic
from pydantic import BaseModel, Field

# User Model Pydantic
class User(BaseModel):
    email: str = Field(min_length=5, max_length=100,
                       title="Email",
                       description="This is the email")
    password: str = Field(min_length=5, max_length=15,
                          title="Password",
                          description="This is the password")