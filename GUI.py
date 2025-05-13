import tkinter as tk
from tkinter import messagebox
import joblib
import pandas as pd
from generate_sensor_data import generate_data
import time

class SensorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SIMATIC HMI - Sensor Monitoring Panel")
        self.root.geometry("1000x600")
        self.root.config(bg="#D3D3D3")

        self.model = joblib.load("sensor_model.pkl")

        # Top title
        self.title_label = tk.Label(root, text="Sensor Data Monitoring System", font=("Arial", 24, "bold"), fg="black", bg="#D3D3D3")
        self.title_label.pack(pady=10)

        # Center panel
        self.center_frame = tk.Frame(root, bg="#D3D3D3")
        self.center_frame.pack(side="left", fill="both", expand=True, padx=20)

        # Right panel (buttons)
        self.right_frame = tk.Frame(root, bg="#B0BEC5")
        self.right_frame.pack(side="right", fill="y")

        # Sensor information
        self.sensor_distance_label = tk.Label(self.center_frame, text="Sensor Distance (cm): 0", font=("Arial", 16), fg="black", bg="#D3D3D3")
        self.sensor_distance_label.pack(pady=5)

        self.pressure_label = tk.Label(self.center_frame, text="Pressure (kPa): 0.00", font=("Arial", 16), fg="black", bg="#D3D3D3")
        self.pressure_label.pack(pady=5)

        self.status_label = tk.Label(self.center_frame, text="Status: Running", font=("Arial", 16), fg="green", bg="#D3D3D3")
        self.status_label.pack(pady=5)

        self.count_label = tk.Label(self.center_frame, text="Box Counter: 0", font=("Arial", 16), fg="black", bg="#D3D3D3")
        self.count_label.pack(pady=5)

        self.error_label = tk.Label(self.center_frame, text="Error Status: None", font=("Arial", 14), fg="red", bg="#D3D3D3")
        self.error_label.pack(pady=5)

        # New LED indicators
        self.led_canvas = tk.Canvas(self.center_frame, width=200, height=100, bg="#D3D3D3", bd=0, highlightthickness=0)
        self.led_canvas.pack(pady=20)

        # LED Circles for Machine, Pressure, and Distance
        self.machine_led = self.led_canvas.create_oval(20, 20, 60, 60, fill="green")  # Initial green (Machine)
        self.pressure_led = self.led_canvas.create_oval(80, 20, 120, 60, fill="green")  # Initial green (Pressure)
        self.distance_led = self.led_canvas.create_oval(140, 20, 180, 60, fill="green")  # Initial green (Distance)

        # List of erroneous data (larger size)
        self.error_listbox = tk.Listbox(self.center_frame, height=15, width=60, font=("Arial", 12))
        self.error_listbox.pack(pady=10)

        # Buttons on the right
        button_style = {"font": ("Arial", 14), "width": 18, "height": 2, "bg": "#CFD8DC", "fg": "black", "bd": 2}

        self.start_button = tk.Button(self.right_frame, text="Start Data Stream", command=self.start_data_stream, **button_style)
        self.start_button.pack(pady=10)

        self.continue_button = tk.Button(self.right_frame, text="Continue", command=self.continue_data_stream, **button_style)
        self.continue_button.pack(pady=10)

        self.reset_button = tk.Button(self.right_frame, text="Reset System", command=self.reset_system, **button_style)
        self.reset_button.pack(pady=10)

        self.save_button = tk.Button(self.right_frame, text="Save Erroneous Data", command=self.save_error_data, **button_style)
        self.save_button.pack(pady=10)

        # New buttons: Shutdown Machine and Exit Program
        self.shutdown_button = tk.Button(self.right_frame, text="Shutdown Machine", command=self.shutdown_machine, **button_style)
        self.shutdown_button.pack(pady=10)

        self.exit_button = tk.Button(self.right_frame, text="Exit Program", command=self.exit_program, **button_style)
        self.exit_button.pack(pady=10)

        # Display user name at the bottom
        self.name_label = tk.Label(self.center_frame, text="Mahmut Esat Kolay", font=("Arial", 12), fg="black", bg="#D3D3D3")
        self.name_label.pack(side="bottom", pady=10)

        self.is_streaming = False
        self.count = 0
        self.error_count = 0
        self.current_index = 0
        self.data_stream()

    def data_stream(self):
        if self.is_streaming:
            df = generate_data(1)
            sensor_distance = df.iloc[0]["sensor_distance"]
            pressure = df.iloc[0]["pressure"]

            # Model ile tahmin yap
            prediction = self.model.predict([[sensor_distance, pressure]])  # Modelin tahminini al

            data_index = self.current_index + 1

            self.sensor_distance_label.config(text=f"Sensor Distance (cm): {sensor_distance:.2f}")
            self.pressure_label.config(text=f"Pressure (kPa): {pressure:.2f}")

            # Makine durumu LED
            if prediction == 1:  # Hatalı veri
                self.status_label.config(text="Status: Erroneous Data", fg="red")
                self.led_canvas.itemconfig(self.machine_led, fill="red")
                self.error_label.config(text=f"Index: {data_index} - Error: Box Distance {sensor_distance:.2f} cm!", fg="red")
                self.is_streaming = False
                self.error_count += 1
                self.count_label.config(text=f"Box Counter: {self.count}")
                self.error_listbox.insert(tk.END, f"Index: {data_index} - Error: Box Distance {sensor_distance:.2f} cm!")
                messagebox.showwarning("Erroneous Data", f"Box Distance {sensor_distance:.2f} cm is erroneous! Data stream stopped.")
            else:
                self.status_label.config(text="Status: Running", fg="green")
                self.led_canvas.itemconfig(self.machine_led, fill="green")

            # Basınç sensörü LED
            if pressure < 20:  # Örnek olarak basınç 20'den küçükse hata
                self.led_canvas.itemconfig(self.pressure_led, fill="red")
                self.error_label.config(text=f"Pressure Error: {pressure:.2f} kPa!", fg="red")
            else:
                self.led_canvas.itemconfig(self.pressure_led, fill="green")

            # Mesafe sensörü LED
            if sensor_distance > 100:  # Örnek olarak mesafe 100'den büyükse hata
                self.led_canvas.itemconfig(self.distance_led, fill="red")
                self.error_label.config(text=f"Distance Error: {sensor_distance:.2f} cm!", fg="red")
            else:
                self.led_canvas.itemconfig(self.distance_led, fill="green")

            self.count += 1
            self.count_label.config(text=f"Box Counter: {self.count}")
            self.current_index = data_index

        self.root.after(1000, self.data_stream)

    def start_data_stream(self):
        self.is_streaming = True
        self.status_label.config(text="Status: Running", fg="green")
        self.count = 0
        self.error_count = 0
        self.count_label.config(text=f"Box Counter: {self.count}")
        self.error_label.config(text="Error Status: None", fg="green")
        self.error_listbox.delete(0, tk.END)
        self.current_index = 0

    def continue_data_stream(self):
        self.is_streaming = True
        self.status_label.config(text="Status: Running", fg="green")
        self.count_label.config(text=f"Box Counter: {self.count}")
        self.error_label.config(text="Error Status: None", fg="green")

    def reset_system(self):
        self.is_streaming = False
        self.status_label.config(text="Status: Running", fg="green")
        self.count = 0
        self.error_count = 0
        self.count_label.config(text=f"Box Counter: {self.count}")
        self.error_label.config(text="Error Status: None", fg="green")
        self.sensor_distance_label.config(text="Sensor Distance (cm): 0")
        self.pressure_label.config(text="Pressure (kPa): 0.00")
        self.error_listbox.delete(0, tk.END)

    def save_error_data(self):
        if self.error_listbox.size() > 0:
            error_data = [self.error_listbox.get(i) for i in range(self.error_listbox.size())]
            df = pd.DataFrame(error_data, columns=["Erroneous Data"])
            df.to_excel("erroneous_data.xlsx", index=False)
            self.error_listbox.delete(0, tk.END)
            messagebox.showinfo("Success", "Erroneous data successfully saved.")
        else:
            messagebox.showwarning("Warning", "No erroneous data to save.")

    def shutdown_machine(self):
        self.is_streaming = False
        self.status_label.config(text="Status: Machine Off", fg="red")
        self.count_label.config(text=f"Box Counter: {self.count}")
        self.error_label.config(text="Error Status: None", fg="green")
        messagebox.showinfo("Machine Shutdown", "Machine has been successfully shut down.")

    def exit_program(self):
        self.status_label.config(text="Program is closing...", fg="black")
        self.root.after(2000, self.quit_program)

    def quit_program(self):
        self.root.quit()

def main():
    root = tk.Tk()
    app = SensorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
