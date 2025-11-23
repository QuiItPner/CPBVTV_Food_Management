import tkinter as tk
from tkinter import ttk, messagebox
from config import COLORS, FONTS, WINDOW_GEOMETRY, WINDOW_BG
from .products_page import ProductsPage
from .meal_registration_page import MealRegistrationPage

class MainWindow:
    def __init__(self, root, data_manager):
        self.root = root
        self.data_manager = data_manager
        
        self.root.title("Quản Lý Thực Phẩm")
        self.root.geometry(WINDOW_GEOMETRY)
        self.root.configure(bg=WINDOW_BG)
        
        self.show_main_menu()
    
    def show_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        main_frame = tk.Frame(self.root, bg=WINDOW_BG)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        title_label = tk.Label(
            main_frame,
            text="APP QUẢN LÍ THỰC PHẨM CP BVTV",
            font=FONTS['title'],
            bg=WINDOW_BG,
            fg=COLORS['dark']
        )
        title_label.pack(pady=40)
        
        btn_products = tk.Button(
            main_frame,
            text="CÁC MẶT HÀNG NÔNG SẢN - THỰC PHẨM",
            font=FONTS['button_large'],
            bg=COLORS['primary'],
            fg=COLORS['white'],
            width=35,
            height=2,
            command=self.show_products_page,
            cursor='hand2'
        )
        btn_products.pack(pady=10)
        
        btn_meal_registration = tk.Button(
            main_frame,
            text="DANH SÁCH CNV ĐĂNG KÝ SUẤT ĂN",
            font=FONTS['button_large'],
            bg=COLORS['success'],
            fg=COLORS['white'],
            width=35,
            height=2,
            command=self.show_meal_registration_page,
            cursor='hand2'
        )
        btn_meal_registration.pack(pady=10)
        
        btn_update_employee = tk.Button(
            main_frame,
            text="CẬP NHẬT DANH SÁCH NHÂN VIÊN",
            font=FONTS['button_large'],
            bg=COLORS['warning'],
            fg=COLORS['white'],
            width=35,
            height=2,
            command=self.show_employee_management,
            cursor='hand2'
        )
        btn_update_employee.pack(pady=10)
        
        btn_statistics = tk.Button(
            main_frame,
            text="THỐNG KÊ",
            font=FONTS['button_large'],
            bg=COLORS['info'],
            fg=COLORS['white'],
            width=35,
            height=2,
            command=self.show_statistics,
            cursor='hand2'
        )
        btn_statistics.pack(pady=10)
        
        exit_btn = tk.Button(
            main_frame,
            text="Thoát",
            font=FONTS['section'],
            bg=COLORS['danger'],
            fg=COLORS['white'],
            width=15,
            command=self.root.quit
        )
        exit_btn.pack(pady=20)
    
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
