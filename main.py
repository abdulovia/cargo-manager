# main.py
from transport import TransportManager
from database import Database

def main():
    db = Database('transport.db')
    transport_manager = TransportManager()

    # Пример использования
    transport_manager.add_transport("TR001", 10.0, model="Model A", manufacturer="Manufacturer A")
    transport_manager.add_transport("TR002", 15.0, model="Model B", manufacturer="Manufacturer B")
    transport_manager.add_transport("TR003", 20.0, model="Model C", manufacturer="Manufacturer C")

    for transport in transport_manager.transports:
        db.add_transport(transport.vehicle_id, transport.capacity, model=transport.model, manufacturer=transport.manufacturer)

    print("All Transports:")
    print(transport_manager.get_all_transports())

    print("Available Transports:")
    print(transport_manager.get_available_transports())

    print("Booked Transports:")
    print(transport_manager.get_booked_transports())

    db.close_connection()

if __name__ == "__main__":
    main()
