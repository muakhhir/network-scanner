import socket
import threading
import ipaddress
import tkinter as tk
from tkinter import scrolledtext, messagebox

def scan_ip(ip, ports=[80, 443, 22, 21, 3389]):
    found_services = []
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((str(ip), port))
            if result == 0:
                found_services.append(port)
            sock.close()
        except:
            pass
    return found_services

def start_scan():
    output_text.delete(1.0, tk.END)  # Clear previous output
    network = entry_network.get()
    try:
        ip_net = ipaddress.ip_network(network, strict=False)
    except ValueError:
        messagebox.showerror("Error", "Invalid network address.")
        return

    def scan_network():
        for ip in ip_net.hosts():
            services = scan_ip(ip)
            if services:
                output_text.insert(tk.END, f"IP: {ip} | Open ports: {services}\n")
            else:
                output_text.insert(tk.END, f"IP: {ip} | No common ports open\n")
            output_text.see(tk.END)  # Scroll down as text comes in

    threading.Thread(target=scan_network).start()

# GUI setup
window = tk.Tk()
window.title("Simple Network Scanner")
window.geometry("600x400")

label_network = tk.Label(window, text="Enter Network (e.g., 192.168.1.0/24):")
label_network.pack(pady=5)

entry_network = tk.Entry(window, width=30)
entry_network.pack(pady=5)

scan_button = tk.Button(window, text="Start Scan", command=start_scan)
scan_button.pack(pady=5)

output_text = scrolledtext.ScrolledText(window, width=70, height=20)
output_text.pack(pady=10)

window.mainloop()
