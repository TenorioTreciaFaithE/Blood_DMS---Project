import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector
from config import DB_CONFIG
from .base_page import BasePage


class DonorManagementPage(BasePage):
    def __init__(self, parent):
        super().__init__(
            parent,
            title="Donor Management",
            subtitle="Register, update, and manage donor information",
        )
        
        main_container = ttk.Frame(self.scrollable_frame)
        main_container.grid(row=self.body_row, column=0, sticky="nsew")
        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        self.scrollable_frame.rowconfigure(self.body_row, weight=1)
        
        form_card = self.create_card(main_container, "Add/Edit Donor", "Enter donor details below. Double-click a donor in the list to edit.")
        form_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        
        form_content = ttk.Frame(form_card)
        form_content.grid(row=2, column=0, sticky="ew", pady=(0, 0))
        form_content.columnconfigure(1, weight=1, minsize=150)
        
        ttk.Label(form_content, text="Full Name *", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(form_content, textvariable=self.name_var, style="TEntry", font=("Segoe UI", 9))
        self.name_entry.grid(row=0, column=1, padx=(0, 0), pady=(0, 6), sticky="ew", ipady=4)
        
        ttk.Label(form_content, text="Date of Birth *", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.dob_var = tk.StringVar()
        self.dob_entry = ttk.Entry(form_content, textvariable=self.dob_var, style="TEntry", font=("Segoe UI", 9))
        self.dob_entry.grid(row=1, column=1, padx=(0, 0), pady=(0, 6), sticky="ew", ipady=4)
        ttk.Label(form_content, text="(YYYY-MM-DD)", style="Subtle.TLabel", font=("Segoe UI", 8)).grid(row=1, column=2, sticky="w", padx=(4, 0))
        
        ttk.Label(form_content, text="Gender *", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.gender_var = tk.StringVar()
        self.gender_combo = ttk.Combobox(form_content, textvariable=self.gender_var, 
                                        values=("Male", "Female", "Other"),
                                        state="readonly", style="TCombobox", font=("Segoe UI", 9))
        self.gender_combo.grid(row=2, column=1, padx=(0, 0), pady=(0, 6), sticky="ew", ipady=4)
        self.gender_combo.current(0)
        
        ttk.Label(form_content, text="Blood Type *", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=3, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.blood_type_var = tk.StringVar()
        self.blood_type_combo = ttk.Combobox(form_content, textvariable=self.blood_type_var, 
                                            values=("A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"),
                                            state="readonly", style="TCombobox", font=("Segoe UI", 9))
        self.blood_type_combo.grid(row=3, column=1, padx=(0, 0), pady=(0, 6), sticky="ew", ipady=4)
        self.blood_type_combo.current(0)
        
        ttk.Label(form_content, text="Phone Number", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=4, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.phone_var = tk.StringVar()
        self.phone_entry = ttk.Entry(form_content, textvariable=self.phone_var, style="TEntry", font=("Segoe UI", 9))
        self.phone_entry.grid(row=4, column=1, padx=(0, 0), pady=(0, 6), sticky="ew", ipady=4)
        
        ttk.Label(form_content, text="Email", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=5, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(form_content, textvariable=self.email_var, style="TEntry", font=("Segoe UI", 9))
        self.email_entry.grid(row=5, column=1, padx=(0, 0), pady=(0, 6), sticky="ew", ipady=4)
        
        ttk.Label(form_content, text="Address", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=6, column=0, sticky="nw", padx=(0, 8), pady=(0, 4))
        self.address_text = tk.Text(form_content, font=("Segoe UI", 9), width=25, height=2, wrap=tk.WORD, relief="solid", bd=1, padx=6, pady=6)
        self.address_text.grid(row=6, column=1, padx=(0, 0), pady=(0, 6), sticky="ew")
        
        ttk.Label(form_content, text="Eligibility Status *", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=7, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.eligibility_var = tk.StringVar()
        self.eligibility_combo = ttk.Combobox(form_content, textvariable=self.eligibility_var, 
                                             values=("Eligible", "Not Eligible", "Temporarily Deferred"),
                                             state="readonly", style="TCombobox", font=("Segoe UI", 9))
        self.eligibility_combo.grid(row=7, column=1, padx=(0, 0), pady=(0, 6), sticky="ew", ipady=4)
        self.eligibility_combo.current(0)
        
        ttk.Label(form_content, text="Last Donation Date", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=8, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.last_donation_var = tk.StringVar()
        self.last_donation_entry = ttk.Entry(form_content, textvariable=self.last_donation_var, style="TEntry", font=("Segoe UI", 9))
        self.last_donation_entry.grid(row=8, column=1, padx=(0, 0), pady=(0, 6), sticky="ew", ipady=4)
        ttk.Label(form_content, text="(YYYY-MM-DD)", style="Subtle.TLabel", font=("Segoe UI", 8)).grid(row=8, column=2, sticky="w", padx=(4, 0))
        
        ttk.Label(form_content, text="Notes", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=9, column=0, sticky="nw", padx=(0, 8), pady=(0, 4))
        self.notes_text = tk.Text(form_content, font=("Segoe UI", 9), width=25, height=2, wrap=tk.WORD, relief="solid", bd=1, padx=6, pady=6)
        self.notes_text.grid(row=9, column=1, padx=(0, 0), pady=(0, 10), sticky="ew")
        
        button_frame = ttk.Frame(form_card)
        button_frame.grid(row=3, column=0, sticky="ew", pady=(6, 0))
        button_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform="buttons")
        
        ttk.Button(button_frame, text="Add Donor", style="Accent.TButton", command=self.add_donor).grid(row=0, column=0, sticky="ew", padx=(0, 4), ipady=6)
        ttk.Button(button_frame, text="Update Donor", style="Outline.TButton", command=self.update_donor).grid(row=0, column=1, sticky="ew", padx=(0, 4), ipady=6)
        ttk.Button(button_frame, text="Delete Donor", style="Outline.TButton", command=self.delete_donor).grid(row=0, column=2, sticky="ew", padx=(0, 4), ipady=6)
        ttk.Button(button_frame, text="Clear", style="Outline.TButton", command=self.clear_form).grid(row=0, column=3, sticky="ew", ipady=6)
        
        list_card = self.create_card(main_container, "Donors List", "Double-click a donor to edit. Use search to filter donors.")
        list_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        list_card.rowconfigure(2, weight=1)
        
        search_frame = ttk.Frame(list_card)
        search_frame.grid(row=2, column=0, sticky="ew", pady=(0, 8), padx=0)
        search_frame.columnconfigure(1, weight=1)
        
        ttk.Label(search_frame, text="Search:", style="Label.TLabel", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 8), pady=6)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, style="TEntry", font=("Segoe UI", 9))
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=(0, 0), pady=6, ipady=4)
        self.search_entry.bind("<KeyRelease>", self.filter_donors)
        
        tree_frame = ttk.Frame(list_card)
        tree_frame.grid(row=3, column=0, sticky="nsew", padx=0, pady=(0, 0))
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        
        columns = ("ID", "Name", "Blood Type", "Gender", "Eligibility", "Last Donation")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "Name":
                self.tree.column(col, width=120, anchor="w")
            elif col == "Last Donation":
                self.tree.column(col, width=100, anchor="center")
            else:
                self.tree.column(col, width=80, anchor="center")
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.tree.bind("<Double-1>", self.on_donor_select)
        
        self.load_donors()
    
    def get_db_connection(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            return conn
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {str(e)}")
            return None
    
    def load_donors(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT donor_id, full_name, blood_type, gender, eligibility_status, last_donation_date FROM donors ORDER BY donor_id")
                rows = cursor.fetchall()
                
                for row in rows:
                    last_donation = row[5].strftime("%Y-%m-%d") if row[5] else "Never"
                    self.tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4], last_donation))
                
                cursor.close()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to load donors: {str(e)}")
            finally:
                conn.close()
    
    def filter_donors(self, event=None):
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
                        "SELECT donor_id, full_name, blood_type, gender, eligibility_status, last_donation_date FROM donors WHERE full_name LIKE %s OR blood_type LIKE %s OR gender LIKE %s OR eligibility_status LIKE %s OR phone_number LIKE %s OR email LIKE %s ORDER BY donor_id",
                        (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern, search_pattern)
                    )
                else:
                    cursor.execute("SELECT donor_id, full_name, blood_type, gender, eligibility_status, last_donation_date FROM donors ORDER BY donor_id")
                
                rows = cursor.fetchall()
                
                for row in rows:
                    last_donation = row[5].strftime("%Y-%m-%d") if row[5] else "Never"
                    self.tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4], last_donation))
                
                cursor.close()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to filter donors: {str(e)}")
            finally:
                conn.close()
    
    def on_donor_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            conn = self.get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM donors WHERE donor_id=%s", (values[0],))
                    result = cursor.fetchone()
                    if result:
                        self.name_var.set(result[1])
                        self.dob_var.set(result[2].strftime("%Y-%m-%d") if result[2] else "")
                        self.gender_var.set(result[3])
                        self.blood_type_var.set(result[4])
                        self.phone_var.set(result[5] if result[5] else "")
                        self.email_var.set(result[6] if result[6] else "")
                        self.address_text.delete(1.0, tk.END)
                        self.address_text.insert(1.0, result[7] if result[7] else "")
                        self.eligibility_var.set(result[8])
                        self.last_donation_var.set(result[9].strftime("%Y-%m-%d") if result[9] else "")
                        self.notes_text.delete(1.0, tk.END)
                        self.notes_text.insert(1.0, result[10] if result[10] else "")
                    cursor.close()
                except mysql.connector.Error:
                    pass
                finally:
                    conn.close()
    
    def add_donor(self):
        name = self.name_var.get().strip()
        dob = self.dob_var.get().strip()
        gender = self.gender_var.get()
        blood_type = self.blood_type_var.get()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        address = self.address_text.get(1.0, tk.END).strip()
        eligibility = self.eligibility_var.get()
        last_donation = self.last_donation_var.get().strip()
        notes = self.notes_text.get(1.0, tk.END).strip()
        
        if not name or not dob or not gender or not blood_type:
            messagebox.showwarning("Validation", "Please fill in all required fields (Name, Date of Birth, Gender, Blood Type)")
            return
        
        try:
            datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Validation", "Please enter a valid date of birth (YYYY-MM-DD)")
            return
        
        if last_donation:
            try:
                datetime.strptime(last_donation, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Validation", "Please enter a valid last donation date (YYYY-MM-DD)")
                return
        
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO donors (full_name, date_of_birth, gender, blood_type, phone_number, email, address, eligibility_status, last_donation_date, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (name, dob, gender, blood_type, phone if phone else None, email if email else None, address if address else None, eligibility, last_donation if last_donation else None, notes if notes else None)
                )
                conn.commit()
                messagebox.showinfo("Success", "Donor added successfully!")
                self.clear_form()
                self.load_donors()
                cursor.close()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to add donor: {str(e)}")
            finally:
                conn.close()
    
    def update_donor(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Selection", "Please select a donor to update")
            return
        
        donor_id = self.tree.item(selection[0])['values'][0]
        name = self.name_var.get().strip()
        dob = self.dob_var.get().strip()
        gender = self.gender_var.get()
        blood_type = self.blood_type_var.get()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        address = self.address_text.get(1.0, tk.END).strip()
        eligibility = self.eligibility_var.get()
        last_donation = self.last_donation_var.get().strip()
        notes = self.notes_text.get(1.0, tk.END).strip()
        
        if not name or not dob or not gender or not blood_type:
            messagebox.showwarning("Validation", "Please fill in all required fields")
            return
        
        try:
            datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Validation", "Please enter a valid date of birth (YYYY-MM-DD)")
            return
        
        if last_donation:
            try:
                datetime.strptime(last_donation, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Validation", "Please enter a valid last donation date (YYYY-MM-DD)")
                return
        
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE donors SET full_name=%s, date_of_birth=%s, gender=%s, blood_type=%s, phone_number=%s, email=%s, address=%s, eligibility_status=%s, last_donation_date=%s, notes=%s WHERE donor_id=%s",
                    (name, dob, gender, blood_type, phone if phone else None, email if email else None, address if address else None, eligibility, last_donation if last_donation else None, notes if notes else None, donor_id)
                )
                conn.commit()
                messagebox.showinfo("Success", "Donor updated successfully!")
                self.clear_form()
                self.load_donors()
                cursor.close()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to update donor: {str(e)}")
            finally:
                conn.close()
    
    def delete_donor(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Selection", "Please select a donor to delete")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this donor?"):
            return
        
        donor_id = self.tree.item(selection[0])['values'][0]
        
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM donors WHERE donor_id=%s", (donor_id,))
                conn.commit()
                messagebox.showinfo("Success", "Donor deleted successfully!")
                self.clear_form()
                self.load_donors()
                cursor.close()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to delete donor: {str(e)}")
            finally:
                conn.close()
    
    def clear_form(self):
        self.name_var.set("")
        self.dob_var.set("")
        self.gender_combo.current(0)
        self.blood_type_combo.current(0)
        self.phone_var.set("")
        self.email_var.set("")
        self.address_text.delete(1.0, tk.END)
        self.eligibility_combo.current(0)
        self.last_donation_var.set("")
        self.notes_text.delete(1.0, tk.END)
        selection = self.tree.selection()
        if selection:
            self.tree.selection_remove(selection)

