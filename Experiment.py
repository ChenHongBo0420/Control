import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import qontrol
# Assuming 'qontrol' is already imported and QXOutput class is available

# Constants for maximum and minimum values
VOLTAGE_MAX = 10.0
VOLTAGE_MIN = 0.0
CURRENT_MAX = 100.0
CURRENT_MIN = 0.0

# Setup Qontroller
serial_port_name = "COM3"
q = qontrol.QXOutput(serial_port_name=serial_port_name, response_timeout=0.1)


# Define the functions for setting and getting hardware values
def set_hardware_voltage(channel, voltage):
	q.v[channel] = voltage


def set_hardware_current(channel, current):
	q.i[channel] = current


def get_hardware_measured_voltage(channel):
	return q.v[channel]


def get_hardware_measured_current(channel):
	return q.i[channel]


# GUI setup
root = tk.Tk()
root.title("Qontrol GUI")

# Treeview setup for displaying channels and values
tree = ttk.Treeview(root, columns=('Channel', 'Mode', 'Set Value', 'Measured Voltage (V)', 'Measured Current (mA)'),
					show='headings')
for col in tree['columns']:
	tree.heading(col, text=col.replace('_', ' '))
	tree.column(col, width=100)

# Insert initial data into Treeview
for i in range(q.n_chs):
	tree.insert('', 'end', iid=i, values=(
	f"Channel {i}", "Voltage", VOLTAGE_MIN, get_hardware_measured_voltage(i), get_hardware_measured_current(i)))

tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Frame for controls
frame = tk.Frame(root)
frame.pack(side=tk.TOP, fill=tk.X)

# Channel selection
channel_label = ttk.Label(frame, text="Select Channel:")
channel_label.pack(side=tk.LEFT)
channel_var = tk.IntVar(value=0)
channel_combobox = ttk.Combobox(frame, textvariable=channel_var, values=[f"Channel {i}" for i in range(q.n_chs)])
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
	channel = channel_var.get()
	mode = mode_var.get()
	set_value = set_value_var.get()

	if mode == 'Voltage' and VOLTAGE_MIN <= set_value <= VOLTAGE_MAX:
		set_hardware_voltage(channel, set_value)
	elif mode == 'Current' and CURRENT_MIN <= set_value <= CURRENT_MAX:
		set_hardware_current(channel, set_value)
	else:
		messagebox.showwarning("Range Error", "Value out of allowed range.")

	# Update the measured values in the GUI
	measured_voltage = get_hardware_measured_voltage(channel)
	measured_current = get_hardware_measured_current(channel)
	tree.item(channel, values=(f"Channel {channel}", mode, set_value, measured_voltage, measured_current))


set_button = ttk.Button(frame, text="Set", command=apply_settings)
set_button.pack(side=tk.LEFT)

root.mainloop()

