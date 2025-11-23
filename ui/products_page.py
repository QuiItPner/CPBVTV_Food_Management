import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from config import COLORS, FONTS, TABLE_CONFIG
from .dialogs import ItemDialog

class ProductsPage:
    def __init__(self, root, data_manager, on_back):
        self.root = root
        self.data_manager = data_manager
        self.on_back = on_back
        self.tree = None
        self.tree_fruits = None
        self.title_var = None
        self.images = {}
        
        self._load_images()
        self._create_page()
    
    def _load_images(self):
        self.product_header_images = []
        self.fruit_header_images = []
        
        products_dir = os.path.join("images", "products")
        fruits_dir = os.path.join("images", "fruits")
        
        if os.path.exists(products_dir):
            for filename in os.listdir(products_dir)[:3]:
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    filepath = os.path.join(products_dir, filename)
                    try:
                        img = Image.open(filepath)
                        img = img.resize((40, 40), Image.Resampling.LANCZOS)
                        self.product_header_images.append(ImageTk.PhotoImage(img))
                    except:
                        pass
        
        if os.path.exists(fruits_dir):
            for filename in os.listdir(fruits_dir)[:3]:
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    filepath = os.path.join(fruits_dir, filename)
                    try:
                        img = Image.open(filepath)
                        img = img.resize((40, 40), Image.Resampling.LANCZOS)
                        self.fruit_header_images.append(ImageTk.PhotoImage(img))
                    except:
                        pass
    
    def _create_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        main_frame = tk.Frame(self.root, bg=COLORS['white'])
        main_frame.pack(expand=True, fill='both')
        
        self._create_header(main_frame)
        self._create_toolbar(main_frame)
        self._create_tables(main_frame)
        
        self.load_products()
        self.load_fruits()
    
    def _create_header(self, parent):
        header_frame = tk.Frame(parent, bg=COLORS['primary'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        self.title_var = tk.StringVar(value=self.data_manager.get_page_title())
        
        title_label = tk.Label(
            header_frame,
            textvariable=self.title_var,
            font=FONTS['header'],
            bg=COLORS['primary'],
            fg=COLORS['white']
        )
        title_label.pack(pady=15)
        
        back_btn = tk.Button(
            header_frame,
            text="Quay lại",
            font=FONTS['small'],
            bg=COLORS['primary_dark'],
            fg=COLORS['white'],
            command=self.on_back
        )
        back_btn.place(relx=0.05, rely=0.5, anchor='w')
    
    def _create_toolbar(self, parent):
        toolbar_frame = tk.Frame(parent, bg=COLORS['light_bg'], height=60)
        toolbar_frame.pack(fill='x')
        toolbar_frame.pack_propagate(False)
        
        left_toolbar = tk.Frame(toolbar_frame, bg=COLORS['light_bg'])
        left_toolbar.pack(side='left', padx=10, pady=15)
        
        tk.Label(
            left_toolbar, 
            text="Nông sản:", 
            font=FONTS['small_bold'], 
            bg=COLORS['light_bg']
        ).pack(side='left', padx=5)
        
        tk.Button(
            left_toolbar,
            text="➕ Thêm",
            font=FONTS['small_bold'],
            bg=COLORS['success'],
            fg=COLORS['white'],
            width=10,
            command=self.add_product
        ).pack(side='left', padx=3)
        
        tk.Button(
            left_toolbar,
            text="✎ Sửa",
            font=FONTS['small_bold'],
            bg=COLORS['warning'],
            fg=COLORS['white'],
            width=10,
            command=self.edit_product
        ).pack(side='left', padx=3)
        
        tk.Button(
            left_toolbar,
            text="🗑 Xóa",
            font=FONTS['small_bold'],
            bg=COLORS['danger'],
            fg=COLORS['white'],
            width=10,
            command=self.delete_product
        ).pack(side='left', padx=3)
        
        right_toolbar = tk.Frame(toolbar_frame, bg=COLORS['light_bg'])
        right_toolbar.pack(side='right', padx=10, pady=15)
        
        tk.Button(
            right_toolbar,
            text="🗑 Xóa",
            font=FONTS['small_bold'],
            bg=COLORS['danger'],
            fg=COLORS['white'],
            width=10,
            command=self.delete_fruit
        ).pack(side='right', padx=3)
        
        tk.Button(
            right_toolbar,
            text="✎ Sửa",
            font=FONTS['small_bold'],
            bg=COLORS['warning'],
            fg=COLORS['white'],
            width=10,
            command=self.edit_fruit
        ).pack(side='right', padx=3)
        
        tk.Button(
            right_toolbar,
            text="➕ Thêm",
            font=FONTS['small_bold'],
            bg=COLORS['success'],
            fg=COLORS['white'],
            width=10,
            command=self.add_fruit
        ).pack(side='right', padx=3)
        
        tk.Label(
            right_toolbar, 
            text="Trái cây:", 
            font=FONTS['small_bold'], 
            bg=COLORS['light_bg']
        ).pack(side='right', padx=5)
    
    def _create_tables(self, parent):
        container_frame = tk.Frame(parent, bg=COLORS['white'])
        container_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        left_frame = tk.Frame(container_frame, bg=COLORS['white'])
        left_frame.pack(side='left', expand=True, fill='both', padx=(0, 5))
        
        header_left = tk.Frame(left_frame, bg='#e8f5e9', relief='solid', borderwidth=1)
        header_left.pack(pady=(0, 10), fill='x', padx=2)
        
        if self.product_header_images:
            for img in self.product_header_images:
                img_label = tk.Label(header_left, image=img, bg='#e8f5e9')
                img_label.pack(side='left', padx=5, pady=8)
        else:
            tk.Label(
                header_left,
                text="🥩🥬",
                font=('Arial', 24),
                bg='#e8f5e9'
            ).pack(side='left', padx=10, pady=8)
        
        tk.Label(
            header_left,
            text="THỰC PHẨM",
            font=FONTS['section'],
            bg='#e8f5e9',
            fg='#2e7d32'
        ).pack(side='left', pady=8, padx=10)
        
        search_frame = tk.Frame(left_frame, bg=COLORS['light_bg'])
        search_frame.pack(pady=(0, 5), fill='x', padx=2)
        
        tk.Label(
            search_frame,
            text="Tìm kiếm:",
            font=FONTS['small_bold'],
            bg=COLORS['light_bg']
        ).pack(side='left', padx=5, pady=5)
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=FONTS['normal'],
            width=25
        )
        self.search_entry.pack(side='left', padx=5, pady=5)
        
        tk.Button(
            search_frame,
            text="Tìm",
            font=FONTS['small_bold'],
            bg=COLORS['primary'],
            fg=COLORS['white'],
            width=8,
            command=self.search_products
        ).pack(side='left', padx=3, pady=5)
        
        tk.Button(
            search_frame,
            text="Đặt lại",
            font=FONTS['small_bold'],
            bg=COLORS['secondary'],
            fg=COLORS['white'],
            width=8,
            command=self.reset_products
        ).pack(side='left', padx=3, pady=5)
        
        self.tree = self._create_tree(left_frame)
        
        right_frame = tk.Frame(container_frame, bg=COLORS['white'])
        right_frame.pack(side='right', expand=True, fill='both', padx=(5, 0))
        
        header_right = tk.Frame(right_frame, bg='#fff3e0', relief='solid', borderwidth=1)
        header_right.pack(pady=(0, 10), fill='x', padx=2)
        
        if self.fruit_header_images:
            for img in self.fruit_header_images:
                img_label = tk.Label(header_right, image=img, bg='#fff3e0')
                img_label.pack(side='left', padx=5, pady=8)
        else:
            tk.Label(
                header_right,
                text="🍎🍊",
                font=('Arial', 24),
                bg='#fff3e0'
            ).pack(side='left', padx=10, pady=8)
        
        tk.Label(
            header_right,
            text="TRÁI CÂY",
            font=FONTS['section'],
            bg='#fff3e0',
            fg='#e65100'
        ).pack(side='left', pady=8, padx=10)
        
        search_frame_fruits = tk.Frame(right_frame, bg=COLORS['light_bg'])
        search_frame_fruits.pack(pady=(0, 5), fill='x', padx=2)
        
        tk.Label(
            search_frame_fruits,
            text="Tìm kiếm:",
            font=FONTS['small_bold'],
            bg=COLORS['light_bg']
        ).pack(side='left', padx=5, pady=5)
        
        self.search_fruits_var = tk.StringVar()
        self.search_fruits_entry = tk.Entry(
            search_frame_fruits,
            textvariable=self.search_fruits_var,
            font=FONTS['normal'],
            width=25
        )
        self.search_fruits_entry.pack(side='left', padx=5, pady=5)
        
        tk.Button(
            search_frame_fruits,
            text="Tìm",
            font=FONTS['small_bold'],
            bg=COLORS['primary'],
            fg=COLORS['white'],
            width=8,
            command=self.search_fruits
        ).pack(side='left', padx=3, pady=5)
        
        tk.Button(
            search_frame_fruits,
            text="Đặt lại",
            font=FONTS['small_bold'],
            bg=COLORS['secondary'],
            fg=COLORS['white'],
            width=8,
            command=self.reset_fruits
        ).pack(side='left', padx=3, pady=5)
        
        self.tree_fruits = self._create_tree(right_frame)
    
    def _create_tree(self, parent):
        table_frame = tk.Frame(parent, bg=COLORS['white'])
        table_frame.pack(expand=True, fill='both')
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Treeview",
            background=COLORS['white'],
            foreground="black",
            rowheight=TABLE_CONFIG['row_height'],
            fieldbackground=COLORS['white'],
            font=FONTS['table']
        )
        style.configure(
            "Treeview.Heading",
            font=FONTS['table_header'],
            background=COLORS['darker'],
            foreground=COLORS['white'],
            relief='flat'
        )
        style.map('Treeview', background=[('selected', COLORS['primary'])])
        
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical')
        scrollbar.pack(side='right', fill='y')
        
        tree = ttk.Treeview(
            table_frame,
            columns=('STT', 'TenHang', 'DVT', 'DonGia'),
            show='headings',
            yscrollcommand=scrollbar.set
        )
        
        scrollbar.config(command=tree.yview)
        
        tree.heading('STT', text='STT', anchor='w')
        tree.heading('TenHang', text='TÊN HÀNG', anchor='w')
        tree.heading('DVT', text='ĐVT', anchor='w')
        tree.heading('DonGia', text='Đơn giá', anchor='w')
        
        widths = TABLE_CONFIG['column_widths']
        tree.column('STT', width=widths['STT'], anchor='w', stretch=False)
        tree.column('TenHang', width=widths['TenHang'], anchor='w', stretch=False)
        tree.column('DVT', width=widths['DVT'], anchor='w', stretch=False)
        tree.column('DonGia', width=widths['DonGia'], anchor='w', stretch=False)
        
        tree.pack(expand=True, fill='both')
        
        tree.tag_configure('oddrow', background=COLORS['row_odd'])
        tree.tag_configure('evenrow', background=COLORS['row_even'])
        
        return tree
    
    def load_products(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            rows = self.data_manager.load_data("Products")
            for idx, row in enumerate(rows):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                don_gia_formatted = f"{float(row[3]):,.0f}".replace(',', '.')
                self.tree.insert('', 'end', values=(row[0], row[1], row[2], don_gia_formatted), tags=(tag,))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {str(e)}")
    
    def load_fruits(self):
        for item in self.tree_fruits.get_children():
            self.tree_fruits.delete(item)
        
        try:
            rows = self.data_manager.load_data("Fruits")
            for idx, row in enumerate(rows):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                don_gia_formatted = f"{float(row[3]):,.0f}".replace(',', '.')
                self.tree_fruits.insert('', 'end', values=(row[0], row[1], row[2], don_gia_formatted), tags=(tag,))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu trái cây: {str(e)}")
    
    def search_products(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        search_text = self.search_var.get().strip().lower()
        
        if not search_text:
            self.load_products()
            return
        
        try:
            rows = self.data_manager.load_data("Products")
            filtered_rows = []
            
            for row in rows:
                ten_hang = str(row[1]).lower()
                don_gia = float(row[3])
                
                match = False
                
                if search_text in ten_hang:
                    match = True
                
                try:
                    search_price = float(search_text.replace('.', '').replace(',', ''))
                    if abs(don_gia - search_price) < 0.01:
                        match = True
                except:
                    pass
                
                if match:
                    filtered_rows.append(row)
            
            if filtered_rows:
                for idx, row in enumerate(filtered_rows):
                    tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                    don_gia_formatted = f"{float(row[3]):,.0f}".replace(',', '.')
                    self.tree.insert('', 'end', values=(row[0], row[1], row[2], don_gia_formatted), tags=(tag,))
            else:
                messagebox.showinfo("Thông báo", f"Không tìm thấy kết quả cho '{search_text}'")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm kiếm: {str(e)}")
    
    def reset_products(self):
        self.search_var.set('')
        self.load_products()
    
    def reset_fruits(self):
        self.search_fruits_var.set('')
        self.load_fruits()
    
    def search_fruits(self):
        for item in self.tree_fruits.get_children():
            self.tree_fruits.delete(item)
        
        search_text = self.search_fruits_var.get().strip().lower()
        
        if not search_text:
            self.load_fruits()
            return
        
        try:
            rows = self.data_manager.load_data("Fruits")
            filtered_rows = []
            
            for row in rows:
                ten_hang = str(row[1]).lower()
                don_gia = float(row[3])
                
                match = False
                
                if search_text in ten_hang:
                    match = True
                
                try:
                    search_price = float(search_text.replace('.', '').replace(',', ''))
                    if abs(don_gia - search_price) < 0.01:
                        match = True
                except:
                    pass
                
                if match:
                    filtered_rows.append(row)
            
            if filtered_rows:
                for idx, row in enumerate(filtered_rows):
                    tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                    don_gia_formatted = f"{float(row[3]):,.0f}".replace(',', '.')
                    self.tree_fruits.insert('', 'end', values=(row[0], row[1], row[2], don_gia_formatted), tags=(tag,))
            else:
                messagebox.showinfo("Thông báo", f"Không tìm thấy kết quả cho '{search_text}'")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm kiếm: {str(e)}")
    
    def add_product(self):
        def save_callback(name, unit, price):
            try:
                self.data_manager.add_item("Products", name, unit, price)
                messagebox.showinfo("Thành công", "Đã thêm mặt hàng!")
                self.load_products()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể thêm: {str(e)}")
        
        ItemDialog(self.root, self.data_manager, "Thêm mặt hàng mới", callback=save_callback)
    
    def edit_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn mặt hàng cần sửa!")
            return
        
        item = self.tree.item(selected[0])
        values = item['values']
        
        def update_callback(name, unit, price):
            try:
                self.data_manager.update_item("Products", values[0], name, unit, price)
                messagebox.showinfo("Thành công", "Đã cập nhật mặt hàng!")
                self.load_products()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật: {str(e)}")
        
        ItemDialog(self.root, self.data_manager, "Sửa mặt hàng", initial_values=values, callback=update_callback)
    
    def delete_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn mặt hàng cần xóa!")
            return
        
        item = self.tree.item(selected[0])
        values = item['values']
        
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa '{values[1]}'?")
        
        if confirm:
            try:
                self.data_manager.delete_item("Products", values[0])
                messagebox.showinfo("Thành công", "Đã xóa mặt hàng!")
                self.load_products()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa: {str(e)}")
    
    def add_fruit(self):
        def save_callback(name, unit, price):
            try:
                self.data_manager.add_item("Fruits", name, unit, price)
                messagebox.showinfo("Thành công", "Đã thêm trái cây!")
                self.load_fruits()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể thêm: {str(e)}")
        
        ItemDialog(self.root, self.data_manager, "Thêm trái cây mới", callback=save_callback)
    
    def edit_fruit(self):
        selected = self.tree_fruits.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn trái cây cần sửa!")
            return
        
        item = self.tree_fruits.item(selected[0])
        values = item['values']
        
        def update_callback(name, unit, price):
            try:
                self.data_manager.update_item("Fruits", values[0], name, unit, price)
                messagebox.showinfo("Thành công", "Đã cập nhật trái cây!")
                self.load_fruits()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật: {str(e)}")
        
        ItemDialog(self.root, self.data_manager, "Sửa trái cây", initial_values=values, callback=update_callback)
    
    def delete_fruit(self):
        selected = self.tree_fruits.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn trái cây cần xóa!")
            return
        
        item = self.tree_fruits.item(selected[0])
        values = item['values']
        
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa '{values[1]}'?")
        
        if confirm:
            try:
                self.data_manager.delete_item("Fruits", values[0])
                messagebox.showinfo("Thành công", "Đã xóa trái cây!")
                self.load_fruits()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa: {str(e)}")
