import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector
from config import DB_CONFIG
from .base_page import BasePage


class RequestManagementPage(BasePage):
    def __init__(self, parent):
        super().__init__(
            parent,
            title="Request Management",
            subtitle="Process blood requests and transfusions",
        )
        
        main_container = ttk.Frame(self.scrollable_frame)
        main_container.grid(row=self.body_row, column=0, sticky="nsew")
        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        self.scrollable_frame.rowconfigure(self.body_row, weight=1)
        
        form_card = self.create_card(main_container, "Blood Request", "Enter request details below. Double-click a request to edit.")
        form_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        
        form_content = ttk.Frame(form_card)
        form_content.grid(row=2, column=0, sticky="ew", pady=(0, 0))
        form_content.columnconfigure(1, weight=1, minsize=150)
        
        ttk.Label(form_content, text="Requester Name *", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.requester_name_var = tk.StringVar()
        self.requester_name_entry = ttk.Entry(form_content, textvariable=self.requester_name_var, style="TEntry", font=("Segoe UI", 9))
        self.requester_name_entry.grid(row=0, column=1, padx=(0, 0), pady=(0, 6), sticky="ew", ipady=4)
        
        ttk.Label(form_content, text="Requester Type *", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.requester_type_var = tk.StringVar()
        self.requester_type_combo = ttk.Combobox(form_content, textvariable=self.requester_type_var, 
                                                 values=("Hospital", "Clinic", "Individual", "Other"),
                                                 state="readonly", style="TCombobox", font=("Segoe UI", 9))
        self.requester_type_combo.grid(row=1, column=1, padx=(0, 0), pady=(0, 6), sticky="ew", ipady=4)
        self.requester_type_combo.current(0)
        
        ttk.Label(form_content, text="Request Date *", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.request_date_var = tk.StringVar()
        self.request_date_entry = ttk.Entry(form_content, textvariable=self.request_date_var, style="TEntry", font=("Segoe UI", 9))
        self.request_date_entry.grid(row=2, column=1, padx=(0, 0), pady=(0, 6), sticky="ew", ipady=4)
        self.request_date_var.set(datetime.now().strftime("%Y-%m-%d"))
        ttk.Label(form_content, text="(YYYY-MM-DD)", style="Subtle.TLabel", font=("Segoe UI", 8)).grid(row=2, column=2, sticky="w", padx=(4, 0))
        
        ttk.Label(form_content, text="Blood Type *", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=3, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.blood_type_var = tk.StringVar()
        self.blood_type_combo = ttk.Combobox(form_content, textvariable=self.blood_type_var, 
                                           values=("A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"),
                                           state="readonly", style="TCombobox", font=("Segoe UI", 9))
        self.blood_type_combo.grid(row=3, column=1, padx=(0, 0), pady=(0, 6), sticky="ew", ipady=4)
        self.blood_type_combo.current(0)
        
        ttk.Label(form_content, text="Quantity *", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=4, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.quantity_var = tk.StringVar(value="1")
        self.quantity_entry = ttk.Entry(form_content, textvariable=self.quantity_var, style="TEntry", font=("Segoe UI", 9))
        self.quantity_entry.grid(row=4, column=1, padx=(0, 0), pady=(0, 6), sticky="ew", ipady=4)
        
        ttk.Label(form_content, text="Urgency Level *", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=5, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.urgency_var = tk.StringVar()
        self.urgency_combo = ttk.Combobox(form_content, textvariable=self.urgency_var, 
                                         values=("Normal", "Urgent", "Critical"),
                                         state="readonly", style="TCombobox", font=("Segoe UI", 9))
        self.urgency_combo.grid(row=5, column=1, padx=(0, 0), pady=(0, 6), sticky="ew", ipady=4)
        self.urgency_combo.current(0)
        
        ttk.Label(form_content, text="Patient Name", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=6, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.patient_name_var = tk.StringVar()
        self.patient_name_entry = ttk.Entry(form_content, textvariable=self.patient_name_var, style="TEntry", font=("Segoe UI", 9))
        self.patient_name_entry.grid(row=6, column=1, padx=(0, 0), pady=(0, 6), sticky="ew", ipady=4)
        
        ttk.Label(form_content, text="Hospital Name", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=7, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.hospital_var = tk.StringVar()
        self.hospital_entry = ttk.Entry(form_content, textvariable=self.hospital_var, style="TEntry", font=("Segoe UI", 9))
        self.hospital_entry.grid(row=7, column=1, padx=(0, 0), pady=(0, 6), sticky="ew", ipady=4)
        
        ttk.Label(form_content, text="Contact Number", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=8, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.contact_var = tk.StringVar()
        self.contact_entry = ttk.Entry(form_content, textvariable=self.contact_var, style="TEntry", font=("Segoe UI", 9))
        self.contact_entry.grid(row=8, column=1, padx=(0, 0), pady=(0, 6), sticky="ew", ipady=4)
        
        ttk.Label(form_content, text="Status *", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=9, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.status_var = tk.StringVar()
        self.status_combo = ttk.Combobox(form_content, textvariable=self.status_var, 
                                        values=("Pending", "Fulfilled", "Cancelled"),
                                        state="readonly", style="TCombobox", font=("Segoe UI", 9))
        self.status_combo.grid(row=9, column=1, padx=(0, 0), pady=(0, 6), sticky="ew", ipady=4)
        self.status_combo.current(0)
        
        ttk.Label(form_content, text="Notes", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=10, column=0, sticky="nw", padx=(0, 8), pady=(0, 4))
        self.notes_text = tk.Text(form_content, font=("Segoe UI", 9), width=25, height=2, wrap=tk.WORD, relief="solid", bd=1, padx=6, pady=6)
        self.notes_text.grid(row=10, column=1, padx=(0, 0), pady=(0, 10), sticky="ew")
        
        button_frame = ttk.Frame(form_card)
        button_frame.grid(row=3, column=0, sticky="ew", pady=(6, 0))
        button_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform="buttons")
        
        ttk.Button(button_frame, text="Add Request", style="Accent.TButton", command=self.add_request).grid(row=0, column=0, sticky="ew", padx=(0, 4), ipady=6)
        ttk.Button(button_frame, text="Update Request", style="Outline.TButton", command=self.update_request).grid(row=0, column=1, sticky="ew", padx=(0, 4), ipady=6)
        ttk.Button(button_frame, text="Fulfill Request", style="Outline.TButton", command=self.fulfill_request).grid(row=0, column=2, sticky="ew", padx=(0, 4), ipady=6)
        ttk.Button(button_frame, text="Clear", style="Outline.TButton", command=self.clear_form).grid(row=0, column=3, sticky="ew", ipady=6)
        
        list_card = self.create_card(main_container, "Blood Requests List", "Double-click a request to edit. Red indicates urgent/critical requests.")
        list_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        list_card.rowconfigure(2, weight=1)
        
        search_frame = ttk.Frame(list_card)
        search_frame.grid(row=2, column=0, sticky="ew", pady=(0, 8), padx=0)
        search_frame.columnconfigure(1, weight=1)
        
        ttk.Label(search_frame, text="Search:", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 8), pady=6)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, style="TEntry", font=("Segoe UI", 9))
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=(0, 0), pady=6, ipady=4)
        self.search_entry.bind("<KeyRelease>", self.filter_requests)
        
        tree_frame = ttk.Frame(list_card)
        tree_frame.grid(row=3, column=0, sticky="nsew", padx=0, pady=(0, 0))
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        
        columns = ("ID", "Requester", "Date", "Blood Type", "Quantity", "Urgency", "Status")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "Requester":
                self.tree.column(col, width=100, anchor="w")
            elif col in ("Date", "Status"):
                self.tree.column(col, width=80, anchor="center")
            else:
                self.tree.column(col, width=70, anchor="center")
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.tree.bind("<Double-1>", self.on_request_select)
        
        self.load_requests()
    
    def get_db_connection(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            return conn
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {str(e)}")
            return None
    
    def load_requests(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT request_id, requester_name, request_date, blood_type, quantity, urgency_level, status FROM blood_requests ORDER BY request_date DESC, request_id DESC")
                rows = cursor.fetchall()
                
                for row in rows:
                    request_date = row[2].strftime("%Y-%m-%d") if row[2] else ""
                    urgency = row[5]
                    tag = "Urgent" if urgency in ("Urgent", "Critical") else "Normal"
                    self.tree.insert("", tk.END, values=(
                        row[0], row[1], request_date, row[3], row[4], urgency, row[6]
                    ), tags=(tag,))
                
                self.tree.tag_configure("Urgent", background="#eeeeee")
                self.tree.tag_configure("Normal", background="#FFFFFF")
                
                cursor.close()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to load requests: {str(e)}")
            finally:
                conn.close()
    
    def filter_requests(self, event=None):
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
                        "SELECT request_id, requester_name, request_date, blood_type, quantity, urgency_level, status FROM blood_requests WHERE requester_name LIKE %s OR blood_type LIKE %s OR urgency_level LIKE %s OR status LIKE %s OR hospital_name LIKE %s OR patient_name LIKE %s OR CAST(request_date AS CHAR) LIKE %s ORDER BY request_date DESC, request_id DESC",
                        (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern, search_pattern, search_pattern)
                    )
                else:
                    cursor.execute("SELECT request_id, requester_name, request_date, blood_type, quantity, urgency_level, status FROM blood_requests ORDER BY request_date DESC, request_id DESC")
                
                rows = cursor.fetchall()
                
                for row in rows:
                    request_date = row[2].strftime("%Y-%m-%d") if row[2] else ""
                    urgency = row[5]
                    tag = "Urgent" if urgency in ("Urgent", "Critical") else "Normal"
                    self.tree.insert("", tk.END, values=(
                        row[0], row[1], request_date, row[3], row[4], urgency, row[6]
                    ), tags=(tag,))
                
                self.tree.tag_configure("Urgent", background="#eeeeee")
                self.tree.tag_configure("Normal", background="#FFFFFF")
                
                cursor.close()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to filter requests: {str(e)}")
            finally:
                conn.close()
    
    def on_request_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            conn = self.get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM blood_requests WHERE request_id=%s", (values[0],))
                    result = cursor.fetchone()
                    if result:
                        self.requester_name_var.set(result[1])
                        self.requester_type_var.set(result[2])
                        self.request_date_var.set(result[3].strftime("%Y-%m-%d") if result[3] else "")
                        self.blood_type_var.set(result[4])
                        self.quantity_var.set(str(result[5]))
                        self.urgency_var.set(result[6])
                        self.patient_name_var.set(result[7] if result[7] else "")
                        self.hospital_var.set(result[8] if result[8] else "")
                        self.contact_var.set(result[9] if result[9] else "")
                        self.status_var.set(result[10])
                        self.notes_text.delete(1.0, tk.END)
                        self.notes_text.insert(1.0, result[12] if result[12] else "")
                    cursor.close()
                except mysql.connector.Error:
                    pass
                finally:
                    conn.close()
    
    def add_request(self):
        requester_name = self.requester_name_var.get().strip()
        requester_type = self.requester_type_var.get()
        request_date = self.request_date_var.get().strip()
        blood_type = self.blood_type_var.get()
        quantity = self.quantity_var.get().strip()
        urgency = self.urgency_var.get()
        patient_name = self.patient_name_var.get().strip()
        hospital = self.hospital_var.get().strip()
        contact = self.contact_var.get().strip()
        status = self.status_var.get()
        notes = self.notes_text.get(1.0, tk.END).strip()
        
        if not requester_name or not request_date or not blood_type or not quantity:
            messagebox.showwarning("Validation", "Please fill in all required fields")
            return
        
        try:
            datetime.strptime(request_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Validation", "Please enter a valid request date (YYYY-MM-DD)")
            return
        
        try:
            quantity_int = int(quantity)
        except ValueError:
            messagebox.showerror("Validation", "Please enter a valid quantity")
            return
        
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO blood_requests (requester_name, requester_type, request_date, blood_type, quantity, urgency_level, patient_name, hospital_name, contact_number, status, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (requester_name, requester_type, request_date, blood_type, quantity_int, urgency, patient_name if patient_name else None, hospital if hospital else None, contact if contact else None, status, notes if notes else None)
                )
                conn.commit()
                messagebox.showinfo("Success", "Blood request added successfully!")
                self.clear_form()
                self.load_requests()
                cursor.close()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to add request: {str(e)}")
            finally:
                conn.close()
    
    def update_request(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Selection", "Please select a request to update")
            return
        
        request_id = self.tree.item(selection[0])['values'][0]
        requester_name = self.requester_name_var.get().strip()
        requester_type = self.requester_type_var.get()
        request_date = self.request_date_var.get().strip()
        blood_type = self.blood_type_var.get()
        quantity = self.quantity_var.get().strip()
        urgency = self.urgency_var.get()
        patient_name = self.patient_name_var.get().strip()
        hospital = self.hospital_var.get().strip()
        contact = self.contact_var.get().strip()
        status = self.status_var.get()
        notes = self.notes_text.get(1.0, tk.END).strip()
        
        if not requester_name or not request_date or not blood_type or not quantity:
            messagebox.showwarning("Validation", "Please fill in all required fields")
            return
        
        try:
            datetime.strptime(request_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Validation", "Please enter a valid request date (YYYY-MM-DD)")
            return
        
        try:
            quantity_int = int(quantity)
        except ValueError:
            messagebox.showerror("Validation", "Please enter a valid quantity")
            return
        
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE blood_requests SET requester_name=%s, requester_type=%s, request_date=%s, blood_type=%s, quantity=%s, urgency_level=%s, patient_name=%s, hospital_name=%s, contact_number=%s, status=%s, notes=%s WHERE request_id=%s",
                    (requester_name, requester_type, request_date, blood_type, quantity_int, urgency, patient_name if patient_name else None, hospital if hospital else None, contact if contact else None, status, notes if notes else None, request_id)
                )
                conn.commit()
                messagebox.showinfo("Success", "Blood request updated successfully!")
                self.clear_form()
                self.load_requests()
                cursor.close()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to update request: {str(e)}")
            finally:
                conn.close()
    
    def fulfill_request(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Selection", "Please select a request to fulfill")
            return
        
        request_id = self.tree.item(selection[0])['values'][0]
        
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT blood_type, quantity, status FROM blood_requests WHERE request_id=%s", (request_id,))
                request = cursor.fetchone()
                
                if not request:
                    messagebox.showerror("Error", "Request not found")
                    return
                
                if request[2] == "Fulfilled":
                    messagebox.showinfo("Info", "This request is already fulfilled")
                    return
                
                # Check inventory
                cursor.execute("SELECT quantity FROM blood_inventory WHERE blood_type=%s", (request[0],))
                inventory = cursor.fetchone()
                
                if not inventory or inventory[0] < request[1]:
                    messagebox.showwarning("Insufficient Stock", f"Not enough {request[0]} blood in inventory. Current stock: {inventory[0] if inventory else 0} units")
                    return
                
                # Update request status
                cursor.execute(
                    "UPDATE blood_requests SET status='Fulfilled', fulfilled_date=%s WHERE request_id=%s",
                    (datetime.now().date(), request_id)
                )
                
                # Update inventory
                cursor.execute(
                    "UPDATE blood_inventory SET quantity = quantity - %s WHERE blood_type = %s",
                    (request[1], request[0])
                )
                
                conn.commit()
                messagebox.showinfo("Success", "Blood request fulfilled successfully!")
                self.load_requests()
                cursor.close()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to fulfill request: {str(e)}")
            finally:
                conn.close()
    
    def clear_form(self):
        self.requester_name_var.set("")
        self.requester_type_combo.current(0)
        self.request_date_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.blood_type_combo.current(0)
        self.quantity_var.set("1")
        self.urgency_combo.current(0)
        self.patient_name_var.set("")
        self.hospital_var.set("")
        self.contact_var.set("")
        self.status_combo.current(0)
        self.notes_text.delete(1.0, tk.END)
        selection = self.tree.selection()
        if selection:
            self.tree.selection_remove(selection)

