import tkinter as tk
from tkinter import messagebox
from config import COLORS, FONTS

class ItemDialog:
    def __init__(self, parent, data_manager, title, initial_values=None, callback=None):
        self.data_manager = data_manager
        self.callback = callback
        self.initial_values = initial_values
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x250")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
    
    def _create_widgets(self):
        tk.Label(
            self.dialog, 
            text="Tên hàng:", 
            font=FONTS['normal']
        ).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        
        self.entry_name = tk.Entry(self.dialog, font=FONTS['normal'], width=30)
        self.entry_name.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(
            self.dialog, 
            text="ĐVT:", 
            font=FONTS['normal']
        ).grid(row=1, column=0, padx=10, pady=10, sticky='w')
        
        self.entry_unit = tk.Entry(self.dialog, font=FONTS['normal'], width=30)
        self.entry_unit.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(
            self.dialog, 
            text="Đơn giá:", 
            font=FONTS['normal']
        ).grid(row=2, column=0, padx=10, pady=10, sticky='w')
        
        self.entry_price = tk.Entry(self.dialog, font=FONTS['normal'], width=30)
        self.entry_price.grid(row=2, column=1, padx=10, pady=10)
        
        if self.initial_values:
            self.entry_name.insert(0, self.initial_values[1])
            self.entry_unit.insert(0, self.initial_values[2])
            self.entry_price.insert(0, str(self.initial_values[3]).replace('.', ''))
        
        btn_frame = tk.Frame(self.dialog)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        save_text = "Cập nhật" if self.initial_values else "Lưu"
        save_color = COLORS['warning'] if self.initial_values else COLORS['success']
        
        tk.Button(
            btn_frame,
            text=save_text,
            font=FONTS['button'],
            bg=save_color,
            fg='white',
            width=10,
            command=self._save
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="Hủy",
            font=FONTS['normal'],
            bg=COLORS['secondary'],
            fg='white',
            width=10,
            command=self.dialog.destroy
        ).pack(side='left', padx=5)
    
    def _save(self):
        name = self.entry_name.get().strip()
        unit = self.entry_unit.get().strip()
        price = self.entry_price.get().strip()
        
        if not name or not unit or not price:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")
            return
        
        try:
            price_float = float(price.replace(',', '.').replace(' ', ''))
        except:
            messagebox.showerror("Lỗi", "Đơn giá không hợp lệ!")
            return
        
        if self.callback:
            self.callback(name, unit, price_float)
        
        self.dialog.destroy()
