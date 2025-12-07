import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector
from config import DB_CONFIG
from .base_page import BasePage


class DonationManagementPage(BasePage):
    def __init__(self, parent):
        super().__init__(
            parent,
            title="Donation Management",
            subtitle="Record and track blood donations",
        )
        
        main_container = ttk.Frame(self.scrollable_frame)
        main_container.grid(row=self.body_row, column=0, sticky="nsew")
        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        self.scrollable_frame.rowconfigure(self.body_row, weight=1)
        
        form_card = self.create_card(main_container, "Record Blood Donation", "Enter donation details below.")
        form_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        
        form_content = ttk.Frame(form_card)
        form_content.grid(row=2, column=0, sticky="ew", pady=(0, 0))
        form_content.columnconfigure(1, weight=1, minsize=150)
        
        ttk.Label(form_content, text="Donor *", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.donor_var = tk.StringVar()
        self.donor_combo = ttk.Combobox(form_content, textvariable=self.donor_var, state="readonly", style="TCombobox", font=("Segoe UI", 9))
        self.donor_combo.grid(row=0, column=1, padx=(0, 0), pady=(0, 6), sticky="ew", ipady=4)
        self.load_donors()
        
        ttk.Label(form_content, text="Donation Date *", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.donation_date_var = tk.StringVar()
        self.donation_date_entry = ttk.Entry(form_content, textvariable=self.donation_date_var, style="TEntry", font=("Segoe UI", 9))
        self.donation_date_entry.grid(row=1, column=1, padx=(0, 0), pady=(0, 6), sticky="ew", ipady=4)
        self.donation_date_var.set(datetime.now().strftime("%Y-%m-%d"))
        ttk.Label(form_content, text="(YYYY-MM-DD)", style="Subtle.TLabel", font=("Segoe UI", 8)).grid(row=1, column=2, sticky="w", padx=(4, 0))
        
        ttk.Label(form_content, text="Blood Type *", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.blood_type_var = tk.StringVar()
        self.blood_type_combo = ttk.Combobox(form_content, textvariable=self.blood_type_var, 
                                           values=("A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"),
                                           state="readonly", style="TCombobox", font=("Segoe UI", 9))
        self.blood_type_combo.grid(row=2, column=1, padx=(0, 0), pady=(0, 6), sticky="ew", ipady=4)
        self.blood_type_combo.current(0)
        
        ttk.Label(form_content, text="Quantity *", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=3, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.quantity_var = tk.StringVar(value="1")
        self.quantity_entry = ttk.Entry(form_content, textvariable=self.quantity_var, style="TEntry", font=("Segoe UI", 9))
        self.quantity_entry.grid(row=3, column=1, padx=(0, 0), pady=(0, 6), sticky="ew", ipady=4)
        
        ttk.Label(form_content, text="Collection Location", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=4, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.location_var = tk.StringVar()
        self.location_entry = ttk.Entry(form_content, textvariable=self.location_var, style="TEntry", font=("Segoe UI", 9))
        self.location_entry.grid(row=4, column=1, padx=(0, 0), pady=(0, 6), sticky="ew", ipady=4)
        
        ttk.Label(form_content, text="Staff Name", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=5, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.staff_var = tk.StringVar()
        self.staff_entry = ttk.Entry(form_content, textvariable=self.staff_var, style="TEntry", font=("Segoe UI", 9))
        self.staff_entry.grid(row=5, column=1, padx=(0, 0), pady=(0, 6), sticky="ew", ipady=4)
        
        ttk.Label(form_content, text="Notes", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=6, column=0, sticky="nw", padx=(0, 8), pady=(0, 4))
        self.notes_text = tk.Text(form_content, font=("Segoe UI", 9), width=25, height=3, wrap=tk.WORD, relief="solid", bd=1, padx=6, pady=6)
        self.notes_text.grid(row=6, column=1, padx=(0, 0), pady=(0, 10), sticky="ew")
        
        button_frame = ttk.Frame(form_card)
        button_frame.grid(row=3, column=0, sticky="ew", pady=(6, 0))
        button_frame.columnconfigure((0, 1, 2), weight=1, uniform="buttons")
        
        ttk.Button(button_frame, text="Record Donation", style="Accent.TButton", command=self.record_donation).grid(row=0, column=0, sticky="ew", padx=(0, 4), ipady=6)
        ttk.Button(button_frame, text="Delete Donation", style="Outline.TButton", command=self.delete_donation).grid(row=0, column=1, sticky="ew", padx=(0, 4), ipady=6)
        ttk.Button(button_frame, text="Clear", style="Outline.TButton", command=self.clear_form).grid(row=0, column=2, sticky="ew", ipady=6)
        
        list_card = self.create_card(main_container, "Donations History", "View all recorded blood donations.")
        list_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        list_card.rowconfigure(2, weight=1)
        
        search_frame = ttk.Frame(list_card)
        search_frame.grid(row=2, column=0, sticky="ew", pady=(0, 8), padx=0)
        search_frame.columnconfigure(1, weight=1)
        
        ttk.Label(search_frame, text="Search:", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 8), pady=6)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, style="TEntry", font=("Segoe UI", 9))
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=(0, 0), pady=6, ipady=4)
        self.search_entry.bind("<KeyRelease>", self.filter_donations)
        
        tree_frame = ttk.Frame(list_card)
        tree_frame.grid(row=3, column=0, sticky="nsew", padx=0, pady=(0, 0))
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        
        columns = ("ID", "Donor", "Date", "Blood Type", "Quantity", "Location")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "Donor":
                self.tree.column(col, width=120, anchor="w")
            elif col == "Location":
                self.tree.column(col, width=100, anchor="w")
            elif col == "Date":
                self.tree.column(col, width=90, anchor="center")
            else:
                self.tree.column(col, width=70, anchor="center")
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.tree.bind("<Double-1>", self.on_donation_select)
        
        self.load_donations()
    
    def get_db_connection(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            return conn
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {str(e)}")
            return None
    
    def load_donors(self):
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT donor_id, full_name FROM donors WHERE eligibility_status = 'Eligible' ORDER BY full_name")
                rows = cursor.fetchall()
                donor_list = [f"{row[0]} - {row[1]}" for row in rows]
                self.donor_combo['values'] = donor_list
                if donor_list:
                    self.donor_combo.current(0)
                cursor.close()
            except mysql.connector.Error:
                pass
            finally:
                conn.close()
    
    def load_donations(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT d.donation_id, don.full_name, d.donation_date, d.blood_type, d.quantity, d.collection_location
                    FROM donations d
                    JOIN donors don ON d.donor_id = don.donor_id
                    ORDER BY d.donation_date DESC, d.donation_id DESC
                """)
                rows = cursor.fetchall()
                
                for row in rows:
                    donation_date = row[2].strftime("%Y-%m-%d") if row[2] else ""
                    location = row[5] if row[5] else "N/A"
                    self.tree.insert("", tk.END, values=(
                        row[0], row[1], donation_date, row[3], row[4], location
                    ))
                
                cursor.close()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to load donations: {str(e)}")
            finally:
                conn.close()
    
    def filter_donations(self, event=None):
        search_term = self.search_var.get().strip()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                if search_term:
                    search_pattern = f"%{search_term}%"
                    cursor.execute("""
                        SELECT d.donation_id, don.full_name, d.donation_date, d.blood_type, d.quantity, d.collection_location
                        FROM donations d
                        JOIN donors don ON d.donor_id = don.donor_id
                        WHERE don.full_name LIKE %s OR d.blood_type LIKE %s OR d.collection_location LIKE %s OR CAST(d.donation_date AS CHAR) LIKE %s
                        ORDER BY d.donation_date DESC, d.donation_id DESC
                    """, (search_pattern, search_pattern, search_pattern, search_pattern))
                else:
                    cursor.execute("""
                        SELECT d.donation_id, don.full_name, d.donation_date, d.blood_type, d.quantity, d.collection_location
                        FROM donations d
                        JOIN donors don ON d.donor_id = don.donor_id
                        ORDER BY d.donation_date DESC, d.donation_id DESC
                    """)
                
                rows = cursor.fetchall()
                
                for row in rows:
                    donation_date = row[2].strftime("%Y-%m-%d") if row[2] else ""
                    location = row[5] if row[5] else "N/A"
                    self.tree.insert("", tk.END, values=(
                        row[0], row[1], donation_date, row[3], row[4], location
                    ))
                
                cursor.close()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to filter donations: {str(e)}")
            finally:
                conn.close()
    
    def on_donation_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            conn = self.get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM donations WHERE donation_id=%s", (values[0],))
                    result = cursor.fetchone()
                    if result:
                        donor_id = result[1]
                        donor_list = self.donor_combo['values']
                        for donor in donor_list:
                            if donor.startswith(f"{donor_id} -"):
                                self.donor_var.set(donor)
                                break
                        self.donation_date_var.set(result[2].strftime("%Y-%m-%d") if result[2] else "")
                        self.blood_type_var.set(result[3])
                        self.quantity_var.set(str(result[4]))
                        self.location_var.set(result[6] if result[6] else "")
                        self.staff_var.set(result[7] if result[7] else "")
                        self.notes_text.delete(1.0, tk.END)
                        self.notes_text.insert(1.0, result[8] if result[8] else "")
                    cursor.close()
                except mysql.connector.Error:
                    pass
                finally:
                    conn.close()
    
    def record_donation(self):
        donor_str = self.donor_var.get()
        donation_date = self.donation_date_var.get().strip()
        blood_type = self.blood_type_var.get()
        quantity = self.quantity_var.get().strip()
        location = self.location_var.get().strip()
        staff = self.staff_var.get().strip()
        notes = self.notes_text.get(1.0, tk.END).strip()
        
        if not donor_str or not donation_date or not blood_type or not quantity:
            messagebox.showwarning("Validation", "Please fill in all required fields")
            return
        
        try:
            donor_id = int(donor_str.split(" -")[0])
        except (ValueError, IndexError):
            messagebox.showerror("Validation", "Please select a valid donor")
            return
        
        try:
            datetime.strptime(donation_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Validation", "Please enter a valid donation date (YYYY-MM-DD)")
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
                    "INSERT INTO donations (donor_id, donation_date, blood_type, quantity, collection_location, staff_name, notes) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (donor_id, donation_date, blood_type, quantity_int, location if location else None, staff if staff else None, notes if notes else None)
                )
                
                # Update donor's last donation date
                cursor.execute(
                    "UPDATE donors SET last_donation_date = %s WHERE donor_id = %s",
                    (donation_date, donor_id)
                )
                
                # Update blood inventory
                cursor.execute(
                    "UPDATE blood_inventory SET quantity = quantity + %s WHERE blood_type = %s",
                    (quantity_int, blood_type)
                )
                
                conn.commit()
                messagebox.showinfo("Success", "Blood donation recorded successfully!")
                self.clear_form()
                self.load_donations()
                cursor.close()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to record donation: {str(e)}")
            finally:
                conn.close()
    
    def delete_donation(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Selection", "Please select a donation to delete")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this donation?"):
            return
        
        donation_id = self.tree.item(selection[0])['values'][0]
        
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # Get donation details before deleting
                cursor.execute("SELECT blood_type, quantity FROM donations WHERE donation_id=%s", (donation_id,))
                donation = cursor.fetchone()
                
                cursor.execute("DELETE FROM donations WHERE donation_id=%s", (donation_id,))
                
                # Update blood inventory
                if donation:
                    cursor.execute(
                        "UPDATE blood_inventory SET quantity = GREATEST(0, quantity - %s) WHERE blood_type = %s",
                        (donation[1], donation[0])
                    )
                
                conn.commit()
                messagebox.showinfo("Success", "Donation deleted successfully!")
                self.clear_form()
                self.load_donations()
                cursor.close()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to delete donation: {str(e)}")
            finally:
                conn.close()
    
    def clear_form(self):
        self.load_donors()
        self.donation_date_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.blood_type_combo.current(0)
        self.quantity_var.set("1")
        self.location_var.set("")
        self.staff_var.set("")
        self.notes_text.delete(1.0, tk.END)
        selection = self.tree.selection()
        if selection:
            self.tree.selection_remove(selection)

