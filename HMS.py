import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3

class Booking:
    def __init__(self, name, check_in_date, check_out_date, room_type, booking_id):
        self.name = name
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.room_type = room_type
        self.booking_id = booking_id

class HotelManagementSystem:
    def __init__(self):
        self.conn = sqlite3.connect('hotel_management.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bookings
                               (id INTEGER PRIMARY KEY, name TEXT, check_in_date TEXT, check_out_date TEXT, room_type TEXT)''')
        self.conn.commit()

    def add_booking(self, name, check_in_date, check_out_date, room_type):
        self.cursor.execute('''INSERT INTO bookings (name, check_in_date, check_out_date, room_type)
                               VALUES (?, ?, ?, ?)''', (name, check_in_date, check_out_date, room_type))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_bookings(self):
        self.cursor.execute('''SELECT * FROM bookings''')
        return self.cursor.fetchall()

    def delete_booking(self, booking_id):
        self.cursor.execute('''DELETE FROM bookings WHERE id = ?''', (booking_id,))
        self.conn.commit()

class HotelManagementSystemGUI:
    def __init__(self, master):
        self.system = HotelManagementSystem()
        self.master = master
        self.master.title("Hotel Management System")

        self.tree = ttk.Treeview(master, columns=("ID", "Name", "Check-In Date", "Check-Out Date", "Room Type"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Check-In Date", text="Check-In Date")
        self.tree.heading("Check-Out Date", text="Check-Out Date")
        self.tree.heading("Room Type", text="Room Type")
        self.tree.pack()

        self.add_booking_btn = tk.Button(master, text="Add Booking", command=self.add_booking)
        self.add_booking_btn.pack()

        self.view_bookings_btn = tk.Button(master, text="View Bookings", command=self.view_bookings)
        self.view_bookings_btn.pack()

        self.delete_booking_btn = tk.Button(master, text="Delete Booking", command=self.delete_booking)
        self.delete_booking_btn.pack()

    def add_booking(self):
        name = simpledialog.askstring("Input", "Customer Name:", parent=self.master)
        check_in_date = simpledialog.askstring("Input", "Check-In Date (YYYY-MM-DD):", parent=self.master)
        check_out_date = simpledialog.askstring("Input", "Check-Out Date (YYYY-MM-DD):", parent=self.master)
        room_type = simpledialog.askstring("Input", "Room Type (e.g., Single, Double, Suite):", parent=self.master)
        if name and check_in_date and check_out_date and room_type:
            self.system.add_booking(name, check_in_date, check_out_date, room_type)
            messagebox.showinfo("Success", "Booking added successfully")
        else:
            messagebox.showwarning("Warning", "All fields are required")

    def view_bookings(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for booking in self.system.get_bookings():
            self.tree.insert('', 'end', values=booking)

    def delete_booking(self):
        booking_id = simpledialog.askinteger("Input", "Enter Booking ID to delete:", parent=self.master)
        if booking_id:
            self.system.delete_booking(booking_id)
            messagebox.showinfo("Success", "Booking deleted successfully")

def main():
    root = tk.Tk()
    app = HotelManagementSystemGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
