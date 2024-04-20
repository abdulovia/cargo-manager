# transport.py

class Transport:
    def __init__(self, vehicle_id, capacity, model=None, manufacturer=None):
        self.vehicle_id = vehicle_id
        self.capacity = capacity
        self.model = model
        self.manufacturer = manufacturer
        self.is_booked = False
        
    def __str__(self):
        return f"Vehicle ID: {self.vehicle_id}, Capacity: {self.capacity}, Model: {self.model}, Manufacturer: {self.manufacturer}, Booked: {self.is_booked}"


class TransportManager:
    def __init__(self):
        self.transports = []

    def add_transport(self, vehicle_id, capacity, model=None, manufacturer=None):
        transport = Transport(vehicle_id, capacity, model, manufacturer)
        self.transports.append(transport)

    def remove_transport(self, vehicle_id):
        for transport in self.transports:
            if transport.vehicle_id == vehicle_id:
                self.transports.remove(transport)
                return True
        return False

    def get_all_transports(self):
        return self.transports

    def get_available_transports(self):
        return [transport for transport in self.transports if not transport.is_booked]

    def get_booked_transports(self):
        return [transport for transport in self.transports if transport.is_booked]
