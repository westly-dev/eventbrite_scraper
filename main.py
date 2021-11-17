from db import DatabaseFactory
from scraper import EventbriteScraper


if __name__ == "__main__":

    events = EventbriteScraper.get_events("lagos", "nigeria", "tech", 100)
    event_tuples = list(map(lambda e: e.to_tuple(), events))

    db = DatabaseFactory.create_database(
        **{'database_exist': True, 'database': "sqlite",  'database_name': 'all_events'})
    db.insert(event_tuples)

    counter = 1
    for event in events:
        print(
            f'{counter}. {event.title} on {event.date} {event.time}, event page: {event.url}')
        counter += 1
