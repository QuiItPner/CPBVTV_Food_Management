import tkinter as tk
from tkinter import ttk, messagebox
from config import COLORS, FONTS, WINDOW_GEOMETRY, WINDOW_BG
from .products_page import ProductsPage
from .meal_registration_page import MealRegistrationPage
from PIL import Image, ImageTk
import os

class MainWindow:
    def __init__(self, root, data_manager):
        self.root = root
        self.data_manager = data_manager
        
        self.root.title("Quản Lý Thực Phẩm")
        self.root.geometry(WINDOW_GEOMETRY)
        self.root.configure(bg=WINDOW_BG)
        
        try:
            icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images", "app_icon.png")
            icon = Image.open(icon_path)
            icon_photo = ImageTk.PhotoImage(icon)
            self.root.iconphoto(True, icon_photo)
        except Exception as e:
            print(f"Could not load icon: {e}")
        
        self.show_main_menu()
    
    def lighten_color(self, hex_color, factor=0.2):
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = int(r + (255 - r) * factor)
        g = int(g + (255 - g) * factor)
        b = int(b + (255 - b) * factor)
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def bind_hover(self, button, original_color):
        hover_color = self.lighten_color(original_color)
        button.bind('<Enter>', lambda e: button.config(bg=hover_color))
        button.bind('<Leave>', lambda e: button.config(bg=original_color))
    
    def create_gradient(self, width, height, color1, color2):
        gradient = Image.new('RGB', (width, height), color1)
        draw = gradient.load()
        
        r1, g1, b1 = tuple(int(color1[i:i+2], 16) for i in (1, 3, 5))
        r2, g2, b2 = tuple(int(color2[i:i+2], 16) for i in (1, 3, 5))
        
        for y in range(height):
            ratio = y / height
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            for x in range(width):
                draw[x, y] = (r, g, b)
        
        return gradient
    
    def show_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        canvas = tk.Canvas(self.root, width=1200, height=700, highlightthickness=0)
        canvas.pack(expand=True, fill='both')
        
        gradient_img = self.create_gradient(1200, 700, '#0a734a', '#75be65')
        gradient_photo = ImageTk.PhotoImage(gradient_img)
        canvas.create_image(0, 0, anchor='nw', image=gradient_photo)
        canvas.image = gradient_photo
        
        try:
            images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images")
            fruits_dir = os.path.join(images_dir, "fruits")
            products_dir = os.path.join(images_dir, "products")
            
            banana_img = Image.open(os.path.join(fruits_dir, "banana.png"))
            banana_img = banana_img.resize((80, 80), Image.Resampling.LANCZOS)
            banana_photo = ImageTk.PhotoImage(banana_img)
            
            watermelon_img = Image.open(os.path.join(fruits_dir, "watermelon.png"))
            watermelon_img = watermelon_img.resize((80, 80), Image.Resampling.LANCZOS)
            watermelon_photo = ImageTk.PhotoImage(watermelon_img)
            
            product1_img = Image.open(os.path.join(products_dir, "Asset 3@3x.png"))
            product1_img = product1_img.resize((80, 80), Image.Resampling.LANCZOS)
            product1_photo = ImageTk.PhotoImage(product1_img)
            
            product2_img = Image.open(os.path.join(products_dir, "Asset 4@3x.png"))
            product2_img = product2_img.resize((80, 80), Image.Resampling.LANCZOS)
            product2_photo = ImageTk.PhotoImage(product2_img)
            
            product3_img = Image.open(os.path.join(products_dir, "Asset 5@3x.png"))
            product3_img = product3_img.resize((80, 80), Image.Resampling.LANCZOS)
            product3_photo = ImageTk.PhotoImage(product3_img)
            
            canvas.create_image(60, 50, image=banana_photo)
            canvas.banana_photo = banana_photo
            
            canvas.create_image(1100, 55, image=product1_photo)
            canvas.product1_photo = product1_photo
            
            canvas.create_image(50, 280, image=watermelon_photo)
            canvas.watermelon_photo = watermelon_photo
            
            canvas.create_image(1090, 315, image=product2_photo)
            canvas.product2_photo = product2_photo
            
            canvas.create_image(55, 605, image=product3_photo)
            canvas.product3_photo = product3_photo
            
            canvas.create_image(1105, 600, image=watermelon_photo)
            canvas.watermelon_photo2 = watermelon_photo
        except Exception as e:
            print(f"Could not load images: {e}")
        
        canvas.create_text(
            600, 80,
            text="ỨNG DỤNG QUẢN LÍ THỰC PHẨM CP BVTV PHÚ NÔNG",
            font=FONTS['title'],
            fill='white'
        )
        
        btn_products_frame = tk.Frame(canvas, bg='white', bd=2)
        btn_products = tk.Button(
            btn_products_frame,
            text="CÁC MẶT HÀNG NÔNG SẢN - THỰC PHẨM",
            font=FONTS['button_large'],
            bg=COLORS['primary'],
            fg=COLORS['white'],
            width=35,
            height=2,
            command=self.show_products_page,
            cursor='hand2',
            bd=0,
            relief='flat'
        )
        btn_products.pack()
        self.bind_hover(btn_products, COLORS['primary'])
        canvas.create_window(600, 180, window=btn_products_frame)
        
        btn_meal_registration_frame = tk.Frame(canvas, bg='white', bd=2)
        btn_meal_registration = tk.Button(
            btn_meal_registration_frame,
            text="DANH SÁCH CNV ĐĂNG KÝ SUẤT ĂN",
            font=FONTS['button_large'],
            bg=COLORS['success'],
            fg=COLORS['white'],
            width=35,
            height=2,
            command=self.show_meal_registration_page,
            cursor='hand2',
            bd=0,
            relief='flat'
        )
        btn_meal_registration.pack()
        self.bind_hover(btn_meal_registration, COLORS['success'])
        canvas.create_window(600, 260, window=btn_meal_registration_frame)
        
        btn_update_employee_frame = tk.Frame(canvas, bg='white', bd=2)
        btn_update_employee = tk.Button(
            btn_update_employee_frame,
            text="CẬP NHẬT DANH SÁCH NHÂN VIÊN",
            font=FONTS['button_large'],
            bg=COLORS['pink'],
            fg=COLORS['white'],
            width=35,
            height=2,
            command=self.show_employee_management,
            cursor='hand2',
            bd=0,
            relief='flat'
        )
        btn_update_employee.pack()
        self.bind_hover(btn_update_employee, COLORS['pink'])
        canvas.create_window(600, 340, window=btn_update_employee_frame)
        
        btn_statistics_frame = tk.Frame(canvas, bg='white', bd=2)
        btn_statistics = tk.Button(
            btn_statistics_frame,
            text="THỐNG KÊ",
            font=FONTS['button_large'],
            bg=COLORS['info'],
            fg=COLORS['white'],
            width=35,
            height=2,
            command=self.show_statistics,
            cursor='hand2',
            bd=0,
            relief='flat'
        )
        btn_statistics.pack()
        self.bind_hover(btn_statistics, COLORS['info'])
        canvas.create_window(600, 420, window=btn_statistics_frame)
        
        exit_btn_frame = tk.Frame(canvas, bg='white', bd=2)
        exit_btn = tk.Button(
            exit_btn_frame,
            text="Thoát",
            font=FONTS['section'],
            bg=COLORS['danger'],
            fg=COLORS['white'],
            width=15,
            command=self.root.quit,
            bd=0,
            relief='flat'
        )
        exit_btn.pack()
        self.bind_hover(exit_btn, COLORS['danger'])
        canvas.create_window(600, 520, window=exit_btn_frame)
    
    def show_products_page(self):
        ProductsPage(self.root, self.data_manager, self.show_main_menu)
    
    def show_meal_registration_page(self):
        MealRegistrationPage(self.root, self.data_manager, self.show_main_menu)
    
    def show_employee_management(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Quản lý danh sách nhân viên")
        dialog.geometry("1200x700")
        dialog.configure(bg=COLORS['white'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = (screen_width - 1200) // 2
        y = (screen_height - 700) // 2
        dialog.geometry(f"1200x700+{x}+{y}")
        
        header_frame = tk.Frame(dialog, bg=COLORS['primary'], height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="QUẢN LÝ DANH SÁCH NHÂN VIÊN",
            font=FONTS['header'],
            bg=COLORS['primary'],
            fg=COLORS['white']
        ).pack(pady=15)
        
        toolbar_frame = tk.Frame(dialog, bg=COLORS['light_bg'], height=60)
        toolbar_frame.pack(fill='x')
        toolbar_frame.pack_propagate(False)
        
        btn_frame = tk.Frame(toolbar_frame, bg=COLORS['light_bg'])
        btn_frame.pack(side='left', padx=10, pady=15)
        
        manage_tree = None
        manage_registrations = self.data_manager.load_meal_list()
        
        def refresh_manage_display():
            for item in manage_tree.get_children():
                manage_tree.delete(item)
            
            for idx, reg in enumerate(manage_registrations):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                
                lunch_val = float(reg['lunch'])
                dinner_val = float(reg['dinner'])
                total_val = lunch_val + dinner_val
                
                manage_tree.insert('', 'end', values=(
                    reg['stt'],
                    reg['name'],
                    reg['department'],
                    f"{lunch_val:.2f}",
                    f"{dinner_val:.2f}",
                    f"{total_val:.2f}",
                    reg['note']
                ), tags=(tag,))
        
        def add_new_item():
            add_dialog = tk.Toplevel(dialog)
            add_dialog.title("Thêm nhân viên")
            add_dialog.geometry("500x550")
            add_dialog.configure(bg=COLORS['white'])
            add_dialog.transient(dialog)
            add_dialog.grab_set()
            
            screen_w = add_dialog.winfo_screenwidth()
            screen_h = add_dialog.winfo_screenheight()
            x_pos = (screen_w - 500) // 2
            y_pos = (screen_h - 550) // 2
            add_dialog.geometry(f"500x550+{x_pos}+{y_pos}")
            
            main_frame = tk.Frame(add_dialog, bg=COLORS['white'], padx=30, pady=15)
            main_frame.pack(expand=True, fill='both')
            
            tk.Label(
                main_frame,
                text="Thêm nhân viên",
                font=FONTS['header'],
                bg=COLORS['white'],
                fg=COLORS['primary']
            ).pack(pady=(0, 12))
            
            tk.Label(main_frame, text="Họ & Tên:", font=FONTS['section'], bg=COLORS['white']).pack(anchor='w', pady=(5, 3))
            name_entry = tk.Entry(main_frame, font=('Arial', 12), width=40)
            name_entry.pack(pady=(0, 5), ipady=5)
            
            tk.Label(main_frame, text="Bộ phận:", font=FONTS['section'], bg=COLORS['white']).pack(anchor='w', pady=(5, 3))
            dept_entry = tk.Entry(main_frame, font=('Arial', 12), width=40)
            dept_entry.pack(pady=(0, 5), ipady=5)
            
            tk.Label(main_frame, text="Ăn trưa 11h30:", font=FONTS['section'], bg=COLORS['white']).pack(anchor='w', pady=(5, 5))
            lunch_var = tk.IntVar(value=1)
            lunch_frame = tk.Frame(main_frame, bg=COLORS['white'])
            lunch_frame.pack(anchor='w', pady=(0, 8))
            tk.Radiobutton(lunch_frame, text="Không ăn (0)", variable=lunch_var, value=0, font=('Arial', 12), bg=COLORS['white'], selectcolor=COLORS['light_bg']).pack(side='left', padx=(10, 30))
            tk.Radiobutton(lunch_frame, text="Có ăn (1)", variable=lunch_var, value=1, font=('Arial', 12), bg=COLORS['white'], selectcolor=COLORS['light_bg']).pack(side='left')
            
            tk.Label(main_frame, text="Ăn chiều 16h00:", font=FONTS['section'], bg=COLORS['white']).pack(anchor='w', pady=(5, 5))
            dinner_var = tk.IntVar(value=1)
            dinner_frame = tk.Frame(main_frame, bg=COLORS['white'])
            dinner_frame.pack(anchor='w', pady=(0, 8))
            tk.Radiobutton(dinner_frame, text="Không ăn (0)", variable=dinner_var, value=0, font=('Arial', 12), bg=COLORS['white'], selectcolor=COLORS['light_bg']).pack(side='left', padx=(10, 30))
            tk.Radiobutton(dinner_frame, text="Có ăn (1)", variable=dinner_var, value=1, font=('Arial', 12), bg=COLORS['white'], selectcolor=COLORS['light_bg']).pack(side='left')
            
            tk.Label(main_frame, text="Ghi chú:", font=FONTS['section'], bg=COLORS['white']).pack(anchor='w', pady=(5, 5))
            note_entry = tk.Entry(main_frame, font=('Arial', 12), width=40)
            note_entry.pack(pady=(0, 12), ipady=5)
            
            def save_new():
                name = name_entry.get().strip()
                department = dept_entry.get().strip()
                
                if not name:
                    messagebox.showwarning("Cảnh báo", "Vui lòng nhập Họ & Tên!")
                    return
                
                if manage_registrations:
                    max_stt = max(reg['stt'] for reg in manage_registrations)
                    stt = max_stt + 1
                else:
                    stt = 1
                
                lunch = float(lunch_var.get())
                dinner = float(dinner_var.get())
                
                new_reg = {
                    'stt': stt,
                    'name': name,
                    'department': department,
                    'lunch': lunch,
                    'dinner': dinner,
                    'total': lunch + dinner,
                    'note': note_entry.get().strip()
                }
                
                manage_registrations.append(new_reg)
                manage_registrations.sort(key=lambda x: x['stt'])
                refresh_manage_display()
                add_dialog.destroy()
                messagebox.showinfo("Thành công", "Đã thêm nhân viên thành công!")
            
            btn_frame_add = tk.Frame(main_frame, bg=COLORS['white'])
            btn_frame_add.pack(pady=10)
            tk.Button(btn_frame_add, text="✓ THÊM", font=('Arial', 13, 'bold'), bg=COLORS['success'], fg=COLORS['white'], width=15, height=2, command=save_new, cursor='hand2').pack(side='left', padx=10)
            tk.Button(btn_frame_add, text="✗ HỦY", font=('Arial', 13, 'bold'), bg=COLORS['secondary'], fg=COLORS['white'], width=15, height=2, command=add_dialog.destroy, cursor='hand2').pack(side='left', padx=10)
        
        def edit_item():
            item = manage_tree.selection()
            if not item:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dòng để sửa!")
                return
            
            values = manage_tree.item(item[0])['values']
            if not values[0]:
                return
            
            stt = values[0]
            reg = None
            for r in manage_registrations:
                if r['stt'] == stt:
                    reg = r
                    break
            
            if not reg:
                return
            
            edit_dialog = tk.Toplevel(dialog)
            edit_dialog.title("Chỉnh sửa nhân viên")
            edit_dialog.geometry("500x650")
            edit_dialog.configure(bg=COLORS['white'])
            edit_dialog.transient(dialog)
            edit_dialog.grab_set()
            
            screen_w = edit_dialog.winfo_screenwidth()
            screen_h = edit_dialog.winfo_screenheight()
            x_pos = (screen_w - 500) // 2
            y_pos = (screen_h - 650) // 2
            edit_dialog.geometry(f"500x650+{x_pos}+{y_pos}")
            
            main_frame = tk.Frame(edit_dialog, bg=COLORS['white'], padx=30, pady=20)
            main_frame.pack(expand=True, fill='both')
            
            tk.Label(main_frame, text="Chỉnh sửa nhân viên", font=FONTS['header'], bg=COLORS['white'], fg=COLORS['primary']).pack(pady=(0, 15))
            
            tk.Label(main_frame, text="STT:", font=FONTS['section'], bg=COLORS['white']).pack(anchor='w', pady=(5, 3))
            stt_entry = tk.Entry(main_frame, font=('Arial', 12), width=40)
            stt_entry.insert(0, str(reg['stt']))
            stt_entry.pack(pady=(0, 5), ipady=5)
            
            tk.Label(main_frame, text="Họ & Tên:", font=FONTS['section'], bg=COLORS['white']).pack(anchor='w', pady=(5, 3))
            name_entry = tk.Entry(main_frame, font=('Arial', 12), width=40)
            name_entry.insert(0, reg['name'])
            name_entry.pack(pady=(0, 5), ipady=5)
            
            tk.Label(main_frame, text="Bộ phận:", font=FONTS['section'], bg=COLORS['white']).pack(anchor='w', pady=(5, 3))
            dept_entry = tk.Entry(main_frame, font=('Arial', 12), width=40)
            dept_entry.insert(0, reg['department'])
            dept_entry.pack(pady=(0, 5), ipady=5)
            
            tk.Label(main_frame, text="Ăn trưa 11h30:", font=FONTS['section'], bg=COLORS['white']).pack(anchor='w', pady=(5, 5))
            lunch_var = tk.IntVar(value=int(reg['lunch']))
            lunch_frame = tk.Frame(main_frame, bg=COLORS['white'])
            lunch_frame.pack(anchor='w', pady=(0, 8))
            tk.Radiobutton(lunch_frame, text="Không ăn (0)", variable=lunch_var, value=0, font=('Arial', 12), bg=COLORS['white'], selectcolor=COLORS['light_bg']).pack(side='left', padx=(10, 30))
            tk.Radiobutton(lunch_frame, text="Có ăn (1)", variable=lunch_var, value=1, font=('Arial', 12), bg=COLORS['white'], selectcolor=COLORS['light_bg']).pack(side='left')
            
            tk.Label(main_frame, text="Ăn chiều 16h00:", font=FONTS['section'], bg=COLORS['white']).pack(anchor='w', pady=(5, 5))
            dinner_var = tk.IntVar(value=int(reg['dinner']))
            dinner_frame = tk.Frame(main_frame, bg=COLORS['white'])
            dinner_frame.pack(anchor='w', pady=(0, 8))
            tk.Radiobutton(dinner_frame, text="Không ăn (0)", variable=dinner_var, value=0, font=('Arial', 12), bg=COLORS['white'], selectcolor=COLORS['light_bg']).pack(side='left', padx=(10, 30))
            tk.Radiobutton(dinner_frame, text="Có ăn (1)", variable=dinner_var, value=1, font=('Arial', 12), bg=COLORS['white'], selectcolor=COLORS['light_bg']).pack(side='left')
            
            tk.Label(main_frame, text="Ghi chú:", font=FONTS['section'], bg=COLORS['white']).pack(anchor='w', pady=(5, 5))
            note_entry = tk.Entry(main_frame, font=('Arial', 12), width=40)
            note_entry.insert(0, reg['note'])
            note_entry.pack(pady=(0, 15), ipady=5)
            
            def save_changes():
                new_stt = stt_entry.get().strip()
                new_name = name_entry.get().strip()
                new_dept = dept_entry.get().strip()
                
                if not new_stt or not new_name:
                    messagebox.showwarning("Cảnh báo", "Vui lòng nhập STT và Họ & Tên!")
                    return
                
                try:
                    new_stt = int(new_stt)
                except ValueError:
                    messagebox.showerror("Lỗi", "STT phải là số nguyên!")
                    return
                
                if new_stt != reg['stt']:
                    for r in manage_registrations:
                        if r['stt'] == new_stt:
                            messagebox.showerror("Lỗi", f"STT {new_stt} đã tồn tại!")
                            return
                
                lunch = float(lunch_var.get())
                dinner = float(dinner_var.get())
                
                reg['stt'] = new_stt
                reg['name'] = new_name
                reg['department'] = new_dept
                reg['lunch'] = lunch
                reg['dinner'] = dinner
                reg['total'] = lunch + dinner
                reg['note'] = note_entry.get().strip()
                
                manage_registrations.sort(key=lambda x: x['stt'])
                refresh_manage_display()
                edit_dialog.destroy()
            
            btn_frame_edit = tk.Frame(main_frame, bg=COLORS['white'])
            btn_frame_edit.pack(pady=10)
            tk.Button(btn_frame_edit, text="✓ CẬP NHẬT", font=('Arial', 13, 'bold'), bg=COLORS['success'], fg=COLORS['white'], width=15, height=2, command=save_changes, cursor='hand2').pack(side='left', padx=10)
            tk.Button(btn_frame_edit, text="✗ HỦY", font=('Arial', 13, 'bold'), bg=COLORS['secondary'], fg=COLORS['white'], width=15, height=2, command=edit_dialog.destroy, cursor='hand2').pack(side='left', padx=10)
        
        def delete_item():
            item = manage_tree.selection()
            if not item:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dòng để xóa!")
                return
            
            values = manage_tree.item(item[0])['values']
            if not values[0]:
                return
            
            stt = values[0]
            name = values[1]
            
            result = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa nhân viên:\n{name} (STT: {stt})?")
            if result:
                manage_registrations[:] = [reg for reg in manage_registrations if reg['stt'] != stt]
                refresh_manage_display()
                messagebox.showinfo("Thành công", "Đã xóa nhân viên!")
        
        def save_all_changes():
            try:
                self.data_manager.save_meal_list(manage_registrations)
                messagebox.showinfo("Thành công", "Đã lưu thay đổi vào sheet Meal_20251120!")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu: {str(e)}")
        
        tk.Button(btn_frame, text="➕ Thêm", font=FONTS['small_bold'], bg=COLORS['success'], fg=COLORS['white'], width=12, command=add_new_item).pack(side='left', padx=5)
        tk.Button(btn_frame, text="✏️ Sửa", font=FONTS['small_bold'], bg=COLORS['warning'], fg=COLORS['white'], width=12, command=edit_item).pack(side='left', padx=5)
        tk.Button(btn_frame, text="🗑️ Xóa", font=FONTS['small_bold'], bg=COLORS['danger'], fg=COLORS['white'], width=12, command=delete_item).pack(side='left', padx=5)
        tk.Button(btn_frame, text="💾 Lưu thay đổi", font=FONTS['small_bold'], bg=COLORS['primary'], fg=COLORS['white'], width=12, command=save_all_changes).pack(side='left', padx=5)
        tk.Button(btn_frame, text="✗ Đóng", font=FONTS['small_bold'], bg=COLORS['secondary'], fg=COLORS['white'], width=12, command=dialog.destroy).pack(side='left', padx=5)
        
        container_frame = tk.Frame(dialog, bg=COLORS['white'])
        container_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        style = ttk.Style()
        style.configure("Manage.Treeview", background=COLORS['white'], foreground="black", rowheight=30, fieldbackground=COLORS['white'], font=FONTS['table'])
        style.configure("Manage.Treeview.Heading", font=FONTS['table_header'], background=COLORS['darker'], foreground=COLORS['white'], relief='flat')
        style.map('Manage.Treeview', background=[('selected', COLORS['primary'])])
        
        scrollbar = ttk.Scrollbar(container_frame, orient='vertical')
        scrollbar.pack(side='right', fill='y')
        
        manage_tree = ttk.Treeview(container_frame, columns=('STT', 'Name', 'Department', 'Lunch', 'Dinner', 'Total', 'Note'), show='headings', yscrollcommand=scrollbar.set, style="Manage.Treeview")
        scrollbar.config(command=manage_tree.yview)
        
        manage_tree.heading('STT', text='STT', anchor='center')
        manage_tree.heading('Name', text='HỌ & TÊN', anchor='w')
        manage_tree.heading('Department', text='BỘ PHẬN', anchor='w')
        manage_tree.heading('Lunch', text='ĂN TRƯA 11h30', anchor='center')
        manage_tree.heading('Dinner', text='ĂN CHIỀU 16h00', anchor='center')
        manage_tree.heading('Total', text='PHẦN ĂN', anchor='center')
        manage_tree.heading('Note', text='GHI CHÚ', anchor='w')
        
        manage_tree.column('STT', width=60, anchor='center', stretch=False)
        manage_tree.column('Name', width=200, anchor='w', stretch=False)
        manage_tree.column('Department', width=150, anchor='w', stretch=False)
        manage_tree.column('Lunch', width=150, anchor='center', stretch=False)
        manage_tree.column('Dinner', width=150, anchor='center', stretch=False)
        manage_tree.column('Total', width=100, anchor='center', stretch=False)
        manage_tree.column('Note', width=250, anchor='w', stretch=True)
        
        manage_tree.pack(expand=True, fill='both')
        
        manage_tree.tag_configure('oddrow', background=COLORS['row_odd'])
        manage_tree.tag_configure('evenrow', background=COLORS['row_even'])
        
        manage_tree.bind('<Double-1>', lambda e: edit_item())
        
        refresh_manage_display()
    
    def show_statistics(self):
        from tkinter import ttk
        from datetime import datetime
        import calendar
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Thống kê chi phí suất ăn")
        dialog.geometry("500x400")
        dialog.configure(bg=COLORS['white'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = (screen_width - 500) // 2
        y = (screen_height - 400) // 2
        dialog.geometry(f"500x400+{x}+{y}")
        
        main_frame = tk.Frame(dialog, bg=COLORS['white'], padx=30, pady=20)
        main_frame.pack(expand=True, fill='both')
        
        tk.Label(
            main_frame,
            text="THỐNG KÊ CHI PHÍ SUẤT ĂN",
            font=FONTS['header'],
            bg=COLORS['white'],
            fg=COLORS['primary']
        ).pack(pady=(0, 20))
        
        tk.Label(
            main_frame,
            text="Chọn tháng/năm để thống kê:",
            font=FONTS['section'],
            bg=COLORS['white']
        ).pack(anchor='w', pady=(10, 5))
        
        date_frame = tk.Frame(main_frame, bg=COLORS['white'])
        date_frame.pack(pady=10)
        
        tk.Label(date_frame, text="Tháng:", font=FONTS['normal'], bg=COLORS['white']).pack(side='left', padx=5)
        month_var = tk.StringVar(value=str(datetime.now().month))
        month_combo = ttk.Combobox(date_frame, textvariable=month_var, values=[str(i) for i in range(1, 13)], width=5, state='readonly')
        month_combo.pack(side='left', padx=5)
        
        tk.Label(date_frame, text="Năm:", font=FONTS['normal'], bg=COLORS['white']).pack(side='left', padx=5)
        year_var = tk.StringVar(value=str(datetime.now().year))
        year_combo = ttk.Combobox(date_frame, textvariable=year_var, values=[str(i) for i in range(2020, 2031)], width=8, state='readonly')
        year_combo.pack(side='left', padx=5)
        
        progress_label = tk.Label(main_frame, text="", font=FONTS['small'], bg=COLORS['white'], fg=COLORS['success'])
        progress_label.pack(pady=10)
        
        def generate_statistics():
            try:
                month = int(month_var.get())
                year = int(year_var.get())
                
                progress_label.config(text="Đang xử lý...", fg=COLORS['warning'])
                dialog.update()
                
                data_rows = self.data_manager.get_monthly_statistics_data(month, year)
                
                dialog.destroy()
                self.show_statistics_preview(month, year, data_rows)
                
            except Exception as e:
                progress_label.config(text="", fg=COLORS['danger'])
                messagebox.showerror("Lỗi", f"Không thể tạo thống kê:\n{str(e)}")
        
        btn_frame = tk.Frame(main_frame, bg=COLORS['white'])
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame,
            text="✓ TẠO THỐNG KÊ",
            font=FONTS['button'],
            bg=COLORS['success'],
            fg=COLORS['white'],
            width=15,
            height=2,
            command=generate_statistics,
            cursor='hand2'
        ).pack(side='left', padx=10)
        
        tk.Button(
            btn_frame,
            text="✗ HỦY",
            font=FONTS['button'],
            bg=COLORS['secondary'],
            fg=COLORS['white'],
            width=15,
            height=2,
            command=dialog.destroy,
            cursor='hand2'
        ).pack(side='left', padx=10)
    
    def show_statistics_preview(self, month, year, data_rows):
        from tkinter import ttk
        
        preview_dialog = tk.Toplevel(self.root)
        preview_dialog.title(f"Thống kê tháng {month}/{year}")
        preview_dialog.geometry("1400x800")
        preview_dialog.configure(bg=COLORS['white'])
        preview_dialog.transient(self.root)
        preview_dialog.grab_set()
        
        screen_width = preview_dialog.winfo_screenwidth()
        screen_height = preview_dialog.winfo_screenheight()
        x = (screen_width - 1400) // 2
        y = (screen_height - 800) // 2
        preview_dialog.geometry(f"1400x800+{x}+{y}")
        
        header_frame = tk.Frame(preview_dialog, bg=COLORS['primary'], height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text=f"THEO DÕI CHI PHÍ SUẤT ĂN THÁNG {str(month).zfill(2)}/{year}",
            font=FONTS['header'],
            bg=COLORS['primary'],
            fg=COLORS['white']
        ).pack(pady=15)
        
        toolbar_frame = tk.Frame(preview_dialog, bg=COLORS['light_bg'], height=70)
        toolbar_frame.pack(fill='x')
        toolbar_frame.pack_propagate(False)
        
        btn_frame = tk.Frame(toolbar_frame, bg=COLORS['light_bg'])
        btn_frame.pack(pady=15)
        
        def save_to_excel():
            try:
                result = self.data_manager.generate_monthly_statistics(month, year)
                messagebox.showinfo("Thành công", result)
                preview_dialog.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu file:\n{str(e)}")
        
        tk.Button(
            btn_frame,
            text="💾 LƯU VÀO EXCEL",
            font=FONTS['button'],
            bg=COLORS['success'],
            fg=COLORS['white'],
            width=20,
            height=2,
            command=save_to_excel,
            cursor='hand2'
        ).pack(side='left', padx=10)
        
        tk.Button(
            btn_frame,
            text="✗ HỦY",
            font=FONTS['button'],
            bg=COLORS['secondary'],
            fg=COLORS['white'],
            width=15,
            height=2,
            command=preview_dialog.destroy,
            cursor='hand2'
        ).pack(side='left', padx=10)
        
        container_frame = tk.Frame(preview_dialog, bg=COLORS['white'])
        container_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        style = ttk.Style()
        style.configure("Stats.Treeview", background=COLORS['white'], foreground="black", rowheight=30, fieldbackground=COLORS['white'], font=FONTS['table'])
        style.configure("Stats.Treeview.Heading", font=FONTS['table_header'], background=COLORS['darker'], foreground=COLORS['white'], relief='flat')
        style.map('Stats.Treeview', background=[('selected', COLORS['primary'])])
        
        scrollbar_y = ttk.Scrollbar(container_frame, orient='vertical')
        scrollbar_y.pack(side='right', fill='y')
        
        scrollbar_x = ttk.Scrollbar(container_frame, orient='horizontal')
        scrollbar_x.pack(side='bottom', fill='x')
        
        stats_tree = ttk.Treeview(
            container_frame,
            columns=('Day', 'DayName', 'TotalMeals', 'TotalCost', 'AvgPrice', 'WeekAvg', 'Note'),
            show='headings',
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
            style="Stats.Treeview"
        )
        
        scrollbar_y.config(command=stats_tree.yview)
        scrollbar_x.config(command=stats_tree.xview)
        
        stats_tree.heading('Day', text='Ngày', anchor='center')
        stats_tree.heading('DayName', text='Thứ', anchor='center')
        stats_tree.heading('TotalMeals', text='Số phần ăn\nTrưa + Chiều', anchor='center')
        stats_tree.heading('TotalCost', text='Chi phí\nthực phẩm', anchor='center')
        stats_tree.heading('AvgPrice', text='Đơn giá\nmỗi suất ăn', anchor='center')
        stats_tree.heading('WeekAvg', text='Trung bình suất\năn của tuần', anchor='center')
        stats_tree.heading('Note', text='Ghi chú', anchor='center')
        
        stats_tree.column('Day', width=70, anchor='center', stretch=False)
        stats_tree.column('DayName', width=80, anchor='center', stretch=False)
        stats_tree.column('TotalMeals', width=150, anchor='center', stretch=False)
        stats_tree.column('TotalCost', width=180, anchor='center', stretch=False)
        stats_tree.column('AvgPrice', width=180, anchor='center', stretch=False)
        stats_tree.column('WeekAvg', width=180, anchor='center', stretch=False)
        stats_tree.column('Note', width=200, anchor='center', stretch=True)
        
        stats_tree.pack(expand=True, fill='both')
        
        for idx, row_data in enumerate(data_rows):
            day = row_data['day']
            day_name = row_data['day_name']
            total_meals = row_data['total_meals']
            total_cost = row_data['total_cost']
            avg_price = row_data['avg_price']
            week_avg = row_data.get('week_avg', 0)
            note = row_data['note']
            weekday = row_data['weekday']
            
            tag = 'weekend' if weekday in [5, 6] else ('evenrow' if idx % 2 == 0 else 'oddrow')
            
            if total_meals == 0:
                stats_tree.insert('', 'end', values=(
                    day,
                    day_name,
                    0,
                    '-',
                    '',
                    '',
                    note
                ), tags=(tag, 'holiday'))
            else:
                cost_str = f'{int(total_cost):,}' if total_cost > 0 else '-'
                avg_str = f'{int(avg_price):,}' if avg_price > 0 else ''
                week_avg_str = f'{int(week_avg):,}' if week_avg > 0 else ''
                
                stats_tree.insert('', 'end', values=(
                    day,
                    day_name,
                    int(total_meals),
                    cost_str,
                    avg_str,
                    week_avg_str,
                    note
                ), tags=(tag,))
        
        stats_tree.tag_configure('oddrow', background=COLORS['row_odd'])
        stats_tree.tag_configure('evenrow', background=COLORS['row_even'])
        stats_tree.tag_configure('weekend', background='#FFFF99')
        stats_tree.tag_configure('holiday', foreground='#FF0000', font=('Arial', 11, 'italic'))
