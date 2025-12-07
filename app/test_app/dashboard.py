import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from datetime import datetime, date
import decimal

# Attempt to import Matplotlib components
try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import numpy as np
except ImportError:
    # Set Figure to None if matplotlib is not installed
    Figure = None

# Assuming these are imported from your main module or are available globally
# Ensure services.py and queries.py are accessible
from services import get_connection
import queries as q 

class DashboardTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=5)
        self.pack(fill="both", expand=True)
        self.kpi_data = {}
        self.chart_data = None
        self.current_chart = "cost"  # 'cost' or 'sessions'
        
        # UI components
        self.kpi_text = None
        self.chart_canvas = None
        self.figure = None
        self.ax = None
        
        self.build_ui()
        # Initial data load
        self.refresh_dashboard()

    def build_ui(self):
        # --- Top Control Frame ---
        top = ttk.Frame(self, padding=8)
        top.pack(fill="x")
        ttk.Button(top, text="Refresh Dashboard", command=self.refresh_dashboard).pack(side="left")
        ttk.Button(top, text="Export KPIs CSV", command=self.export_kpi_csv).pack(side="left", padx=8)
        # Chart selection buttons
        chart_btn_frame = ttk.Frame(top)
        chart_btn_frame.pack(side="right")
        ttk.Button(chart_btn_frame, text="Original Graph", command=self.show_original_graph).pack(side="left", padx=4)
        ttk.Button(chart_btn_frame, text="Sessions Over Time", command=self.show_sessions_graph).pack(side="left", padx=4)

        # --- Body Frame (KPIs on Left, Chart on Right) ---
        body = ttk.Frame(self, padding=8)
        body.pack(fill="both", expand=True)
        
        # --- Left Panel: KPIs ---
        left = ttk.LabelFrame(body, text="Key Performance Indicators (KPIs)", padding=10)
        left.pack(side="left", fill="both", expand=False, padx=6, pady=6)
        
        self.kpi_text = tk.Text(left, width=45, height=10, state="disabled", padx=8, pady=8)
        self.kpi_text.pack(fill="both", expand=False)

        # --- Right Panel: Chart ---
        right = ttk.LabelFrame(body, text="Treatment Cost Distribution", padding=10)
        right.pack(side="right", fill="both", expand=True, padx=6, pady=6)

        # Chart area (matplotlib)
        if Figure is None:
            ttk.Label(right, text="matplotlib not installed - chart disabled").pack(pady=20)
            self.chart_canvas = None
        else:
            self.figure = Figure(figsize=(6,4), dpi=100)
            self.ax = self.figure.add_subplot(111)
            self.chart_canvas = FigureCanvasTkAgg(self.figure, master=right)
            self.chart_canvas.get_tk_widget().pack(fill="both", expand=True)


    def refresh_dashboard(self):
        """Fetches all KPI data and chart data from the database."""
        con = None
        try:
            con = get_connection()
            if not con: 
                messagebox.showerror("Connection Error", "Could not connect to database for dashboard.")
                return
            cur = con.cursor()
            
            # --- 1. Fetch KPIs ---
            cur.execute("SELECT COUNT(*) AS cnt FROM patients"); total_patients = cur.fetchone()["cnt"]
            cur.execute("SELECT COUNT(*) AS cnt FROM doctors"); total_doctors = cur.fetchone()["cnt"]
            cur.execute("SELECT COUNT(*) AS cnt FROM sessions"); total_sessions = cur.fetchone()["cnt"]
            cur.execute("SELECT AVG(cost) AS avgc FROM treatments"); avg_cost_r = cur.fetchone()["avgc"]
            avg_cost = float(avg_cost_r) if (avg_cost_r is not None) else 0.0
            cur.execute("SELECT COUNT(*) AS cnt FROM treatments WHERE cost > (SELECT AVG(cost) FROM treatments)")
            high_cost_treatments = cur.fetchone()["cnt"]
            
            # Store KPI data
            self.kpi_data = {
                "Total Patients": total_patients,
                "Total Doctors": total_doctors,
                "Total Sessions": total_sessions,
                "Average Treatment Cost": avg_cost,
                "High-Cost Treatments": high_cost_treatments
            }

            # Update KPI text widget
            txt = "\n".join([f"{k}: {v:,.2f}" if isinstance(v, float) else f"{k}: {v}" 
                             for k, v in self.kpi_data.items()])
                             
            self.kpi_text.configure(state="normal")
            self.kpi_text.delete("1.0", tk.END)
            self.kpi_text.insert(tk.END, txt)
            self.kpi_text.configure(state="disabled")

            # --- 2. Fetch Chart Data (Treatment Costs) ---
            if Figure is not None:
                cur.execute(q.Q_TREATMENT_COST_DISTRIBUTION)
                rows = cur.fetchall()
                # Ensure conversion to standard float type for plotting; query returns `cost`
                self.chart_data = [float(r.get('cost')) for r in rows if r.get('cost') is not None]
                # Draw the currently selected chart
                if self.current_chart == "cost":
                    self.draw_cost_distribution_chart()
                else:
                    # If sessions chart is selected, draw it after fetching data
                    self.draw_sessions_over_time_chart()
            
        except Exception as e:
            messagebox.showerror("Dashboard Error", f"Could not refresh dashboard: {e}")
        finally:
            if con: con.close()


    def draw_cost_distribution_chart(self):
        """Draws the histogram of treatment costs using matplotlib."""
        if self.chart_canvas is None: return

        self.ax.clear()
        
        if not self.chart_data:
            self.ax.text(0.5, 0.5, "No treatment cost data", ha="center")
        else:
            # Create a histogram for cost distribution
            # The 'bins' parameter determines the number of bars/categories
            self.ax.hist(self.chart_data, bins=10, edgecolor='black', alpha=0.7)
            self.ax.set_title("Distribution of Treatment Costs")
            self.ax.set_xlabel("Cost")
            self.ax.set_ylabel("Frequency")
        
        self.figure.tight_layout()
        self.chart_canvas.draw()


    def show_original_graph(self):
        """Switch to original treatment-cost distribution graph."""
        self.current_chart = "cost"
        # If we have cost data already, draw it, otherwise refresh to fetch
        if self.chart_data:
            self.draw_cost_distribution_chart()
        else:
            self.refresh_dashboard()


    def show_sessions_graph(self):
        """Switch to sessions-over-time graph and fetch data to display."""
        self.current_chart = "sessions"
        # Draw sessions chart (method fetches its own data)
        self.draw_sessions_over_time_chart()


    def draw_sessions_over_time_chart(self):
        """Queries sessions grouped by date and draws a time-series chart of counts."""
        if self.chart_canvas is None: return

        # Query DB for session counts by date
        try:
            con = get_connection()
            if not con:
                messagebox.showerror("Connection Error", "Could not connect to database for sessions chart.")
                return
            cur = con.cursor()
            cur.execute("SELECT treatment_date, COUNT(*) AS cnt FROM sessions WHERE treatment_date IS NOT NULL GROUP BY treatment_date ORDER BY treatment_date")
            rows = cur.fetchall()
            # rows expected as dict-like with keys 'treatment_date' and 'cnt'
            dates = []
            counts = []
            for r in rows:
                d = r.get('treatment_date') if isinstance(r, dict) else r[0]
                c = r.get('cnt') if isinstance(r, dict) else r[1]
                if d is None:
                    continue
                # Ensure date is a datetime/date object or parseable string
                if isinstance(d, str):
                    try:
                        d = datetime.fromisoformat(d).date()
                    except Exception:
                        try:
                            d = datetime.strptime(d, "%Y-%m-%d").date()
                        except Exception:
                            continue
                dates.append(d)
                counts.append(int(c))
        except Exception as e:
            messagebox.showerror("Sessions Chart Error", f"Could not load sessions data: {e}")
            return
        finally:
            try:
                if con: con.close()
            except Exception:
                pass

        # Draw
        self.ax.clear()
        if not dates:
            self.ax.text(0.5, 0.5, "No session data", ha="center")
        else:
            # Sort by date (should already be sorted by SQL) and plot
            # Convert dates to matplotlib-friendly values if necessary
            try:
                import matplotlib.dates as mdates
                self.ax.plot(dates, counts, marker='o')
                self.ax.set_title("Sessions Over Time")
                self.ax.set_xlabel("Date")
                self.ax.set_ylabel("Number of Sessions")
                self.ax.xaxis.set_major_locator(mdates.AutoDateLocator())
                self.ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(mdates.AutoDateLocator()))
            except Exception:
                # Fallback to bar chart with string labels
                labels = [d.strftime("%Y-%m-%d") if hasattr(d, 'strftime') else str(d) for d in dates]
                self.ax.bar(labels, counts)
                self.ax.set_title("Sessions Over Time")
                self.ax.set_xlabel("Date")
                self.ax.set_ylabel("Number of Sessions")

        self.figure.tight_layout()
        self.chart_canvas.draw()
        


    def export_kpi_csv(self):
        """Exports the current KPI values to a CSV file."""
        if not self.kpi_data:
            messagebox.showinfo("Export", "No KPI data to export")
            return
            
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if not path: return
            
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["Key Performance Indicator", "Value"])
                for k, v in self.kpi_data.items():
                    # Format float values for export
                    value = f"{v:,.2f}" if isinstance(v, float) else v
                    w.writerow([k, value])
            messagebox.showinfo("Exported", f"KPI saved to {path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Could not export CSV: {e}")