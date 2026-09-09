{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "4570800c-01c4-426a-adbe-085dc7a1a9a2",
   "metadata": {},
   "outputs": [],
   "source": [
    "class EventBookingSystem:\n",
    "\n",
    "    def add_user(self, user_id: int, name: str) -> bool:\n",
    "        pass\n",
    "\n",
    "    def add_event(\n",
    "        self,\n",
    "        event_id: int,\n",
    "        name: str,\n",
    "        capacity: int\n",
    "    ) -> bool:\n",
    "        pass\n",
    "\n",
    "    def get_event(self, event_id: int) -> dict | None:\n",
    "        pass\n",
    "\n",
    "\n",
    "class EventBookingSystemImpl(EventBookingSystem):\n",
    "\n",
    "    def __init__(self):\n",
    "        self.users = []\n",
    "        self.events = []\n",
    "        self.bookings = []\n",
    "\n",
    "    def add_user(self, user_id: int, name: str) -> bool:\n",
    "        pass\n",
    "\n",
    "    def add_event(\n",
    "        self,\n",
    "        event_id: int,\n",
    "        name: str,\n",
    "        capacity: int\n",
    "    ) -> bool:\n",
    "        pass\n",
    "\n",
    "    def get_event(self, event_id: int) -> dict | None:\n",
    "        pass"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
