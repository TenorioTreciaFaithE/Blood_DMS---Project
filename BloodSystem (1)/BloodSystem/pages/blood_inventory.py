import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector
from config import DB_CONFIG
from .base_page import BasePage


class BloodInventoryPage(BasePage):
    def __init__(self, parent):
        super().__init__(
            parent,
            title="Blood Inventory",
            subtitle="Monitor and manage blood inventory by type",
        )
        
        main_container = ttk.Frame(self.scrollable_frame)
        main_container.grid(row=self.body_row, column=0, sticky="nsew")
        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        self.scrollable_frame.rowconfigure(self.body_row, weight=1)
        
        form_card = self.create_card(main_container, "Update Blood Inventory", "Update blood stock levels. Double-click an item in the list to edit.")
        form_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        
        form_content = ttk.Frame(form_card)
        form_content.grid(row=2, column=0, sticky="ew", pady=(0, 0))
        form_content.columnconfigure(1, weight=1, minsize=150)
        
        ttk.Label(form_content, text="Blood Type *", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.blood_type_var = tk.StringVar()
        self.blood_type_combo = ttk.Combobox(form_content, textvariable=self.blood_type_var, 
                                           values=("A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"),
                                           state="readonly", style="TCombobox", font=("Segoe UI", 9))
        self.blood_type_combo.grid(row=0, column=1, padx=(0, 0), pady=(0, 6), sticky="ew", ipady=4)
        self.blood_type_combo.current(0)
        
        ttk.Label(form_content, text="Quantity *", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.quantity_var = tk.StringVar()
        self.quantity_entry = ttk.Entry(form_content, textvariable=self.quantity_var, style="TEntry", font=("Segoe UI", 9))
        self.quantity_entry.grid(row=1, column=1, padx=(0, 0), pady=(0, 6), sticky="ew", ipady=4)
        
        ttk.Label(form_content, text="Min Stock Level *", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.min_stock_var = tk.StringVar()
        self.min_stock_entry = ttk.Entry(form_content, textvariable=self.min_stock_var, style="TEntry", font=("Segoe UI", 9))
        self.min_stock_entry.grid(row=2, column=1, padx=(0, 0), pady=(0, 6), sticky="ew", ipady=4)
        
        ttk.Label(form_content, text="Expiry Date", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=3, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.expiry_var = tk.StringVar()
        self.expiry_entry = ttk.Entry(form_content, textvariable=self.expiry_var, style="TEntry", font=("Segoe UI", 9))
        self.expiry_entry.grid(row=3, column=1, padx=(0, 0), pady=(0, 6), sticky="ew", ipady=4)
        ttk.Label(form_content, text="(YYYY-MM-DD)", style="Subtle.TLabel", font=("Segoe UI", 8)).grid(row=3, column=2, sticky="w", padx=(4, 0))
        
        ttk.Label(form_content, text="Storage Location", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=4, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.storage_var = tk.StringVar()
        self.storage_entry = ttk.Entry(form_content, textvariable=self.storage_var, style="TEntry", font=("Segoe UI", 9))
        self.storage_entry.grid(row=4, column=1, padx=(0, 0), pady=(0, 10), sticky="ew", ipady=4)
        
        button_frame = ttk.Frame(form_card)
        button_frame.grid(row=3, column=0, sticky="ew", pady=(6, 0))
        button_frame.columnconfigure((0, 1, 2), weight=1, uniform="buttons")
        
        ttk.Button(button_frame, text="Update Inventory", style="Accent.TButton", command=self.update_inventory).grid(row=0, column=0, sticky="ew", padx=(0, 4), ipady=6)
        ttk.Button(button_frame, text="Add New Type", style="Outline.TButton", command=self.add_inventory).grid(row=0, column=1, sticky="ew", padx=(0, 4), ipady=6)
        ttk.Button(button_frame, text="Clear", style="Outline.TButton", command=self.clear_form).grid(row=0, column=2, sticky="ew", ipady=6)
        
        list_card = self.create_card(main_container, "Blood Inventory List", "Red background indicates low stock levels.")
        list_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        list_card.rowconfigure(2, weight=1)
        
        search_frame = ttk.Frame(list_card)
        search_frame.grid(row=2, column=0, sticky="ew", pady=(0, 8), padx=0)
        search_frame.columnconfigure(1, weight=1)
        
        ttk.Label(search_frame, text="Search:", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 8), pady=6)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, style="TEntry", font=("Segoe UI", 9))
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=(0, 0), pady=6, ipady=4)
        self.search_entry.bind("<KeyRelease>", self.filter_inventory)
        
        tree_frame = ttk.Frame(list_card)
        tree_frame.grid(row=3, column=0, sticky="nsew", padx=0, pady=(0, 0))
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        
        columns = ("ID", "Blood Type", "Quantity", "Min Level", "Status", "Location")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "Location":
                self.tree.column(col, width=120, anchor="w")
            elif col in ("Quantity", "Min Level"):
                self.tree.column(col, width=80, anchor="e")
            elif col == "Status":
                self.tree.column(col, width=80, anchor="center")
            else:
                self.tree.column(col, width=70, anchor="center")
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.tree.bind("<Double-1>", self.on_item_select)
        
        self.load_inventory()
    
    def get_db_connection(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            return conn
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {str(e)}")
            return None
    
    def load_inventory(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT inventory_id, blood_type, quantity, min_stock_level, storage_location FROM blood_inventory ORDER BY blood_type")
                rows = cursor.fetchall()
                
                for row in rows:
                    quantity = int(row[2])
                    min_level = int(row[3])
                    status = "Low Stock" if quantity <= min_level else "In Stock"
                    location = row[4] if row[4] else "N/A"
                    self.tree.insert("", tk.END, values=(
                        row[0], row[1], quantity, min_level, status, location
                    ), tags=(status,))
                
                self.tree.tag_configure("Low Stock", background="#FFE5E5")
                self.tree.tag_configure("In Stock", background="#FFFFFF")
                
                cursor.close()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to load inventory: {str(e)}")
            finally:
                conn.close()
    
    def filter_inventory(self, event=None):
        search_term = self.search_var.get().strip()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                if search_term:
                    search_pattern = f"%{search_term}%"
                    cursor.execute(
                        "SELECT inventory_id, blood_type, quantity, min_stock_level, storage_location FROM blood_inventory WHERE blood_type LIKE %s OR storage_location LIKE %s OR CAST(quantity AS CHAR) LIKE %s ORDER BY blood_type",
                        (search_pattern, search_pattern, search_pattern)
                    )
                else:
                    cursor.execute("SELECT inventory_id, blood_type, quantity, min_stock_level, storage_location FROM blood_inventory ORDER BY blood_type")
                
                rows = cursor.fetchall()
                
                for row in rows:
                    quantity = int(row[2])
                    min_level = int(row[3])
                    status = "Low Stock" if quantity <= min_level else "In Stock"
                    location = row[4] if row[4] else "N/A"
                    self.tree.insert("", tk.END, values=(
                        row[0], row[1], quantity, min_level, status, location
                    ), tags=(status,))
                
                self.tree.tag_configure("Low Stock", background="#FFE5E5")
                self.tree.tag_configure("In Stock", background="#FFFFFF")
                
                cursor.close()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to filter inventory: {str(e)}")
            finally:
                conn.close()
    
    def on_item_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            self.blood_type_var.set(values[1])
            self.quantity_var.set(str(values[2]))
            self.min_stock_var.set(str(values[3]))
            self.storage_var.set(values[5] if values[5] != "N/A" else "")
            
            conn = self.get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("SELECT expiry_date FROM blood_inventory WHERE inventory_id=%s", (values[0],))
                    result = cursor.fetchone()
                    if result and result[0]:
                        self.expiry_var.set(result[0].strftime("%Y-%m-%d"))
                    else:
                        self.expiry_var.set("")
                    cursor.close()
                except mysql.connector.Error:
                    pass
                finally:
                    conn.close()
    
    def add_inventory(self):
        blood_type = self.blood_type_var.get()
        quantity = self.quantity_var.get().strip()
        min_stock = self.min_stock_var.get().strip()
        expiry = self.expiry_var.get().strip()
        storage = self.storage_var.get().strip()
        
        if not blood_type or not quantity or not min_stock:
            messagebox.showwarning("Validation", "Please fill in all required fields")
            return
        
        try:
            quantity_int = int(quantity)
            min_stock_int = int(min_stock)
        except ValueError:
            messagebox.showerror("Validation", "Please enter valid numbers for quantity and min stock level")
            return
        
        if expiry:
            try:
                datetime.strptime(expiry, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Validation", "Please enter a valid expiry date (YYYY-MM-DD)")
                return
        
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO blood_inventory (blood_type, quantity, min_stock_level, expiry_date, storage_location) VALUES (%s, %s, %s, %s, %s)",
                    (blood_type, quantity_int, min_stock_int, expiry if expiry else None, storage if storage else None)
                )
                conn.commit()
                messagebox.showinfo("Success", "Blood inventory item added successfully!")
                self.clear_form()
                self.load_inventory()
                cursor.close()
            except mysql.connector.IntegrityError:
                messagebox.showerror("Error", "This blood type already exists. Use Update Inventory instead.")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to add inventory: {str(e)}")
            finally:
                conn.close()
    
    def update_inventory(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Selection", "Please select an inventory item to update")
            return
        
        inventory_id = self.tree.item(selection[0])['values'][0]
        blood_type = self.blood_type_var.get()
        quantity = self.quantity_var.get().strip()
        min_stock = self.min_stock_var.get().strip()
        expiry = self.expiry_var.get().strip()
        storage = self.storage_var.get().strip()
        
        if not blood_type or not quantity or not min_stock:
            messagebox.showwarning("Validation", "Please fill in all required fields")
            return
        
        try:
            quantity_int = int(quantity)
            min_stock_int = int(min_stock)
        except ValueError:
            messagebox.showerror("Validation", "Please enter valid numbers for quantity and min stock level")
            return
        
        if expiry:
            try:
                datetime.strptime(expiry, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Validation", "Please enter a valid expiry date (YYYY-MM-DD)")
                return
        
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE blood_inventory SET blood_type=%s, quantity=%s, min_stock_level=%s, expiry_date=%s, storage_location=%s WHERE inventory_id=%s",
                    (blood_type, quantity_int, min_stock_int, expiry if expiry else None, storage if storage else None, inventory_id)
                )
                conn.commit()
                messagebox.showinfo("Success", "Blood inventory updated successfully!")
                self.clear_form()
                self.load_inventory()
                cursor.close()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to update inventory: {str(e)}")
            finally:
                conn.close()
    
    def clear_form(self):
        self.blood_type_combo.current(0)
        self.quantity_var.set("")
        self.min_stock_var.set("")
        self.expiry_var.set("")
        self.storage_var.set("")
        selection = self.tree.selection()
        if selection:
            self.tree.selection_remove(selection)
