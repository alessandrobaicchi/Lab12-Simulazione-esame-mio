import datetime
from dataclasses import dataclass


@dataclass
class Actor:
    id: str
    name: str
    date_of_birth: datetime.date


    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return f"{self.name} ({self.date_of_birth})"


    def age(self):
        today = datetime.date.today()
        age = today.year - self.date_of_birth.year

        # Se non è ancora arrivato il suo compleanno tolgo 1 anno
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1
        return age