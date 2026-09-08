class EventBookingSystem:

    def add_user(self, user_id: int, name: str) -> bool:
        pass

    def add_event(
        self,
        event_id: int,
        name: str,
        capacity: int
    ) -> bool:
        pass

    def get_event(self, event_id: int) -> dict | None:
        pass
########

class EventBookingSystemImpl(EventBookingSystem):

    def __init__(self):
        self.users = []
        self.events = []
        self.bookings = []
        self.waitlist = []

    def add_user(self, user_id: int, name: str) -> bool:
        for user in self.users:
            if user['user_id'] == user_id:
                return False
        user = {'user_id': user_id, 'name': name}
        self.users.append(user)
        return True

    
    def add_event(self, event_id: int, name: str, capacity: int) -> bool:
        
        if capacity <= 0:
            return False
        for event in self.events: 
            if event['event_id'] == event_id:
                return False

        event = {'event_id': event_id, 'name': name, 'capacity': capacity, 'available': capacity}     # initially, all the seats are availabe.
        self.events.append(event)
        return True

    
    def get_event(self, event_id: int) -> dict | None:

        for event in self.events:
            if event['event_id'] == event_id:
                return event
        return None

    def create_booking(self, booking_id: int, user_id: int, event_id: int, seats: int) -> bool:

        if seats <= 0:
            return False
            
        for booking in self.bookings:
            if booking['booking_id'] == booking_id:
                return False
                
        for user in self.users:
            for event in self.events:
                if user['user_id'] == user_id and event['event_id'] == event_id and event['available'] >= seats:
                    booking = {'booking_id': booking_id, 'user_id': user_id, 'event_id': event_id, 'seats': seats, 'status': 'active'}
                    event['available'] = event['available'] - seats
                    self.bookings.append(booking)
                    return True
                    
        return False
        

    def cancel_booking(self, booking_id: int) -> bool:

        for booking in self.bookings:
            if booking['booking_id'] == booking_id and booking['status'] != 'cancelled':
                booking['status'] = 'cancelled'
                for event in self.events:
                    if event['event_id'] == booking['event_id']:
                        event['available'] += booking['seats']
                        return True
                
        return False

        

    def get_user_bookings(self, user_id: int) -> list[dict]:
        
        user_bookings = []

        for booking in self.bookings:
            if booking['user_id'] == user_id:
                user_bookings.append(booking)

        user_bookings.sort(key = lambda user_bookings: user_bookings['booking_id'])
        
        return user_bookings


    def get_event_bookings(self, event_id: int) -> list[dict]:

        bookings_by_event = []

        for booking in self.bookings:
            if booking['event_id'] == event_id and booking['status'] == 'active':
                bookings_by_event.append(booking)

        bookings_by_event.sort(key=lambda booking: booking['booking_id'])

        return bookings_by_event            
        

    def get_event_occupancy(self, event_id: int) -> float:
        
        for event in self.events:
            if event['event_id'] == event_id:
                return (event['capacity'] - event['available'])/(event['capacity'])
        return 0.0

    def get_most_popular_event(self) -> int | None:

        popular_events_ids = []
        
        for event in self.events:
            popular_events_ids.append(event['event_id'])

        if len(popular_events_ids) == 0:
            return None

        popular_events_ids.sort(key = lambda popular_events_ids: self.get_event_occupancy(popular_events_ids) , reverse=True)

        return popular_events_ids[0]

    def join_waitlist(self, user_id: int, event_id: int) -> bool:
        
        for member in self.waitlist:
            if member['user_id'] == user_id:
                return False
        for booking in self.bookings:
            if booking['user_id'] == user_id:
                return False

        for user in self.users:
            for event in self.events:
                if user['user_id'] == user_id and event['event_id'] == event_id and event['available'] == 0:
                        self.waitlist.append(user)
                        return True


        return False


    def leave_waitlist(self, user_id: int, event_id: int) -> bool:
        pass

    def get_waitlist(self, event_id: int) -> list[int]:
        pass







        