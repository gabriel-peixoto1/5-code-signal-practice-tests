{
 "cells": [],
 "metadata": {},
 "nbformat": 4,
 "nbformat_minor": 5
}

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


class EventBookingSystemImpl(EventBookingSystem):

    def __init__(self):
        self.users = []
        self.events = []
        self.bookings = []

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
