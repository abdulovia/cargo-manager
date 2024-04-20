# gui.py
import tkinter as tk
from tkinter import ttk
from transport import TransportManager
from database import Database

class TransportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Transport Management System")
        self.transport_manager = TransportManager()
        self.db = Database('transport.db')
        self.create_widgets()
        self.load_transports()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Add Transport
        self.add_transport_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.add_transport_frame, text='Add Transport')
        self.create_add_transport_widgets()

        # Tab 2: View Transports
        self.view_transports_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.view_transports_frame, text='View Transports')
        self.create_view_transports_widgets()

    def create_add_transport_widgets(self):
        self.add_transport_frame.columnconfigure(0, weight=1)
        self.add_transport_frame.rowconfigure(1, weight=1)

        self.vehicle_id_label = ttk.Label(self.add_transport_frame, text="Vehicle ID:")
        self.vehicle_id_label.grid(row=0, column=0, sticky="w")
        self.vehicle_id_entry = ttk.Entry(self.add_transport_frame)
        self.vehicle_id_entry.grid(row=0, column=1)

        self.capacity_label = ttk.Label(self.add_transport_frame, text="Capacity:")
        self.capacity_label.grid(row=1, column=0, sticky="w")
        self.capacity_entry = ttk.Entry(self.add_transport_frame)
        self.capacity_entry.grid(row=1, column=1)

        self.model_label = ttk.Label(self.add_transport_frame, text="Model:")
        self.model_label.grid(row=2, column=0, sticky="w")
        self.model_entry = ttk.Entry(self.add_transport_frame)
        self.model_entry.grid(row=2, column=1)

        self.manufacturer_label = ttk.Label(self.add_transport_frame, text="Manufacturer:")
        self.manufacturer_label.grid(row=3, column=0, sticky="w")
        self.manufacturer_entry = ttk.Entry(self.add_transport_frame)
        self.manufacturer_entry.grid(row=3, column=1)

        self.add_button = ttk.Button(self.add_transport_frame, text="Add Transport", command=self.edit_transport)
        self.add_button.grid(row=4, column=0, columnspan=2)

    def create_view_transports_widgets(self):
        self.view_transports_frame.columnconfigure(0, weight=1)
        self.view_transports_frame.rowconfigure(0, weight=1)

        self.transports_listbox = tk.Listbox(self.view_transports_frame, width=50, height=10)
        self.transports_listbox.grid(row=0, column=0, sticky="nsew")

        self.load_transports_button = ttk.Button(self.view_transports_frame, text="Load Transports", command=self.load_transports)
        self.load_transports_button.grid(row=1, column=0)

        self.delete_button = ttk.Button(self.view_transports_frame, text="Delete", command=self.delete_transport)
        self.delete_button.grid(row=2, column=0)

        self.edit_button = ttk.Button(self.view_transports_frame, text="Edit", command=self.edit_transport)
        self.edit_button.grid(row=3, column=0)

        self.delete_all_button = ttk.Button(self.view_transports_frame, text="Delete All", command=self.delete_all_transports)
        self.delete_all_button.grid(row=4, column=0)

    def delete_transport(self):
        selected_index = self.transports_listbox.curselection()
        if selected_index:
            selected_transport = self.transports_listbox.get(selected_index[0])
            vehicle_id = selected_transport.split(',')[0].split(':')[1].strip()
            self.db.remove_transport(vehicle_id)
            self.load_transports()

    def edit_transport(self):
        selected_index = self.transports_listbox.curselection()
        if selected_index:
            selected_transport = self.transports_listbox.get(selected_index[0])
            vehicle_id = selected_transport.split(',')[0].split(':')[1].strip()
            transport = self.db.get_transport_by_id(vehicle_id)
            if transport:
                edit_window = EditTransportWindow(self.root, transport, self.db, self.load_transports)
            self.root.wait_window(edit_window.top)

    def delete_all_transports(self):
        self.db.cur.execute("DELETE FROM transports")
        self.db.conn.commit()
        self.load_transports()

    def load_transports(self):
        self.transports_listbox.delete(0, tk.END)
        transports = self.db.get_all_transports()
        for transport in transports:
            self.transports_listbox.insert(tk.END, transport)

class EditTransportWindow:
    def __init__(self, root, transport, db, callback):
        self.top = tk.Toplevel(root)
        self.top.title("Edit Transport")
        self.transport = transport
        self.db = db
        self.callback = callback

        self.create_widgets()

    def create_widgets(self):
        self.vehicle_id_label = ttk.Label(self.top, text="Vehicle ID:")
        self.vehicle_id_label.grid(row=0, column=0)
        self.vehicle_id_entry = ttk.Entry(self.top, state="readonly")
        self.vehicle_id_entry.grid(row=0, column=1)
        self.vehicle_id_entry.insert(0, self.transport.vehicle_id)

        self.capacity_label = ttk.Label(self.top, text="Capacity:")
        self.capacity_label.grid(row=1, column=0)
        self.capacity_entry = ttk.Entry(self.top)
        self.capacity_entry.grid(row=1, column=1)
        self.capacity_entry.insert(0, self.transport.capacity)

        self.model_label = ttk.Label(self.top, text="Model:")
        self.model_label.grid(row=2, column=0)
        self.model_entry = ttk.Entry(self.top)
        self.model_entry.grid(row=2, column=1)
        self.model_entry.insert(0, self.transport.model)

        self.manufacturer_label = ttk.Label(self.top, text="Manufacturer:")
        self.manufacturer_label.grid(row=3, column=0)
        self.manufacturer_entry = ttk.Entry(self.top)
        self.manufacturer_entry.grid(row=3, column=1)
        self.manufacturer_entry.insert(0, self.transport.manufacturer)

        self.save_button = ttk.Button(self.top, text="Save", command=self.save_transport)
        self.save_button.grid(row=4, column=0, columnspan=2)

    def save_transport(self):
        self.transport.capacity = float(self.capacity_entry.get())
        self.transport.model = self.model_entry.get()
        self.transport.manufacturer = self.manufacturer_entry.get()
        self.db.update_transport(self.transport)
        self.callback()
        self.top.destroy()

def main():
    root = tk.Tk()
    app = TransportApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
