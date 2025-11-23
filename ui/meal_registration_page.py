import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from config import COLORS, FONTS

class MealRegistrationPage:
    def __init__(self, root, data_manager, on_back):
        self.root = root
        self.data_manager = data_manager
        self.on_back = on_back
        self.tree = None
        self.registrations = []
        self.current_date = datetime.now()
        self.date_str = self.current_date.strftime("%d/%m/%Y")
        self.morning_menu_items = []
        self.evening_menu_items = []
        
        self._create_page()
    
    def _create_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        main_frame = tk.Frame(self.root, bg=COLORS['white'])
        main_frame.pack(expand=True, fill='both')
        
        self._create_header(main_frame)
        self._create_toolbar(main_frame)
        self._create_table(main_frame)
        
        self.load_data()
    
    def _create_header(self, parent):
        header_frame = tk.Frame(parent, bg=COLORS['primary'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text=f"DANH SÁCH CNV ĐĂNG KÝ SUẤT ĂN NGÀY {self.date_str}",
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
        
        btn_frame = tk.Frame(toolbar_frame, bg=COLORS['light_bg'])
        btn_frame.pack(side='left', padx=10, pady=15)
        
        tk.Button(
            btn_frame,
            text="💾 Lưu",
            font=FONTS['small_bold'],
            bg=COLORS['success'],
            fg=COLORS['white'],
            width=12,
            command=self.save_data
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="🔄 Tải lại",
            font=FONTS['small_bold'],
            bg=COLORS['primary'],
            fg=COLORS['white'],
            width=12,
            command=self.load_data
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="🌅 Thực đơn trưa",
            font=FONTS['small_bold'],
            bg=COLORS['info'],
            fg=COLORS['white'],
            width=16,
            command=self.open_morning_menu
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="🌆 Thực đơn chiều",
            font=FONTS['small_bold'],
            bg=COLORS['info'],
            fg=COLORS['white'],
            width=16,
            command=self.open_evening_menu
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="📊 Tổng hợp thực đơn",
            font=FONTS['small_bold'],
            bg=COLORS['warning'],
            fg=COLORS['white'],
            width=18,
            command=self.open_summary_menu
        ).pack(side='left', padx=5)
    
    def _create_table(self, parent):
        container_frame = tk.Frame(parent, bg=COLORS['white'])
        container_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Meal.Treeview",
            background=COLORS['white'],
            foreground="black",
            rowheight=30,
            fieldbackground=COLORS['white'],
            font=FONTS['table']
        )
        style.configure(
            "Meal.Treeview.Heading",
            font=FONTS['table_header'],
            background=COLORS['darker'],
            foreground=COLORS['white'],
            relief='flat'
        )
        style.map('Meal.Treeview', background=[('selected', COLORS['primary'])])
        
        scrollbar = ttk.Scrollbar(container_frame, orient='vertical')
        scrollbar.pack(side='right', fill='y')
        
        self.tree = ttk.Treeview(
            container_frame,
            columns=('STT', 'Name', 'Department', 'Lunch', 'Dinner', 'Total', 'Note'),
            show='headings',
            yscrollcommand=scrollbar.set,
            style="Meal.Treeview"
        )
        
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading('STT', text='STT', anchor='center')
        self.tree.heading('Name', text='HỌ & TÊN', anchor='w')
        self.tree.heading('Department', text='BỘ PHẬN', anchor='w')
        self.tree.heading('Lunch', text='ĂN TRƯA 11h30', anchor='center')
        self.tree.heading('Dinner', text='ĂN CHIỀU 16h00', anchor='center')
        self.tree.heading('Total', text='PHẦN ĂN', anchor='center')
        self.tree.heading('Note', text='GHI CHÚ (Double-click để sửa)', anchor='w')
        
        self.tree.column('STT', width=60, anchor='center', stretch=False)
        self.tree.column('Name', width=200, anchor='w', stretch=False)
        self.tree.column('Department', width=150, anchor='w', stretch=False)
        self.tree.column('Lunch', width=150, anchor='center', stretch=False)
        self.tree.column('Dinner', width=150, anchor='center', stretch=False)
        self.tree.column('Total', width=100, anchor='center', stretch=False)
        self.tree.column('Note', width=250, anchor='w', stretch=True)
        
        self.tree.pack(expand=True, fill='both')
        
        self.tree.tag_configure('oddrow', background=COLORS['row_odd'])
        self.tree.tag_configure('evenrow', background=COLORS['row_even'])
        self.tree.tag_configure('total_row', background='#ffffcc', font=FONTS['table_header'])
        
        self.tree.bind('<Double-1>', self.on_double_click)
    
    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            meal_list = self.data_manager.load_meal_list()
            
            if not meal_list:
                messagebox.showwarning("Cảnh báo", "Chưa có dữ liệu trong sheet 'Meal_20251120'")
                return
            
            self.registrations = meal_list
            self.refresh_display()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {str(e)}")
    
    def refresh_display(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        total_lunch = 0
        total_dinner = 0
        total_meals = 0
        
        for idx, reg in enumerate(self.registrations):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            
            lunch_val = float(reg['lunch'])
            dinner_val = float(reg['dinner'])
            total_val = lunch_val + dinner_val
            
            total_lunch += lunch_val
            total_dinner += dinner_val
            total_meals += total_val
            
            self.tree.insert('', 'end', values=(
                reg['stt'],
                reg['name'],
                reg['department'],
                f"{lunch_val:.2f}",
                f"{dinner_val:.2f}",
                f"{total_val:.2f}",
                reg['note']
            ), tags=(tag,))
        
        self.tree.insert('', 'end', values=(
            '',
            'Tổng cộng',
            '',
            f"{total_lunch:.2f}",
            f"{total_dinner:.2f}",
            f"{total_meals:.2f}",
            ''
        ), tags=('total_row',))
    
    def on_double_click(self, event):
        item = self.tree.selection()
        if not item:
            return
        
        values = self.tree.item(item[0])['values']
        
        if not values[0]:
            return
        
        stt = values[0]
        
        for reg in self.registrations:
            if reg['stt'] == stt:
                self.edit_registration(reg)
                break
    
    def edit_registration(self, reg):
        dialog = tk.Toplevel(self.root)
        dialog.title("Chỉnh sửa đăng ký")
        dialog.geometry("500x450")
        dialog.configure(bg=COLORS['white'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.resizable(False, False)
        
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = (screen_width - 500) // 2
        y = (screen_height - 450) // 2
        dialog.geometry(f"500x450+{x}+{y}")
        
        main_frame = tk.Frame(dialog, bg=COLORS['white'], padx=30, pady=20)
        main_frame.pack(expand=True, fill='both')
        
        tk.Label(
            main_frame,
            text=f"Nhân viên: {reg['name']}",
            font=FONTS['header'],
            bg=COLORS['white'],
            fg=COLORS['primary']
        ).pack(pady=(0, 10))
        
        info_frame = tk.Frame(main_frame, bg=COLORS['white'])
        info_frame.pack(pady=(0, 15), fill='x')
        
        tk.Label(
            info_frame,
            text=f"STT: {reg['stt']} | Bộ phận: {reg['department']}",
            font=('Arial', 11),
            bg=COLORS['white'],
            fg=COLORS['darker']
        ).pack()
        
        tk.Label(
            main_frame,
            text="Ăn trưa 11h30:",
            font=FONTS['section'],
            bg=COLORS['white']
        ).pack(anchor='w', pady=(5, 5))
        
        lunch_var = tk.IntVar(value=int(reg['lunch']))
        lunch_frame = tk.Frame(main_frame, bg=COLORS['white'])
        lunch_frame.pack(anchor='w', pady=(0, 8))
        
        tk.Radiobutton(
            lunch_frame,
            text="Không ăn (0)",
            variable=lunch_var,
            value=0,
            font=('Arial', 12),
            bg=COLORS['white'],
            selectcolor=COLORS['light_bg']
        ).pack(side='left', padx=(10, 30))
        
        tk.Radiobutton(
            lunch_frame,
            text="Có ăn (1)",
            variable=lunch_var,
            value=1,
            font=('Arial', 12),
            bg=COLORS['white'],
            selectcolor=COLORS['light_bg']
        ).pack(side='left')
        
        tk.Label(
            main_frame,
            text="Ăn chiều 16h00:",
            font=FONTS['section'],
            bg=COLORS['white']
        ).pack(anchor='w', pady=(5, 5))
        
        dinner_var = tk.IntVar(value=int(reg['dinner']))
        dinner_frame = tk.Frame(main_frame, bg=COLORS['white'])
        dinner_frame.pack(anchor='w', pady=(0, 8))
        
        tk.Radiobutton(
            dinner_frame,
            text="Không ăn (0)",
            variable=dinner_var,
            value=0,
            font=('Arial', 12),
            bg=COLORS['white'],
            selectcolor=COLORS['light_bg']
        ).pack(side='left', padx=(10, 30))
        
        tk.Radiobutton(
            dinner_frame,
            text="Có ăn (1)",
            variable=dinner_var,
            value=1,
            font=('Arial', 12),
            bg=COLORS['white'],
            selectcolor=COLORS['light_bg']
        ).pack(side='left')
        
        tk.Label(
            main_frame,
            text="Ghi chú:",
            font=FONTS['section'],
            bg=COLORS['white']
        ).pack(anchor='w', pady=(5, 5))
        
        note_entry = tk.Entry(
            main_frame,
            font=('Arial', 12),
            width=40
        )
        note_entry.insert(0, reg['note'])
        note_entry.pack(pady=(0, 15), ipady=5)
        
        def save_changes():
            lunch = float(lunch_var.get())
            dinner = float(dinner_var.get())
            
            reg['lunch'] = lunch
            reg['dinner'] = dinner
            reg['total'] = lunch + dinner
            reg['note'] = note_entry.get().strip()
            
            self.refresh_display()
            dialog.destroy()
        
        btn_frame = tk.Frame(main_frame, bg=COLORS['white'])
        btn_frame.pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="✓ CẬP NHẬT",
            font=('Arial', 13, 'bold'),
            bg=COLORS['success'],
            fg=COLORS['white'],
            width=15,
            height=2,
            command=save_changes,
            cursor='hand2'
        ).pack(side='left', padx=10)
        
        tk.Button(
            btn_frame,
            text="✗ HỦY",
            font=('Arial', 13, 'bold'),
            bg=COLORS['secondary'],
            fg=COLORS['white'],
            width=15,
            height=2,
            command=dialog.destroy,
            cursor='hand2'
        ).pack(side='left', padx=10)
    
    def save_data(self):
        try:
            meal_file = self.data_manager.save_meal_registration(self.current_date, self.registrations)
            
            total_lunch = sum(float(reg['lunch']) for reg in self.registrations)
            total_dinner = sum(float(reg['dinner']) for reg in self.registrations)
            
            self.data_manager.save_menu_summary(
                self.current_date,
                self.morning_menu_items,
                self.evening_menu_items,
                total_lunch,
                total_dinner
            )
            
            messagebox.showinfo("Thành công", f"Đã lưu dữ liệu vào file:\n{meal_file}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu: {str(e)}")
    
    def add_registration(self):
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
    
    def open_morning_menu(self):
        self._open_menu_dialog("morning")
    
    def open_evening_menu(self):
        self._open_menu_dialog("evening")
    
    def open_summary_menu(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("TỔNG HỢP THỰC ĐƠN")
        dialog.geometry("1400x700")
        dialog.configure(bg=COLORS['white'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = (screen_width - 1400) // 2
        y = (screen_height - 700) // 2
        dialog.geometry(f"1400x700+{x}+{y}")
        
        header_frame = tk.Frame(dialog, bg=COLORS['primary'], height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="TỔNG HỢP THỰC ĐƠN",
            font=FONTS['header'],
            bg=COLORS['primary'],
            fg=COLORS['white']
        ).pack(pady=15)
        
        container_frame = tk.Frame(dialog, bg=COLORS['white'])
        container_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        style = ttk.Style()
        style.configure("Summary.Treeview", background=COLORS['white'], foreground="black", rowheight=30, fieldbackground=COLORS['white'], font=FONTS['table'])
        style.configure("Summary.Treeview.Heading", font=FONTS['table_header'], background=COLORS['darker'], foreground=COLORS['white'], relief='flat')
        style.map('Summary.Treeview', background=[('selected', COLORS['primary'])])
        
        scrollbar = ttk.Scrollbar(container_frame, orient='vertical')
        scrollbar.pack(side='right', fill='y')
        
        summary_tree = ttk.Treeview(container_frame, columns=('STT', 'Name', 'Qty', 'Meals', 'Unit', 'Price', 'Total', 'VAT'), show='headings', yscrollcommand=scrollbar.set, style="Summary.Treeview")
        scrollbar.config(command=summary_tree.yview)
        
        summary_tree.heading('STT', text='TT', anchor='center')
        summary_tree.heading('Name', text='Tên thực phẩm', anchor='w')
        summary_tree.heading('Qty', text='Định mức Kg', anchor='center')
        summary_tree.heading('Meals', text='Số phần ăn', anchor='center')
        summary_tree.heading('Unit', text='Đơn vị Kg', anchor='center')
        summary_tree.heading('Price', text='Đơn giá/Kg', anchor='center')
        summary_tree.heading('Total', text='Thành tiền', anchor='center')
        summary_tree.heading('VAT', text='Trước VAT', anchor='center')
        
        summary_tree.column('STT', width=50, anchor='center', stretch=False)
        summary_tree.column('Name', width=200, anchor='w', stretch=False)
        summary_tree.column('Qty', width=120, anchor='center', stretch=False)
        summary_tree.column('Meals', width=120, anchor='center', stretch=False)
        summary_tree.column('Unit', width=120, anchor='center', stretch=False)
        summary_tree.column('Price', width=120, anchor='center', stretch=False)
        summary_tree.column('Total', width=150, anchor='center', stretch=False)
        summary_tree.column('VAT', width=150, anchor='center', stretch=True)
        
        summary_tree.pack(expand=True, fill='both')
        
        summary_tree.tag_configure('oddrow', background=COLORS['row_odd'])
        summary_tree.tag_configure('evenrow', background=COLORS['row_even'])
        summary_tree.tag_configure('total_row', background='#ffffcc', font=FONTS['table_header'])
        summary_tree.tag_configure('morning_price_row', background='#90EE90', font=FONTS['table_header'])
        summary_tree.tag_configure('evening_price_row', background='#87CEEB', font=FONTS['table_header'])
        summary_tree.tag_configure('average_row', background='#FFD700', font=FONTS['table_header'])
        
        total_lunch = sum(float(reg['lunch']) for reg in self.registrations)
        total_dinner = sum(float(reg['dinner']) for reg in self.registrations)
        total_meals = total_lunch + total_dinner
        
        all_items = []
        for item in self.morning_menu_items:
            all_items.append(item)
        for item in self.evening_menu_items:
            all_items.append(item)
        
        idx = 0
        total_morning_price = 0
        total_evening_price = 0
        
        for item in self.morning_menu_items:
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            summary_tree.insert('', 'end', values=(
                idx + 1,
                item['name'],
                f"{item['qty']:.2f}",
                int(total_lunch),
                f"{item['unit']:.2f}",
                f"{item['price']:,.0f}",
                f"{item['total']:,.0f}",
                f"{item['vat']:,.0f}"
            ), tags=(tag,))
            total_morning_price += item['total']
            idx += 1
        
        for item in self.evening_menu_items:
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            summary_tree.insert('', 'end', values=(
                idx + 1,
                item['name'],
                f"{item['qty']:.2f}",
                int(total_dinner),
                f"{item['unit']:.2f}",
                f"{item['price']:,.0f}",
                f"{item['total']:,.0f}",
                f"{item['vat']:,.0f}"
            ), tags=(tag,))
            total_evening_price += item['total']
            idx += 1
        
        total_price = total_morning_price + total_evening_price
        
        summary_tree.insert('', 'end', values=(
            '',
            'Tổng cộng',
            '',
            '',
            '',
            '',
            f"{total_price:,.0f}",
            ''
        ), tags=('total_row',))
        
        morning_avg = total_morning_price / total_lunch if total_lunch > 0 else 0
        summary_tree.insert('', 'end', values=(
            '',
            'Đơn giá phần ăn trưa',
            '',
            '',
            '',
            '',
            f"{morning_avg:,.0f}",
            ''
        ), tags=('morning_price_row',))
        
        evening_avg = total_evening_price / total_dinner if total_dinner > 0 else 0
        summary_tree.insert('', 'end', values=(
            '',
            'Đơn giá phần ăn chiều',
            '',
            '',
            '',
            '',
            f"{evening_avg:,.0f}",
            ''
        ), tags=('evening_price_row',))
        
        overall_avg = total_price / total_meals if total_meals > 0 else 0
        summary_tree.insert('', 'end', values=(
            '',
            'TRUNG BÌNH',
            '',
            '',
            '',
            '',
            f"{overall_avg:,.0f}",
            ''
        ), tags=('average_row',))
        
        btn_frame = tk.Frame(dialog, bg=COLORS['white'])
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="✗ Đóng", font=FONTS['small_bold'], bg=COLORS['secondary'], fg=COLORS['white'], width=12, command=dialog.destroy).pack(padx=5)
    
    def _open_menu_dialog(self, meal_type):
        title = "THỰC ĐƠN TRƯA" if meal_type == "morning" else "THỰC ĐƠN CHIỀU"
        menu_items = self.morning_menu_items if meal_type == "morning" else self.evening_menu_items
        
        total_meals = sum(float(reg['lunch']) for reg in self.registrations) if meal_type == "morning" else sum(float(reg['dinner']) for reg in self.registrations)
        
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("1400x700")
        dialog.configure(bg=COLORS['white'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = (screen_width - 1400) // 2
        y = (screen_height - 700) // 2
        dialog.geometry(f"1400x700+{x}+{y}")
        
        header_frame = tk.Frame(dialog, bg=COLORS['primary'], height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text=title,
            font=FONTS['header'],
            bg=COLORS['primary'],
            fg=COLORS['white']
        ).pack(pady=15)
        
        products_data = self.data_manager.load_data("Products")
        fruits_data = self.data_manager.load_data("Fruits")
        all_products = {row[1]: row[3] for row in products_data if row[1]}
        all_products.update({row[1]: row[3] for row in fruits_data if row[1]})
        product_names = list(all_products.keys())
        
        form_frame = tk.Frame(dialog, bg=COLORS['light_bg'])
        form_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(form_frame, text=f"Số phần ăn: {int(total_meals)}", font=FONTS['normal'], bg=COLORS['light_bg']).grid(row=0, column=0, columnspan=2, pady=10)
        
        tk.Label(form_frame, text="Tên thực phẩm:", font=FONTS['normal'], bg=COLORS['light_bg']).grid(row=1, column=0, sticky='e', padx=10, pady=5)
        product_combo = ttk.Combobox(form_frame, values=product_names, width=30, font=FONTS['normal'])
        product_combo.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Đơn vị Kg:", font=FONTS['normal'], bg=COLORS['light_bg']).grid(row=1, column=2, sticky='e', padx=10, pady=5)
        unit_entry = tk.Entry(form_frame, width=15, font=FONTS['normal'])
        unit_entry.grid(row=1, column=3, padx=10, pady=5)
        
        tk.Label(form_frame, text="Định mức Kg:", font=FONTS['normal'], bg=COLORS['light_bg']).grid(row=2, column=0, sticky='e', padx=10, pady=5)
        qty_label = tk.Label(form_frame, text="0", font=FONTS['normal'], bg=COLORS['light_bg'], width=15, anchor='w')
        qty_label.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Đơn giá/Kg:", font=FONTS['normal'], bg=COLORS['light_bg']).grid(row=2, column=2, sticky='e', padx=10, pady=5)
        price_label = tk.Label(form_frame, text="0", font=FONTS['normal'], bg=COLORS['light_bg'], width=15, anchor='w')
        price_label.grid(row=2, column=3, padx=10, pady=5)
        
        tk.Label(form_frame, text="Thành tiền:", font=FONTS['normal'], bg=COLORS['light_bg']).grid(row=3, column=0, sticky='e', padx=10, pady=5)
        total_label = tk.Label(form_frame, text="0", font=FONTS['normal'], bg=COLORS['light_bg'], width=15, anchor='w')
        total_label.grid(row=3, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Trước VAT:", font=FONTS['normal'], bg=COLORS['light_bg']).grid(row=3, column=2, sticky='e', padx=10, pady=5)
        vat_label = tk.Label(form_frame, text="0", font=FONTS['normal'], bg=COLORS['light_bg'], width=15, anchor='w')
        vat_label.grid(row=3, column=3, padx=10, pady=5)
        
        def on_product_change(event=None):
            product_name = product_combo.get()
            if product_name in all_products:
                price = all_products[product_name]
                price_label.config(text=f"{price:,.0f}")
                calculate_totals()
        
        def calculate_totals(event=None):
            try:
                unit_val = float(unit_entry.get() or 0)
                price_val = float(price_label.cget("text").replace(",", "") or 0)
                
                if total_meals > 0:
                    qty_val = unit_val / total_meals
                    qty_label.config(text=f"{qty_val:.2f}")
                else:
                    qty_label.config(text="0")
                
                total = unit_val * price_val
                vat_val = total / 1.05
                total_label.config(text=f"{total:,.0f}")
                vat_label.config(text=f"{vat_val:,.0f}")
            except:
                pass
        
        def on_keyrelease(event):
            value = event.widget.get()
            if value == '':
                product_combo['values'] = product_names
            else:
                filtered = [item for item in product_names if value.lower() in item.lower()]
                product_combo['values'] = filtered
        
        product_combo.bind('<<ComboboxSelected>>', on_product_change)
        product_combo.bind('<KeyRelease>', on_keyrelease)
        unit_entry.bind('<KeyRelease>', calculate_totals)
        
        menu_tree = None
        
        def refresh_menu_display():
            for item in menu_tree.get_children():
                menu_tree.delete(item)
            
            for idx, item in enumerate(menu_items):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                menu_tree.insert('', 'end', values=(
                    item['stt'],
                    item['name'],
                    f"{item['qty']:.2f}",
                    int(total_meals),
                    f"{item['unit']:.2f}",
                    f"{item['price']:,.0f}",
                    f"{item['total']:,.0f}",
                    f"{item['vat']:,.0f}"
                ), tags=(tag,))
        
        def add_item():
            product_name = product_combo.get()
            if not product_name:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn tên thực phẩm!")
                return
            
            try:
                qty = float(qty_label.cget("text").replace(",", ""))
                unit = float(unit_entry.get())
                price = float(price_label.cget("text").replace(",", ""))
                total = unit * price
                vat = total / 1.05
                
                stt = len(menu_items) + 1
                menu_items.append({
                    'stt': stt,
                    'name': product_name,
                    'qty': qty,
                    'meals': int(total_meals),
                    'unit': unit,
                    'price': price,
                    'total': total,
                    'vat': vat
                })
                
                refresh_menu_display()
                
                product_combo.set('')
                unit_entry.delete(0, tk.END)
                qty_label.config(text="0")
                price_label.config(text="0")
                total_label.config(text="0")
                vat_label.config(text="0")
                
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng số!")
        
        def delete_item():
            selected = menu_tree.selection()
            if not selected:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dòng để xóa!")
                return
            
            values = menu_tree.item(selected[0])['values']
            stt = values[0]
            
            menu_items[:] = [item for item in menu_items if item['stt'] != stt]
            
            for idx, item in enumerate(menu_items):
                item['stt'] = idx + 1
            
            refresh_menu_display()
        
        def save_menu():
            if meal_type == "morning":
                self.morning_menu_items = list(menu_items)
            else:
                self.evening_menu_items = list(menu_items)
            
            messagebox.showinfo("Thành công", f"Đã lưu {title.lower()}!")
            dialog.destroy()
        
        btn_frame = tk.Frame(form_frame, bg=COLORS['light_bg'])
        btn_frame.grid(row=4, column=0, columnspan=4, pady=15)
        
        tk.Button(btn_frame, text="➕ Thêm", font=FONTS['small_bold'], bg=COLORS['success'], fg=COLORS['white'], width=12, command=add_item).pack(side='left', padx=5)
        tk.Button(btn_frame, text="🗑️ Xóa", font=FONTS['small_bold'], bg=COLORS['danger'], fg=COLORS['white'], width=12, command=delete_item).pack(side='left', padx=5)
        tk.Button(btn_frame, text="💾 Lưu", font=FONTS['small_bold'], bg=COLORS['primary'], fg=COLORS['white'], width=12, command=save_menu).pack(side='left', padx=5)
        tk.Button(btn_frame, text="✗ Đóng", font=FONTS['small_bold'], bg=COLORS['secondary'], fg=COLORS['white'], width=12, command=dialog.destroy).pack(side='left', padx=5)
        
        container_frame = tk.Frame(dialog, bg=COLORS['white'])
        container_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        style = ttk.Style()
        style.configure("Menu.Treeview", background=COLORS['white'], foreground="black", rowheight=30, fieldbackground=COLORS['white'], font=FONTS['table'])
        style.configure("Menu.Treeview.Heading", font=FONTS['table_header'], background=COLORS['darker'], foreground=COLORS['white'], relief='flat')
        style.map('Menu.Treeview', background=[('selected', COLORS['primary'])])
        
        scrollbar = ttk.Scrollbar(container_frame, orient='vertical')
        scrollbar.pack(side='right', fill='y')
        
        menu_tree = ttk.Treeview(container_frame, columns=('STT', 'Name', 'Qty', 'Meals', 'Unit', 'Price', 'Total', 'VAT'), show='headings', yscrollcommand=scrollbar.set, style="Menu.Treeview")
        scrollbar.config(command=menu_tree.yview)
        
        menu_tree.heading('STT', text='TT', anchor='center')
        menu_tree.heading('Name', text='Tên thực phẩm', anchor='w')
        menu_tree.heading('Qty', text='Định mức Kg', anchor='center')
        menu_tree.heading('Meals', text='Số phần ăn', anchor='center')
        menu_tree.heading('Unit', text='Đơn vị Kg', anchor='center')
        menu_tree.heading('Price', text='Đơn giá/Kg', anchor='center')
        menu_tree.heading('Total', text='Thành tiền', anchor='center')
        menu_tree.heading('VAT', text='Trước VAT', anchor='center')
        
        menu_tree.column('STT', width=50, anchor='center', stretch=False)
        menu_tree.column('Name', width=200, anchor='w', stretch=False)
        menu_tree.column('Qty', width=120, anchor='center', stretch=False)
        menu_tree.column('Meals', width=120, anchor='center', stretch=False)
        menu_tree.column('Unit', width=120, anchor='center', stretch=False)
        menu_tree.column('Price', width=120, anchor='center', stretch=False)
        menu_tree.column('Total', width=150, anchor='center', stretch=False)
        menu_tree.column('VAT', width=150, anchor='center', stretch=True)
        
        menu_tree.pack(expand=True, fill='both')
        
        menu_tree.tag_configure('oddrow', background=COLORS['row_odd'])
        menu_tree.tag_configure('evenrow', background=COLORS['row_even'])
        
        refresh_menu_display()

