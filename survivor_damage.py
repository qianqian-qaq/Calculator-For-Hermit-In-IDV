import tkinter as tk
from tkinter import ttk, messagebox
import math

class Survivor:
    def __init__(self, name, initial_hp=2.0):
        self.name = name
        self.hp = initial_hp
        self.elect = "无"
        self.invincible = False

class FifthPersonalityDamageCalc:
    def __init__(self, root):
        self.root = root
        self.root.title("第五人格 - 隐士伤害计算器")
        self.root.geometry("1050x850")
        self.root.resizable(True, True)
        self.root.configure(bg="#2b2b2b")

        self.survivors = [
            Survivor("求生者 1"),
            Survivor("求生者 2"),
            Survivor("求生者 3"),
            Survivor("求生者 4")
        ]

        self.elect_colors = {
            "红": "#e74c3c",
            "蓝": "#3498db",
            "无": "#7f8c8d"
        }

        self.high_damage_mode = tk.BooleanVar(value=False)
        self.current_lang = tk.StringVar(value="zh")  # zh, en, ja
        self.image_labels = []

        # 语言文本库
        self.lang_texts = {
            "zh": {
                "title": "隐士 · 电流分摊计算器",
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
            },
            "en": {
                "title": "Hermit · Current Sharing Calculator",
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
            },
            "ja": {
                "title": "ハーミット · 電流分担計算機",
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
            }
        }

        self.create_widgets()
        self.update_display()
        self.apply_language()

    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg="#2b2b2b")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        left_frame = tk.Frame(main_frame, bg="#2b2b2b")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        right_frame = tk.Frame(main_frame, bg="#2b2b2b")
        right_frame.grid(row=0, column=1, sticky="nsew")

        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        self.frames = []
        self.invincible_btns = []
        self.hp_labels = []
        self.inv_status_labels = []
        self.elect_menus = []
        self.attack_btns = []
        self.heal_btns = []

        for idx in range(4):
            panel = tk.LabelFrame(left_frame, text=self.survivors[idx].name, font=("微软雅黑", 11, "bold"),
                                  bg="#3c3f41", fg="white", padx=8, pady=5, relief=tk.RIDGE, bd=2)
            panel.pack(fill="x", pady=5)
            self.frames.append(panel)

            hp_frame = tk.Frame(panel, bg="#3c3f41")
            hp_frame.pack(pady=2)
            hp_label = tk.Label(hp_frame, font=("微软雅黑", 12), bg="#3c3f41", fg="#f1c40f")
            hp_label.pack(side="left")
            inv_status = tk.Label(hp_frame, text="", font=("微软雅黑", 10), bg="#3c3f41", fg="#f39c12")
            inv_status.pack(side="left", padx=5)
            self.hp_labels.append(hp_label)
            self.inv_status_labels.append(inv_status)

            elect_var = tk.StringVar(value=self.survivors[idx].elect)
            elect_menu = ttk.Combobox(panel, textvariable=elect_var, values=["红", "蓝", "无"],
                                      state="readonly", width=6, font=("微软雅黑", 9))
            elect_menu.pack(pady=2)
            elect_menu.bind("<<ComboboxSelected>>", lambda e, i=idx, var=elect_var: self.change_elect(i, var.get()))
            self.elect_menus.append(elect_menu)

            attack_btn = tk.Button(panel, font=("微软雅黑", 9, "bold"),
                                   bg="#e67e22", fg="white", activebackground="#d35400",
                                   command=lambda i=idx: self.attack_survivor(i))
            attack_btn.pack(pady=2)
            self.attack_btns.append(attack_btn)

            action_frame = tk.Frame(panel, bg="#3c3f41")
            action_frame.pack(pady=2)
            heal_btn = tk.Button(action_frame, font=("微软雅黑", 8),
                                 bg="#2ecc71", fg="white", activebackground="#27ae60",
                                 command=lambda i=idx: self.heal_survivor(i))
            heal_btn.pack(side="left", padx=2)
            inv_btn = tk.Button(action_frame, font=("微软雅黑", 8),
                                bg="#7f8c8d", fg="white", activebackground="#95a5a6",
                                command=lambda i=idx: self.toggle_invincible(i))
            inv_btn.pack(side="left", padx=2)
            self.heal_btns.append(heal_btn)
            self.invincible_btns.append(inv_btn)

        # 右侧图片框
        for idx in range(4):
            img_frame = tk.LabelFrame(right_frame, font=("微软雅黑", 9, "bold"),
                                      bg="#3c3f41", fg="white", relief=tk.RIDGE, bd=2)
            img_frame.pack(fill="both", expand=True, pady=5)
            img_label = tk.Label(img_frame, bg="#3c3f41", font=("微软雅黑", 9))
            img_label.pack(expand=True, fill="both", padx=5, pady=5)
            self.image_labels.append((img_frame, img_label))

        # 底部选项栏
        option_frame = tk.Frame(self.root, bg="#2b2b2b")
        option_frame.pack(fill="x", pady=5, padx=20, side="bottom")

        # 语言选择下拉框
        lang_frame = tk.Frame(option_frame, bg="#2b2b2b")
        lang_frame.pack(side="left", padx=10)
        tk.Label(lang_frame, text="Language:", bg="#2b2b2b", fg="#ecf0f1", font=("微软雅黑", 9)).pack(side="left")
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.current_lang, values=["zh", "en", "ja"],
                                  state="readonly", width=5, font=("微软雅黑", 9))
        lang_combo.pack(side="left", padx=5)
        lang_combo.bind("<<ComboboxSelected>>", lambda e: self.apply_language())

        self.high_damage_check = tk.Checkbutton(option_frame,
                                                variable=self.high_damage_mode,
                                                bg="#2b2b2b", fg="#ecf0f1", selectcolor="#2b2b2b",
                                                font=("微软雅黑", 9))
        self.high_damage_check.pack(side="left", padx=10)

        self.reset_btn = tk.Button(option_frame, font=("微软雅黑", 9),
                                   bg="#95a5a6", fg="white", command=self.reset_hp)
        self.reset_btn.pack(side="right", padx=10)

        info_frame = tk.Frame(self.root, bg="#2b2b2b")
        info_frame.pack(fill="x", pady=10, side="bottom")
        self.info_label = tk.Label(info_frame, font=("微软雅黑", 9), bg="#2b2b2b", fg="#bdc3c7")
        self.info_label.pack()

    def apply_language(self):
        lang = self.current_lang.get()
        texts = self.lang_texts[lang]

        self.root.title(f"第五人格 - {texts['title']}" if lang == "zh" else texts['title'])

        for idx, (img_frame, img_label) in enumerate(self.image_labels):
            img_frame.config(text=f"{self.survivors[idx].name} {texts['status_label']}")
            img_label.config(text=texts['image_placeholder'])

        for idx in range(4):
            self.attack_btns[idx].config(text=texts['attack'])
            self.heal_btns[idx].config(text=texts['heal'])
            if self.survivors[idx].invincible:
                self.invincible_btns[idx].config(text=texts['invincible_on'])
            else:
                self.invincible_btns[idx].config(text=texts['invincible_off'])
            self.update_hp_label(idx)

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

        self.high_damage_check.config(text=texts['high_damage'])
        self.reset_btn.config(text=texts['reset_hp'])
        self.info_label.config(text=texts['info_default'])
        self.update_display()

    def update_hp_label(self, idx):
        lang = self.current_lang.get()
        texts = self.lang_texts[lang]
        hp_text = f"{texts['hp']}: {self.survivors[idx].hp:.1f}"
        self.hp_labels[idx].config(text=hp_text)

    def toggle_invincible(self, idx):
        s = self.survivors[idx]
        s.invincible = not s.invincible
        lang = self.current_lang.get()
        texts = self.lang_texts[lang]
        btn = self.invincible_btns[idx]
        if s.invincible:
            btn.config(text=texts['invincible_on'], bg="#f39c12")
            self.inv_status_labels[idx].config(text="🛡️")
        else:
            btn.config(text=texts['invincible_off'], bg="#7f8c8d")
            self.inv_status_labels[idx].config(text="")
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
        msg = texts['heal_msg'].format(self.survivors[idx].name, new_hp)
        self.info_label.config(text=msg)

    def attack_survivor(self, target_idx):
        target = self.survivors[target_idx]
        lang = self.current_lang.get()
        texts = self.lang_texts[lang]

        if target.invincible:
            target.invincible = False
            self.invincible_btns[target_idx].config(text=texts['invincible_off'], bg="#7f8c8d")
            self.inv_status_labels[target_idx].config(text="")
            self.update_display()
            self.info_label.config(text=texts['attack_invalid'].format(target.name))
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
                immune_list.append(self.survivors[i].name)
                self.survivors[i].invincible = False
                self.invincible_btns[i].config(text=texts['invincible_off'], bg="#7f8c8d")
                self.inv_status_labels[i].config(text="")
            else:
                self.survivors[i].hp = max(0, self.survivors[i].hp - damage_per_person)
                if self.survivors[i].elect != "无":
                    self.survivors[i].elect = "无"
                    self.change_elect(i, texts['elect_none'])

        self.update_display()

        names = [self.survivors[i].name for i in same_elect_indices]
        mode_str = "（高伤模式）" if self.high_damage_mode.get() else ""
        if elect == "无":
            msg = texts['attack_no_elect'].format(target.name, mode_str) + "\n"
            msg += texts['only_self'].format(target.name, damage_per_person)
        else:
            elect_display = texts['elect_red'] if elect == "红" else (texts['elect_blue'] if elect == "蓝" else texts['elect_none'])
            msg = texts['attack_with_elect'].format(target.name, elect_display, mode_str) + "\n"
            msg += texts['damage_split'].format(base_damage, ", ".join(names), damage_per_person)
        if immune_list:
            msg += texts['immune_msg'].format(", ".join(immune_list))
        else:
            msg += texts['no_immune_msg']
        self.info_label.config(text=msg)

        downed = [s.name for s in self.survivors if s.hp <= 0]
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
                btn.config(text=texts['invincible_on'], bg="#f39c12")
            else:
                btn.config(text=texts['invincible_off'], bg="#7f8c8d")

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