import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import mysql.connector
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from config import DB_CONFIG
from .base_page import BasePage


class DashboardPage(BasePage):
    def __init__(self, parent):
        super().__init__(
            parent,
            title="Dashboard",
            subtitle="Overview of blood donation system statistics",
        )
        
        # Statistics cards row
        stats_container = ttk.Frame(self.scrollable_frame)
        stats_container.grid(row=self.body_row, column=0, sticky="ew", pady=(0, 10))
        stats_container.columnconfigure((0, 1, 2, 3), weight=1)
        
        self.create_stat_card(stats_container, "Total Donors", self.get_total_donors(), 0)
        self.create_stat_card(stats_container, "Total Donations", self.get_total_donations(), 1)
        self.create_stat_card(stats_container, "Pending Requests", self.get_pending_requests(), 2)
        self.create_stat_card(stats_container, "Low Stock Types", self.get_low_stock_count(), 3)
        
        # Graphs row 1
        graphs_row1 = ttk.Frame(self.scrollable_frame)
        graphs_row1.grid(row=self.body_row + 1, column=0, sticky="ew", pady=(0, 10))
        graphs_row1.columnconfigure(0, weight=1)
        graphs_row1.columnconfigure(1, weight=1)
        
        # Blood Inventory Chart
        inventory_card = self.create_card(graphs_row1, "Blood Inventory by Type", "Current stock levels for each blood type")
        inventory_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self.create_inventory_chart(inventory_card)
        
        # Donations Over Time Chart
        donations_card = self.create_card(graphs_row1, "Donations Over Time", "Last 30 days donation trend")
        donations_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        self.create_donations_chart(donations_card)
        
        # Graphs row 2
        graphs_row2 = ttk.Frame(self.scrollable_frame)
        graphs_row2.grid(row=self.body_row + 2, column=0, sticky="ew", pady=(0, 10))
        graphs_row2.columnconfigure(0, weight=1)
        graphs_row2.columnconfigure(1, weight=1)
        
        # Request Status Chart
        requests_card = self.create_card(graphs_row2, "Request Status Distribution", "Breakdown of blood requests by status")
        requests_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self.create_requests_chart(requests_card)
        
        # Donor Eligibility Chart
        eligibility_card = self.create_card(graphs_row2, "Donor Eligibility Status", "Distribution of donor eligibility")
        eligibility_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        self.create_eligibility_chart(eligibility_card)
        
        # Graphs row 3
        graphs_row3 = ttk.Frame(self.scrollable_frame)
        graphs_row3.grid(row=self.body_row + 3, column=0, sticky="ew")
        graphs_row3.columnconfigure(0, weight=1)
        
        # Blood Type Distribution Chart
        distribution_card = self.create_card(graphs_row3, "Blood Type Distribution", "Donations by blood type")
        distribution_card.grid(row=0, column=0, sticky="nsew")
        self.create_blood_type_distribution_chart(distribution_card)
    
    def create_stat_card(self, parent, title, value, column):
        card = ttk.Frame(parent, padding=12, style="Card.TFrame")
        card.grid(row=0, column=column, sticky="ew", padx=(0, 8) if column < 3 else (0, 0))
        
        title_label = ttk.Label(card, text=title, style="CardSubtitle.TLabel", font=("Segoe UI", 9))
        title_label.grid(row=0, column=0, sticky="w")
        
        value_label = ttk.Label(card, text=str(value), style="CardHeading.TLabel", font=("Segoe UI", 24, "bold"), foreground="#8B0000")
        value_label.grid(row=1, column=0, sticky="w", pady=(4, 0))
    
    def get_db_connection(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            return conn
        except mysql.connector.Error:
            return None
    
    def get_total_donors(self):
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM donors")
                result = cursor.fetchone()
                cursor.close()
                return result[0] if result else 0
            except:
                return 0
            finally:
                conn.close()
        return 0
    
    def get_total_donations(self):
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM donations")
                result = cursor.fetchone()
                cursor.close()
                return result[0] if result else 0
            except:
                return 0
            finally:
                conn.close()
        return 0
    
    def get_pending_requests(self):
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM blood_requests WHERE status = 'Pending'")
                result = cursor.fetchone()
                cursor.close()
                return result[0] if result else 0
            except:
                return 0
            finally:
                conn.close()
        return 0
    
    def get_low_stock_count(self):
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM blood_inventory WHERE quantity <= min_stock_level")
                result = cursor.fetchone()
                cursor.close()
                return result[0] if result else 0
            except:
                return 0
            finally:
                conn.close()
        return 0
    
    def create_inventory_chart(self, parent):
        conn = self.get_db_connection()
        blood_types = []
        quantities = []
        
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT blood_type, quantity FROM blood_inventory ORDER BY blood_type")
                rows = cursor.fetchall()
                for row in rows:
                    blood_types.append(row[0])
                    quantities.append(int(row[1]))
                cursor.close()
            except:
                pass
            finally:
                conn.close()
        
        fig = Figure(figsize=(5, 3), facecolor='white')
        ax = fig.add_subplot(111)
        
        colors = ['#DC143C' if q <= 10 else '#8B0000' for q in quantities]
        bars = ax.bar(blood_types, quantities, color=colors, alpha=0.8)
        ax.set_ylabel('Quantity (units)', fontsize=9)
        ax.set_title('Blood Inventory Levels', fontsize=10, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=8)
        
        fig.tight_layout(pad=1.5)
        
        chart_frame = ttk.Frame(parent)
        chart_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        parent.rowconfigure(2, weight=1)
        parent.columnconfigure(0, weight=1)
        
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        chart_frame.rowconfigure(0, weight=1)
        chart_frame.columnconfigure(0, weight=1)
    
    def create_donations_chart(self, parent):
        conn = self.get_db_connection()
        dates = []
        counts = []
        
        if conn:
            try:
                cursor = conn.cursor()
                # Get last 30 days
                end_date = datetime.now().date()
                start_date = end_date - timedelta(days=30)
                
                cursor.execute("""
                    SELECT DATE(donation_date) as date, COUNT(*) as count
                    FROM donations
                    WHERE donation_date >= %s AND donation_date <= %s
                    GROUP BY DATE(donation_date)
                    ORDER BY date
                """, (start_date, end_date))
                
                rows = cursor.fetchall()
                for row in rows:
                    dates.append(row[0].strftime('%m/%d'))
                    counts.append(row[1])
                cursor.close()
            except:
                pass
            finally:
                conn.close()
        
        if not dates:
            dates = [datetime.now().strftime('%m/%d')]
            counts = [0]
        
        fig = Figure(figsize=(5, 3), facecolor='white')
        ax = fig.add_subplot(111)
        
        ax.plot(dates, counts, marker='o', color='#8B0000', linewidth=2, markersize=4)
        ax.fill_between(dates, counts, alpha=0.3, color='#DC143C')
        ax.set_ylabel('Number of Donations', fontsize=9)
        ax.set_title('Donations Trend (Last 30 Days)', fontsize=10, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # Rotate x-axis labels if there are many dates
        if len(dates) > 7:
            step = max(1, len(dates)//7)
            tick_positions = range(0, len(dates), step)
            ax.set_xticks(tick_positions)
            ax.set_xticklabels([dates[i] for i in tick_positions], rotation=45, ha='right', fontsize=7)
        else:
            ax.set_xticks(range(len(dates)))
            ax.set_xticklabels(dates, rotation=45, ha='right', fontsize=7)
        
        fig.tight_layout(pad=1.5)
        
        chart_frame = ttk.Frame(parent)
        chart_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        parent.rowconfigure(2, weight=1)
        parent.columnconfigure(0, weight=1)
        
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        chart_frame.rowconfigure(0, weight=1)
        chart_frame.columnconfigure(0, weight=1)
    
    def create_requests_chart(self, parent):
        conn = self.get_db_connection()
        statuses = []
        counts = []
        
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT status, COUNT(*) as count
                    FROM blood_requests
                    GROUP BY status
                """)
                rows = cursor.fetchall()
                for row in rows:
                    statuses.append(row[0])
                    counts.append(row[1])
                cursor.close()
            except:
                pass
            finally:
                conn.close()
        
        if not statuses:
            statuses = ['Pending', 'Fulfilled', 'Cancelled']
            counts = [0, 0, 0]
        
        fig = Figure(figsize=(5, 3), facecolor='white')
        ax = fig.add_subplot(111)
        
        # Check if all counts are zero - pie chart can't handle this
        if sum(counts) == 0:
            ax.text(0.5, 0.5, 'No data available', 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=12, color='gray')
            ax.set_title('Request Status Distribution', fontsize=10, fontweight='bold')
        else:
            colors = ['#FFA500', '#32CD32', '#DC143C']  # Orange, Green, Red
            wedges, texts, autotexts = ax.pie(counts, labels=statuses, autopct='%1.1f%%',
                                              colors=colors[:len(statuses)], startangle=90,
                                              textprops={'fontsize': 9})
            ax.set_title('Request Status Distribution', fontsize=10, fontweight='bold')
        
        fig.tight_layout(pad=1.5)
        
        chart_frame = ttk.Frame(parent)
        chart_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        parent.rowconfigure(2, weight=1)
        parent.columnconfigure(0, weight=1)
        
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        chart_frame.rowconfigure(0, weight=1)
        chart_frame.columnconfigure(0, weight=1)
    
    def create_eligibility_chart(self, parent):
        conn = self.get_db_connection()
        eligibility = []
        counts = []
        
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT eligibility_status, COUNT(*) as count
                    FROM donors
                    GROUP BY eligibility_status
                """)
                rows = cursor.fetchall()
                for row in rows:
                    eligibility.append(row[0])
                    counts.append(row[1])
                cursor.close()
            except:
                pass
            finally:
                conn.close()
        
        if not eligibility:
            eligibility = ['Eligible', 'Not Eligible', 'Temporarily Deferred']
            counts = [0, 0, 0]
        
        fig = Figure(figsize=(5, 3), facecolor='white')
        ax = fig.add_subplot(111)
        
        colors = ['#32CD32', '#DC143C', '#FFA500']  # Green, Red, Orange
        bars = ax.barh(eligibility, counts, color=colors[:len(eligibility)], alpha=0.8)
        ax.set_xlabel('Number of Donors', fontsize=9)
        ax.set_title('Donor Eligibility Status', fontsize=10, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        
        # Add value labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2.,
                   f'{int(width)}',
                   ha='left', va='center', fontsize=8)
        
        fig.tight_layout(pad=1.5)
        
        chart_frame = ttk.Frame(parent)
        chart_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        parent.rowconfigure(2, weight=1)
        parent.columnconfigure(0, weight=1)
        
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        chart_frame.rowconfigure(0, weight=1)
        chart_frame.columnconfigure(0, weight=1)
    
    def create_blood_type_distribution_chart(self, parent):
        conn = self.get_db_connection()
        blood_types = []
        donation_counts = []
        
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT blood_type, COUNT(*) as count
                    FROM donations
                    GROUP BY blood_type
                    ORDER BY blood_type
                """)
                rows = cursor.fetchall()
                for row in rows:
                    blood_types.append(row[0])
                    donation_counts.append(row[1])
                cursor.close()
            except:
                pass
            finally:
                conn.close()
        
        if not blood_types:
            blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
            donation_counts = [0] * 8
        
        fig = Figure(figsize=(10, 3), facecolor='white')
        ax = fig.add_subplot(111)
        
        bars = ax.bar(blood_types, donation_counts, color='#8B0000', alpha=0.8)
        ax.set_ylabel('Number of Donations', fontsize=9)
        ax.set_title('Donations by Blood Type', fontsize=10, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontsize=8)
        
        fig.tight_layout(pad=1.5)
        
        chart_frame = ttk.Frame(parent)
        chart_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        parent.rowconfigure(2, weight=1)
        parent.columnconfigure(0, weight=1)
        
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        chart_frame.rowconfigure(0, weight=1)
        chart_frame.columnconfigure(0, weight=1)

