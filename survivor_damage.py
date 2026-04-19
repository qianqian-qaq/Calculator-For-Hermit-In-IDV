import tkinter as tk
from tkinter import ttk, messagebox
import math

class Survivor:
    def __init__(self, name_key, initial_hp=2.0):
        self.name_key = name_key   # 存储语言键，如 "survivor1"
        self.hp = initial_hp
        self.elect = "无"
        self.invincible = False

class FifthPersonalityDamageCalc:
    def __init__(self, root):
        self.root = root
        self.root.title("第五人格 - 隐士伤害计算器")
        self.root.geometry("1100x800")
        self.root.resizable(True, True)
        self.root.configure(bg="#2b2b2b")

        # 求生者名称键
        self.survivor_keys = ["survivor1", "survivor2", "survivor3", "survivor4"]
        self.survivors = [
            Survivor("survivor1"),
            Survivor("survivor2"),
            Survivor("survivor3"),
            Survivor("survivor4")
        ]

        # 电极颜色（不随主题改变）
        self.elect_colors = {
            "红": "#e74c3c",
            "蓝": "#3498db",
            "无": "#7f8c8d"
        }

        # 主题颜色定义
        self.themes = {
            "dark": {
                "bg": "#2b2b2b",
                "fg": "#ecf0f1",
                "panel_bg": "#3c3f41",
                "panel_fg": "white",
                "hp_fg": "#f1c40f",
                "info_fg": "#bdc3c7",
                "button_attack": "#e67e22",
                "button_heal": "#2ecc71",
                "button_inv_off": "#7f8c8d",
                "button_inv_on": "#f39c12",
                "button_reset": "#95a5a6",
                "combobox_bg": "#4a4d4f",
                "combobox_fg": "white"
            },
            "light": {
                "bg": "#f0f0f0",
                "fg": "#2c3e50",
                "panel_bg": "#ffffff",
                "panel_fg": "#2c3e50",
                "hp_fg": "#e67e22",
                "info_fg": "#555555",
                "button_attack": "#e67e22",
                "button_heal": "#27ae60",
                "button_inv_off": "#95a5a6",
                "button_inv_on": "#f39c12",
                "button_reset": "#7f8c8d",
                "combobox_bg": "white",
                "combobox_fg": "black"
            }
        }
        self.current_theme = tk.StringVar(value="dark")

        self.high_damage_mode = tk.BooleanVar(value=False)
        self.current_lang = tk.StringVar(value="CN")
        self.image_labels = []

        # 完整语言文本库
        self.lang_texts = {
            "CN": {
                "title": "隐士 · 电流分摊计算器",
                "survivor1": "求生者 1",
                "survivor2": "求生者 2",
                "survivor3": "求生者 3",
                "survivor4": "求生者 4",
                "lang_label": "语言:",
                "theme_label": "主题:",
                "elect_red": "红",
                "elect_blue": "蓝",
                "elect_none": "无",
                "hp": "血量",
                "attack": "⚔ 攻击 ⚔",
                "heal": "💚 治疗 (+0.5)",
                "invincible_on": "🛡️ 无敌 ON",
                "invincible_off": "🛡️ 无敌 OFF",
                "high_damage": "恐惧震慑 / 触发挽留 (伤害2.2, 分摊向上取整4位小数)",
                "reset_hp": "重置全部血量",
                "info_default": "点击攻击按钮，伤害会在相同电极的求生者之间分摊（不带电时不分摊）",
                "heal_msg": "{} 恢复了 0.5 血量，当前血量 {:.1f}",
                "attack_invalid": "攻击无效！{} 处于无敌状态，本次攻击不造成任何伤害。无敌状态已解除。",
                "attack_no_elect": "攻击 {}（不带电）{}",
                "attack_with_elect": "攻击 {}（{}电）{}",
                "only_self": "只有 {} 受到 {:.4f} 伤害，且变为不带电",
                "damage_split": "总伤害 {:.1f} 分摊给 {}，每人应受 {:.4f} 伤害",
                "immune_msg": "\n【无敌免疫】{} 免疫了本次伤害，不扣血且保持电极。",
                "no_immune_msg": "\n受伤后他们全部变为不带电",
                "downed_warning": "倒地提示",
                "downed_msg": "{} 已倒地！",
                "reset_msg": "血量已重置，所有求生者恢复 2.0 血，电极保持不变",
                "image_placeholder": "图片功能暂缓\n(后续可加)",
                "status_label": "状态",
                "theme_dark": "深色主题",
                "theme_light": "浅色主题",
            },
            "EN": {
                "title": "Hermit · Current Sharing Calculator",
                "survivor1": "Survivor 1",
                "survivor2": "Survivor 2",
                "survivor3": "Survivor 3",
                "survivor4": "Survivor 4",
                "lang_label": "Language:",
                "theme_label": "Theme:",
                "elect_red": "Red",
                "elect_blue": "Blue",
                "elect_none": "None",
                "hp": "HP",
                "attack": "⚔ Attack ⚔",
                "heal": "💚 Heal (+0.5)",
                "invincible_on": "🛡️ Invincible ON",
                "invincible_off": "🛡️ Invincible OFF",
                "high_damage": "Terror Shock / Detention (DMG 2.2, ceiling 4 decimals)",
                "reset_hp": "Reset HP",
                "info_default": "Click attack: damage is shared among survivors with same charge (no sharing if no charge)",
                "heal_msg": "{} recovered 0.5 HP, current HP {:.1f}",
                "attack_invalid": "Attack invalid! {} is invincible, no damage dealt. Invincibility removed.",
                "attack_no_elect": "Attack {} (No charge) {}",
                "attack_with_elect": "Attack {} ({} charge) {}",
                "only_self": "Only {} takes {:.4f} damage and becomes no charge",
                "damage_split": "Total damage {:.1f} shared among {}，each takes {:.4f} damage",
                "immune_msg": "\n【Invincible】{} immune to damage, no HP loss and charge unchanged.",
                "no_immune_msg": "\nAfter injury, all become no charge",
                "downed_warning": "Downed Alert",
                "downed_msg": "{} has been downed!",
                "reset_msg": "HP reset to 2.0 for all survivors, charges unchanged",
                "image_placeholder": "Image function pending\n(add later)",
                "status_label": "Status",
                "theme_dark": "Dark Theme",
                "theme_light": "Light Theme",
            },
            "JP": {
                "title": "ハーミット · 電流分担計算機",
                "survivor1": "サバイバー 1",
                "survivor2": "サバイバー 2",
                "survivor3": "サバイバー 3",
                "survivor4": "サバイバー 4",
                "lang_label": "言語:",
                "theme_label": "テーマ:",
                "elect_red": "赤",
                "elect_blue": "青",
                "elect_none": "なし",
                "hp": "HP",
                "attack": "⚔ 攻撃 ⚔",
                "heal": "💚 治療 (+0.5)",
                "invincible_on": "🛡️ 無敵 ON",
                "invincible_off": "🛡️ 無敵 OFF",
                "high_damage": "恐怖震撼／執念 (ダメージ2.2, 分担時小数点第4位切り上げ)",
                "reset_hp": "HPリセット",
                "info_default": "攻撃ボタンを押すと、同じ電極のサバイバーにダメージが分担されます（電極なしの場合は分担なし）",
                "heal_msg": "{} は0.5回復、現在HP {:.1f}",
                "attack_invalid": "攻撃無効！ {} は無敵状態のため、ダメージはありません。無敵状態を解除しました。",
                "attack_no_elect": "{}（電極なし）を攻撃 {}",
                "attack_with_elect": "{}（{}電）を攻撃 {}",
                "only_self": "{} のみが {:.4f} ダメージを受け、電極なしになる",
                "damage_split": "総ダメージ {:.1f} を {} で分担、各 {:.4f} ダメージ",
                "immune_msg": "\n【無敵】{} はダメージを無効化、HPと電極は変化なし",
                "no_immune_msg": "\n負傷後は全員が電極なしになる",
                "downed_warning": "ダウン警告",
                "downed_msg": "{} がダウンした！",
                "reset_msg": "HPをリセットしました。全サバイバーのHPが2.0に戻り、電極はそのまま",
                "image_placeholder": "画像機能は保留中\n(後で追加)",
                "status_label": "状態",
                "theme_dark": "ダークテーマ",
                "theme_light": "ライトテーマ",
            }
        }

        self.create_widgets()
        self.apply_language()
        self.apply_theme()
        self.update_display()

    def create_widgets(self):
        # 主容器
        main_container = tk.Frame(self.root)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # 内容区域（左右两部分）
        content_frame = tk.Frame(main_container)
        content_frame.pack(fill="both", expand=True)

        # 左侧面板容器（求生者）
        left_frame = tk.Frame(content_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))

        # 右侧图片容器
        right_frame = tk.Frame(content_frame)
        right_frame.pack(side="right", fill="both", expand=True)

        # 底部控制栏
        bottom_frame = tk.Frame(main_container)
        bottom_frame.pack(side="bottom", fill="x", pady=(10, 0))

        # 创建四个求生者面板
        self.frames = []
        self.invincible_btns = []
        self.hp_labels = []
        self.inv_status_labels = []
        self.elect_menus = []
        self.attack_btns = []
        self.heal_btns = []
        self.panel_labels = []  # 存储每个面板的LabelFrame对象，用于更新标题

        for idx in range(4):
            panel = tk.LabelFrame(left_frame, font=("微软雅黑", 11, "bold"),
                                  padx=8, pady=5, relief=tk.RIDGE, bd=2)
            panel.pack(fill="x", pady=5, expand=False)
            self.frames.append(panel)
            self.panel_labels.append(panel)  # 保存以便更新标题

            # 血量行
            hp_frame = tk.Frame(panel)
            hp_frame.pack(fill="x", pady=2)
            hp_label = tk.Label(hp_frame, font=("微软雅黑", 12))
            hp_label.pack(side="left")
            inv_status = tk.Label(hp_frame, text="", font=("微软雅黑", 10))
            inv_status.pack(side="left", padx=5)
            self.hp_labels.append(hp_label)
            self.inv_status_labels.append(inv_status)

            # 电极下拉菜单
            elect_var = tk.StringVar(value=self.survivors[idx].elect)
            elect_menu = ttk.Combobox(panel, textvariable=elect_var, values=["红", "蓝", "无"],
                                      state="readonly", width=6, font=("微软雅黑", 9))
            elect_menu.pack(pady=2, fill="x")
            elect_menu.bind("<<ComboboxSelected>>", lambda e, i=idx, var=elect_var: self.change_elect(i, var.get()))
            self.elect_menus.append(elect_menu)

            # 攻击按钮
            attack_btn = tk.Button(panel, font=("微软雅黑", 9, "bold"),
                                   command=lambda i=idx: self.attack_survivor(i))
            attack_btn.pack(pady=2, fill="x")
            self.attack_btns.append(attack_btn)

            # 治疗和无敌按钮行
            action_frame = tk.Frame(panel)
            action_frame.pack(fill="x", pady=2)
            heal_btn = tk.Button(action_frame, font=("微软雅黑", 8),
                                 command=lambda i=idx: self.heal_survivor(i))
            heal_btn.pack(side="left", expand=True, fill="x", padx=2)
            inv_btn = tk.Button(action_frame, font=("微软雅黑", 8),
                                command=lambda i=idx: self.toggle_invincible(i))
            inv_btn.pack(side="left", expand=True, fill="x", padx=2)
            self.heal_btns.append(heal_btn)
            self.invincible_btns.append(inv_btn)

        # 右侧图片框
        self.right_frames = []  # 存储右侧每个图片框的LabelFrame和Label
        for idx in range(4):
            img_frame = tk.LabelFrame(right_frame, font=("微软雅黑", 9, "bold"), relief=tk.RIDGE, bd=2)
            img_frame.pack(fill="both", expand=True, pady=5)
            img_label = tk.Label(img_frame, font=("微软雅黑", 9))
            img_label.pack(expand=True, fill="both", padx=5, pady=5)
            self.image_labels.append((img_frame, img_label))
            self.right_frames.append(img_frame)

        # 底部控制栏组件
        left_controls = tk.Frame(bottom_frame)
        left_controls.pack(side="left", padx=5)

        # 语言选择
        lang_frame = tk.Frame(left_controls)
        lang_frame.pack(side="left", padx=5)
        self.lang_label = tk.Label(lang_frame, font=("微软雅黑", 9))
        self.lang_label.pack(side="left")
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.current_lang, values=["CN", "EN", "JP"],
                                  state="readonly", width=5, font=("微软雅黑", 9))
        lang_combo.pack(side="left", padx=5)
        lang_combo.bind("<<ComboboxSelected>>", lambda e: self.apply_language())

        # 主题选择
        theme_frame = tk.Frame(left_controls)
        theme_frame.pack(side="left", padx=10)
        self.theme_label = tk.Label(theme_frame, font=("微软雅黑", 9))
        self.theme_label.pack(side="left")
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.current_theme, values=["dark", "light"],
                                   state="readonly", width=6, font=("微软雅黑", 9))
        theme_combo.pack(side="left", padx=5)
        theme_combo.bind("<<ComboboxSelected>>", lambda e: self.apply_theme())

        # 高伤害模式复选框
        self.high_damage_check = tk.Checkbutton(bottom_frame, variable=self.high_damage_mode,
                                                font=("微软雅黑", 9))
        self.high_damage_check.pack(side="left", padx=10)

        # 重置按钮
        self.reset_btn = tk.Button(bottom_frame, font=("微软雅黑", 9), command=self.reset_hp)
        self.reset_btn.pack(side="right", padx=10)

        # 信息栏
        info_frame = tk.Frame(main_container)
        info_frame.pack(side="bottom", fill="x", pady=(5,0))
        self.info_label = tk.Label(info_frame, font=("微软雅黑", 9))
        self.info_label.pack()

    def apply_theme(self):
        theme = self.current_theme.get()
        colors = self.themes[theme]

        self.root.configure(bg=colors["bg"])

        # 设置各个组件的主题颜色（不覆盖电极颜色）
        for frame in self.frames:
            for child in frame.winfo_children():
                if isinstance(child, (tk.Frame, tk.LabelFrame)):
                    child.configure(bg=colors["panel_bg"])
                elif isinstance(child, tk.Label):
                    child.configure(bg=colors["panel_bg"], fg=colors["panel_fg"])
        for hp_label in self.hp_labels:
            hp_label.configure(bg=colors["panel_bg"], fg=colors["hp_fg"])
        for inv_label in self.inv_status_labels:
            inv_label.configure(bg=colors["panel_bg"], fg=colors["hp_fg"])
        for menu in self.elect_menus:
            menu.configure(foreground=colors["combobox_fg"])
            try:
                menu.configure(background=colors["combobox_bg"])
            except: pass

        for btn in self.attack_btns:
            btn.configure(bg=colors["button_attack"], fg="white", activebackground=colors["button_attack"])
        for btn in self.heal_btns:
            btn.configure(bg=colors["button_heal"], fg="white", activebackground=colors["button_heal"])
        self.reset_btn.configure(bg=colors["button_reset"], fg="white")
        self.info_label.configure(bg=colors["bg"], fg=colors["info_fg"])
        self.high_damage_check.configure(bg=colors["bg"], fg=colors["fg"], selectcolor=colors["bg"])
        for img_frame, img_label in self.image_labels:
            img_frame.configure(bg=colors["panel_bg"], fg=colors["panel_fg"])
            img_label.configure(bg=colors["panel_bg"], fg=colors["panel_fg"])

        # 底部控制栏背景
        bottom_frame = self.root.winfo_children()[0].winfo_children()[-1] if len(self.root.winfo_children())>0 else None
        if bottom_frame:
            bottom_frame.configure(bg=colors["bg"])
            for child in bottom_frame.winfo_children():
                child.configure(bg=colors["bg"])
                if isinstance(child, tk.Frame):
                    for grand in child.winfo_children():
                        grand.configure(bg=colors["bg"])

        # 刷新无敌按钮颜色
        lang = self.current_lang.get()
        texts = self.lang_texts[lang]
        for idx, btn in enumerate(self.invincible_btns):
            if self.survivors[idx].invincible:
                btn.configure(bg=colors["button_inv_on"], fg="white", text=texts['invincible_on'])
            else:
                btn.configure(bg=colors["button_inv_off"], fg="white", text=texts['invincible_off'])

        # 重新应用电极颜色（覆盖面板背景）
        self.update_display()

    def apply_language(self):
        lang = self.current_lang.get()
        texts = self.lang_texts[lang]

        self.root.title(texts['title'])

        # 更新求生者名字显示：面板标题、右侧图片框标题、以及存储的name_key对应的显示名（但攻击消息中使用的是显示名，需要动态获取）
        for idx in range(4):
            survivor_name = texts[self.survivor_keys[idx]]
            # 更新左侧面板的LabelFrame标题
            self.panel_labels[idx].config(text=survivor_name)
            # 更新右侧图片框的LabelFrame标题
            self.right_frames[idx].config(text=f"{survivor_name} {texts['status_label']}")
            # 更新右侧图片框内的占位文字（如果后续有图片，则图片标签的文本也会变）
            self.image_labels[idx][1].config(text=texts['image_placeholder'])

        # 更新按钮文字
        for idx in range(4):
            self.attack_btns[idx].config(text=texts['attack'])
            self.heal_btns[idx].config(text=texts['heal'])
            if self.survivors[idx].invincible:
                self.invincible_btns[idx].config(text=texts['invincible_on'])
            else:
                self.invincible_btns[idx].config(text=texts['invincible_off'])
            self.update_hp_label(idx)

        # 更新电极下拉菜单选项和当前值
        for elect_menu in self.elect_menus:
            current_val = elect_menu.get()
            if current_val in ["红", "Red", "赤"]:
                new_val = texts['elect_red']
            elif current_val in ["蓝", "Blue", "青"]:
                new_val = texts['elect_blue']
            elif current_val in ["无", "None", "なし"]:
                new_val = texts['elect_none']
            else:
                new_val = current_val
            elect_menu.config(values=[texts['elect_red'], texts['elect_blue'], texts['elect_none']])
            elect_menu.set(new_val)

        # 更新底部标签文字
        self.lang_label.config(text=texts['lang_label'])
        self.theme_label.config(text=texts['theme_label'])
        self.high_damage_check.config(text=texts['high_damage'])
        self.reset_btn.config(text=texts['reset_hp'])
        self.info_label.config(text=texts['info_default'])

        self.update_display()

    def update_hp_label(self, idx):
        lang = self.current_lang.get()
        texts = self.lang_texts[lang]
        hp_text = f"{texts['hp']}: {self.survivors[idx].hp:.1f}"
        self.hp_labels[idx].config(text=hp_text)

    def get_survivor_name(self, idx):
        """根据当前语言返回求生者显示名"""
        lang = self.current_lang.get()
        texts = self.lang_texts[lang]
        return texts[self.survivor_keys[idx]]

    def toggle_invincible(self, idx):
        s = self.survivors[idx]
        s.invincible = not s.invincible
        lang = self.current_lang.get()
        texts = self.lang_texts[lang]
        btn = self.invincible_btns[idx]
        if s.invincible:
            btn.config(text=texts['invincible_on'])
            self.inv_status_labels[idx].config(text="🛡️")
        else:
            btn.config(text=texts['invincible_off'])
            self.inv_status_labels[idx].config(text="")
        self.apply_theme()
        self.update_display()

    def change_elect(self, idx, elect_text):
        lang = self.current_lang.get()
        texts = self.lang_texts[lang]
        if elect_text == texts['elect_red']:
            elect = "红"
        elif elect_text == texts['elect_blue']:
            elect = "蓝"
        elif elect_text == texts['elect_none']:
            elect = "无"
        else:
            elect = "无"
        self.survivors[idx].elect = elect
        color = self.elect_colors.get(elect, "#3c3f41")
        self.frames[idx].configure(bg=color)
        for child in self.frames[idx].winfo_children():
            if isinstance(child, (tk.Label, tk.Frame)):
                child.configure(bg=color)
        self.update_display()

    def heal_survivor(self, idx):
        new_hp = min(2.0, self.survivors[idx].hp + 0.5)
        self.survivors[idx].hp = new_hp
        self.update_display()
        lang = self.current_lang.get()
        texts = self.lang_texts[lang]
        name = self.get_survivor_name(idx)
        msg = texts['heal_msg'].format(name, new_hp)
        self.info_label.config(text=msg)

    def attack_survivor(self, target_idx):
        target = self.survivors[target_idx]
        lang = self.current_lang.get()
        texts = self.lang_texts[lang]
        target_name = self.get_survivor_name(target_idx)

        if target.invincible:
            target.invincible = False
            self.invincible_btns[target_idx].config(text=texts['invincible_off'])
            self.inv_status_labels[target_idx].config(text="")
            self.apply_theme()
            self.update_display()
            self.info_label.config(text=texts['attack_invalid'].format(target_name))
            return

        elect = target.elect
        if elect == "无":
            same_elect_indices = [target_idx]
        else:
            same_elect_indices = [i for i, s in enumerate(self.survivors) if s.elect == elect]
            if not same_elect_indices:
                same_elect_indices = [target_idx]

        n = len(same_elect_indices)
        base_damage = 2.2 if self.high_damage_mode.get() else 1.2
        raw_damage_per = base_damage / n

        if self.high_damage_mode.get():
            damage_per_person = math.ceil(raw_damage_per * 10000) / 10000
        else:
            damage_per_person = raw_damage_per

        immune_list = []
        for i in same_elect_indices:
            if self.survivors[i].invincible:
                immune_list.append(self.get_survivor_name(i))
                self.survivors[i].invincible = False
                self.invincible_btns[i].config(text=texts['invincible_off'])
                self.inv_status_labels[i].config(text="")
            else:
                self.survivors[i].hp = max(0, self.survivors[i].hp - damage_per_person)
                if self.survivors[i].elect != "无":
                    self.survivors[i].elect = "无"
                    self.change_elect(i, texts['elect_none'])

        self.apply_theme()
        self.update_display()

        names = [self.get_survivor_name(i) for i in same_elect_indices]
        mode_str = "（高伤模式）" if self.high_damage_mode.get() else ""
        if elect == "无":
            msg = texts['attack_no_elect'].format(target_name, mode_str) + "\n"
            msg += texts['only_self'].format(target_name, damage_per_person)
        else:
            elect_display = texts['elect_red'] if elect == "红" else (texts['elect_blue'] if elect == "蓝" else texts['elect_none'])
            msg = texts['attack_with_elect'].format(target_name, elect_display, mode_str) + "\n"
            msg += texts['damage_split'].format(base_damage, ", ".join(names), damage_per_person)
        if immune_list:
            msg += texts['immune_msg'].format(", ".join(immune_list))
        else:
            msg += texts['no_immune_msg']
        self.info_label.config(text=msg)

        downed = [self.get_survivor_name(i) for i, s in enumerate(self.survivors) if s.hp <= 0]
        if downed:
            messagebox.showwarning(texts['downed_warning'], texts['downed_msg'].format(", ".join(downed)))

    def update_display(self):
        for idx, s in enumerate(self.survivors):
            self.update_hp_label(idx)
            lang = self.current_lang.get()
            texts = self.lang_texts[lang]
            if s.elect == "红":
                display_elect = texts['elect_red']
            elif s.elect == "蓝":
                display_elect = texts['elect_blue']
            else:
                display_elect = texts['elect_none']
            self.elect_menus[idx].set(display_elect)
            # 设置面板背景色为电极颜色
            color = self.elect_colors.get(s.elect, "#3c3f41")
            self.frames[idx].configure(bg=color)
            for child in self.frames[idx].winfo_children():
                if isinstance(child, (tk.Label, tk.Frame)):
                    child.configure(bg=color)
            if s.invincible:
                self.inv_status_labels[idx].config(text="🛡️")
            else:
                self.inv_status_labels[idx].config(text="")
            btn = self.invincible_btns[idx]
            if s.invincible:
                btn.config(text=texts['invincible_on'])
            else:
                btn.config(text=texts['invincible_off'])

    def reset_hp(self):
        for s in self.survivors:
            s.hp = 2.0
        self.update_display()
        lang = self.current_lang.get()
        texts = self.lang_texts[lang]
        self.info_label.config(text=texts['reset_msg'])

if __name__ == "__main__":
    root = tk.Tk()
    app = FifthPersonalityDamageCalc(root)
    root.mainloop()