from dataclasses import dataclass


@dataclass
class User():
    id: int
    name: str
    username: str
    password: str
    user_city: str

    def __init__(self, user_tuple: tuple):
        self.id = user_tuple[0]
        self.name = user_tuple[1]
        self.username = user_tuple[2]
        self.password = user_tuple[3]
        self.user_city = user_tuple[4]
    
    def __str__(self) -> str:
        return f"Пользователь {self.username}: id-{self.id}, name-{self.name}, город-{self.user_city}"

current_user: User = None