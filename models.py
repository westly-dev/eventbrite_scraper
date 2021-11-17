from dataclasses import dataclass


@dataclass
class Event:
    url: str
    title: str
    date: str
    time: str
    venue: str
    street_address: str
    city: str
    state: str
    price: float

    def to_tuple(self):
        return (
            self.url, self.title, self.date, self.time, self.venue, self.street_address,
            self.city, self.state, self.price
        )
