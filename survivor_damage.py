import tkinter as tk
from tkinter import ttk, messagebox
import math

class Survivor:
    def __init__(self, name, initial_hp=2.0):
        self.name = name
        self.hp = initial_hp
        self.elect = "无"

class FifthPersonalityDamageCalc:
    def __init__(self, root):
        self.root = root
        self.root.title("第五人格 - 隐士伤害计算器")
        self.root.geometry("1000x800")   # 增加高度
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
        self.image_labels = []

        self.create_widgets()
        self.update_display()

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
        for idx in range(4):
            # 减少垂直内边距 pady=5, 并减小 LabelFrame 内部边距
            panel = tk.LabelFrame(left_frame, text=self.survivors[idx].name, font=("微软雅黑", 11, "bold"),
                                  bg="#3c3f41", fg="white", padx=8, pady=5, relief=tk.RIDGE, bd=2)
            panel.pack(fill="x", pady=5)   # 面板之间间距从8改为5
            self.frames.append(panel)

            # 血量标签，减小字体和间距
            hp_label = tk.Label(panel, text=f"血量: {self.survivors[idx].hp:.1f}", font=("微软雅黑", 12),
                                bg="#3c3f41", fg="#f1c40f")
            hp_label.pack(pady=2)   # 从5改为2

            elect_var = tk.StringVar(value=self.survivors[idx].elect)
            elect_menu = ttk.Combobox(panel, textvariable=elect_var, values=["红", "蓝", "无"],
                                      state="readonly", width=6, font=("微软雅黑", 9))
            elect_menu.pack(pady=2)
            elect_menu.bind("<<ComboboxSelected>>", lambda e, i=idx, var=elect_var: self.change_elect(i, var.get()))

            attack_btn = tk.Button(panel, text="⚔ 攻击 ⚔", font=("微软雅黑", 9, "bold"),
                                   bg="#e67e22", fg="white", activebackground="#d35400",
                                   command=lambda i=idx: self.attack_survivor(i))
            attack_btn.pack(pady=2)

            heal_btn = tk.Button(panel, text="💚 治疗 (+0.5)", font=("微软雅黑", 8),
                                 bg="#2ecc71", fg="white", activebackground="#27ae60",
                                 command=lambda i=idx: self.heal_survivor(i))
            heal_btn.pack(pady=2)

            panel.hp_label = hp_label

        # 右侧图片框（保持占位，高度跟随左侧）
        for idx in range(4):
            img_frame = tk.LabelFrame(right_frame, text=f"{self.survivors[idx].name} 状态", font=("微软雅黑", 9, "bold"),
                                      bg="#3c3f41", fg="white", relief=tk.RIDGE, bd=2)
            img_frame.pack(fill="both", expand=True, pady=5)
            img_label = tk.Label(img_frame, bg="#3c3f41", text="图片功能暂缓\n(后续可加)", font=("微软雅黑", 9))
            img_label.pack(expand=True, fill="both", padx=5, pady=5)
            self.image_labels.append(img_label)

        # 底部选项栏
        option_frame = tk.Frame(self.root, bg="#2b2b2b")
        option_frame.pack(fill="x", pady=5, padx=20, side="bottom")

        high_damage_check = tk.Checkbutton(option_frame, text="恐惧震慑 / 触发挽留 (伤害2.2, 分摊向上取整4位小数)",
                                           variable=self.high_damage_mode,
                                           bg="#2b2b2b", fg="#ecf0f1", selectcolor="#2b2b2b",
                                           font=("微软雅黑", 9))
        high_damage_check.pack(side="left", padx=10)

        reset_btn = tk.Button(option_frame, text="重置全部血量", font=("微软雅黑", 9),
                              bg="#95a5a6", fg="white", command=self.reset_hp)
        reset_btn.pack(side="right", padx=10)

        info_frame = tk.Frame(self.root, bg="#2b2b2b")
        info_frame.pack(fill="x", pady=10, side="bottom")
        self.info_label = tk.Label(info_frame, text="点击攻击按钮，伤害会在相同电极的求生者之间分摊（不带电时不分摊）",
                                   font=("微软雅黑", 9), bg="#2b2b2b", fg="#bdc3c7")
        self.info_label.pack()

    # ---------- 核心功能 ----------
    def change_elect(self, idx, elect):
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
        self.info_label.config(text=f"{self.survivors[idx].name} 恢复了 0.5 血量，当前血量 {new_hp:.1f}")

    def attack_survivor(self, target_idx):
        target = self.survivors[target_idx]
        elect = target.elect

        # 关键修正：如果目标不带电，则只有目标自己承受伤害，不与其他不带电分摊
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

        # 应用伤害
        for i in same_elect_indices:
            self.survivors[i].hp = max(0, self.survivors[i].hp - damage_per_person)

        # 受伤后变为不带电（仅对实际受到伤害的人）
        for i in same_elect_indices:
            if self.survivors[i].elect != "无":
                self.survivors[i].elect = "无"
                self.change_elect(i, "无")

        self.update_display()

        # 提示信息
        names = [self.survivors[i].name for i in same_elect_indices]
        mode_str = "（高伤模式）" if self.high_damage_mode.get() else ""
        if elect == "无":
            msg = f"攻击 {target.name}（不带电）{mode_str}\n只有 {target.name} 受到 {damage_per_person:.4f} 伤害，且变为不带电"
        else:
            msg = f"攻击 {target.name}（{elect}电）{mode_str}\n总伤害 {base_damage} 分摊给 {', '.join(names)}，每人受到 {damage_per_person:.4f} 伤害\n受伤后他们全部变为不带电"
        self.info_label.config(text=msg)

        downed = [s.name for s in self.survivors if s.hp <= 0]
        if downed:
            messagebox.showwarning("倒地提示", f"{', '.join(downed)} 已倒地！")

    def update_display(self):
        for idx, s in enumerate(self.survivors):
            self.frames[idx].hp_label.config(text=f"血量: {s.hp:.1f}")
            for child in self.frames[idx].winfo_children():
                if isinstance(child, ttk.Combobox):
                    child.set(s.elect)
                    break
            color = self.elect_colors.get(s.elect, "#3c3f41")
            self.frames[idx].configure(bg=color)
            for child in self.frames[idx].winfo_children():
                if isinstance(child, (tk.Label, tk.Frame)):
                    child.configure(bg=color)

    def reset_hp(self):
        for s in self.survivors:
            s.hp = 2.0
        self.update_display()
        self.info_label.config(text="血量已重置，所有求生者恢复 2.0 血，电极保持不变")

if __name__ == "__main__":
    root = tk.Tk()
    app = FifthPersonalityDamageCalc(root)
    root.mainloop()