import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random

# Constants for maximum and minimum values
VOLTAGE_MAX = 10.0
VOLTAGE_MIN = 0.0
CURRENT_MAX = 100.0
CURRENT_MIN = 0.0


# Functions to simulate setting and getting measurements from hardware
def simulate_hardware_interaction(channel, mode, set_value):
    # This function simulates interaction with the hardware by returning
    # pseudo-random but plausible values for measured voltage and current.
    if mode == "Voltage":
        # Simulate a voltage reading with some noise
        measured_voltage = set_value + random.uniform(-0.01, 0.01) * set_value
        measured_current = random.uniform(0, CURRENT_MAX / 10)  # Assume some baseline current
    else:
        # Simulate a current reading with some noise
        measured_current = set_value + random.uniform(-0.01, 0.01) * set_value
        measured_voltage = random.uniform(0, VOLTAGE_MAX / 10)  # Assume some baseline voltage

    return measured_voltage, measured_current


# Main GUI Setup
root = tk.Tk()
root.title("Qontrol GUI")

# Setup Treeview
tree = ttk.Treeview(root, columns=('Channel', 'Mode', 'Set Value', 'Measured Voltage (V)', 'Measured Current (mA)'),
                    show='headings')
tree.heading('Channel', text='Channel')
tree.heading('Mode', text='Mode (V/I)')
tree.heading('Set Value', text='Set Value')
tree.heading('Measured Voltage (V)', text='Measured Voltage (V)')
tree.heading('Measured Current (mA)', text='Measured Current (mA)')

# Insert initial data into Treeview
for i in range(8):
    tree.insert('', 'end', iid=i, values=(f"Channel {i}", "Voltage", VOLTAGE_MIN, 0.0, 0.0))

tree.pack(side=tk.TOP, fill=tk.X)

# Frame for controls
frame = tk.Frame(root)
frame.pack(side=tk.TOP, fill=tk.X)

# Channel selection
channel_label = ttk.Label(frame, text="Select Channel:")
channel_label.pack(side=tk.LEFT)
channel_var = tk.IntVar(value=0)
channel_combobox = ttk.Combobox(frame, textvariable=channel_var, values=[f"Channel {i}" for i in range(8)])
channel_combobox.pack(side=tk.LEFT)

# Mode selection
mode_label = ttk.Label(frame, text="Select Mode (V/I):")
mode_label.pack(side=tk.LEFT)
mode_var = tk.StringVar(value='Voltage')
mode_combobox = ttk.Combobox(frame, textvariable=mode_var, values=['Voltage', 'Current'])
mode_combobox.pack(side=tk.LEFT)

# Set value entry
set_value_label = ttk.Label(frame, text="Set Value:")
set_value_label.pack(side=tk.LEFT)
set_value_var = tk.DoubleVar(value=VOLTAGE_MIN)
set_value_entry = ttk.Entry(frame, textvariable=set_value_var)
set_value_entry.pack(side=tk.LEFT)


# Button to set value
def apply_settings():
    channel = int(channel_combobox.get().split()[-1])
    mode = mode_combobox.get()
    set_value = set_value_var.get()

    if (mode == 'Voltage' and VOLTAGE_MIN <= set_value <= VOLTAGE_MAX) or (
            mode == 'Current' and CURRENT_MIN <= set_value <= CURRENT_MAX):
        measured_voltage, measured_current = simulate_hardware_interaction(channel, mode, set_value)
        tree.item(channel, values=(f"Channel {channel}", mode, set_value, measured_voltage, measured_current))
    else:
        messagebox.showwarning("Range Error", "Value out of allowed range.")


set_button = ttk.Button(frame, text="Set", command=apply_settings)
set_button.pack(side=tk.LEFT)

root.mainloop()


