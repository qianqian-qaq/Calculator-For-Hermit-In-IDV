import tkinter as tk
from tkinter import ttk, messagebox
import math

class Survivor:
    def __init__(self, name, initial_hp=2.0):
        self.name = name
        self.hp = initial_hp
        self.elect = "无"  # "红", "蓝", "无"

class FifthPersonalityDamageCalc:
    def __init__(self, root):
        self.root = root
        self.root.title("第五人格 - 隐士伤害计算器")
        self.root.geometry("880x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#2b2b2b")

        # 初始化四位求生者
        self.survivors = [
            Survivor("求生者 1"),
            Survivor("求生者 2"),
            Survivor("求生者 3"),
            Survivor("求生者 4")
        ]

        # 电极颜色映射
        self.elect_colors = {
            "红": "#e74c3c",
            "蓝": "#3498db",
            "无": "#7f8c8d"
        }

        # 是否开启恐惧震慑/挽留（高伤害模式）
        self.high_damage_mode = tk.BooleanVar(value=False)

        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        # 标题
        title = tk.Label(self.root, text="隐士 · 电流分摊计算器", font=("微软雅黑", 20, "bold"),
                         bg="#2b2b2b", fg="#ecf0f1")
        title.pack(pady=15)

        # 中间区域：四个求生者面板
        self.frames = []
        main_frame = tk.Frame(self.root, bg="#2b2b2b")
        main_frame.pack(expand=True, fill="both", padx=20, pady=10)

        for i in range(2):
            row_frame = tk.Frame(main_frame, bg="#2b2b2b")
            row_frame.pack(expand=True, fill="both", pady=5)
            for j in range(2):
                idx = i*2 + j
                frame = tk.LabelFrame(row_frame, text=self.survivors[idx].name, font=("微软雅黑", 12, "bold"),
                                      bg="#3c3f41", fg="white", padx=10, pady=10, relief=tk.RIDGE, bd=2)
                frame.pack(side="left", expand=True, fill="both", padx=10)
                self.frames.append(frame)

                # 血量标签
                hp_label = tk.Label(frame, text=f"血量: {self.survivors[idx].hp:.1f}", font=("微软雅黑", 14),
                                    bg="#3c3f41", fg="#f1c40f")
                hp_label.pack(pady=5)
                # 电极下拉菜单
                elect_var = tk.StringVar(value=self.survivors[idx].elect)
                elect_menu = ttk.Combobox(frame, textvariable=elect_var, values=["红", "蓝", "无"],
                                          state="readonly", width=8, font=("微软雅黑", 10))
                elect_menu.pack(pady=5)
                # 绑定电极修改事件
                elect_menu.bind("<<ComboboxSelected>>", lambda e, i=idx, var=elect_var: self.change_elect(i, var.get()))

                # 攻击按钮
                attack_btn = tk.Button(frame, text="⚔ 攻击 ⚔", font=("微软雅黑", 10, "bold"),
                                       bg="#e67e22", fg="white", activebackground="#d35400",
                                       command=lambda i=idx: self.attack_survivor(i))
                attack_btn.pack(pady=5)

                # 治疗按钮（回血）
                heal_btn = tk.Button(frame, text="💚 治疗 (+0.5)", font=("微软雅黑", 9),
                                     bg="#2ecc71", fg="white", activebackground="#27ae60",
                                     command=lambda i=idx: self.heal_survivor(i))
                heal_btn.pack(pady=5)

                # 存储标签引用以便更新
                frame.hp_label = hp_label

        # 底部选项区域
        option_frame = tk.Frame(self.root, bg="#2b2b2b")
        option_frame.pack(fill="x", pady=5, padx=20)

        # 高伤害模式复选框
        high_damage_check = tk.Checkbutton(option_frame, text="恐惧震慑 / 触发挽留 (伤害2.2, 分摊向上取整4位小数)",
                                           variable=self.high_damage_mode,
                                           bg="#2b2b2b", fg="#ecf0f1", selectcolor="#2b2b2b",
                                           font=("微软雅黑", 9))
        high_damage_check.pack(side="left", padx=10)

        # 重置按钮
        reset_btn = tk.Button(option_frame, text="重置全部血量", font=("微软雅黑", 10),
                              bg="#95a5a6", fg="white", command=self.reset_hp)
        reset_btn.pack(side="right", padx=10)

        # 底部信息栏
        info_frame = tk.Frame(self.root, bg="#2b2b2b")
        info_frame.pack(fill="x", pady=10)
        self.info_label = tk.Label(info_frame, text="点击攻击按钮，伤害会在相同电极的求生者之间分摊",
                                   font=("微软雅黑", 10), bg="#2b2b2b", fg="#bdc3c7")
        self.info_label.pack()

    def change_elect(self, idx, elect):
        self.survivors[idx].elect = elect
        # 更新对应面板的背景色
        color = self.elect_colors.get(elect, "#3c3f41")
        self.frames[idx].configure(bg=color)
        for child in self.frames[idx].winfo_children():
            if isinstance(child, (tk.Label, tk.Frame)):
                child.configure(bg=color)
        self.update_display()

    def heal_survivor(self, idx):
        """回血：增加0.5，不超过2.0"""
        new_hp = min(2.0, self.survivors[idx].hp + 0.5)
        self.survivors[idx].hp = new_hp
        self.update_display()
        self.info_label.config(text=f"{self.survivors[idx].name} 恢复了 0.5 血量，当前血量 {new_hp:.1f}")

    def attack_survivor(self, target_idx):
        target = self.survivors[target_idx]
        elect = target.elect

        # 找出所有与目标相同电极的求生者
        same_elect_indices = [i for i, s in enumerate(self.survivors) if s.elect == elect]
        if not same_elect_indices:  # 安全起见，至少包含目标自己
            same_elect_indices = [target_idx]

        n = len(same_elect_indices)
        # 决定基础伤害值
        base_damage = 2.2 if self.high_damage_mode.get() else 1.2
        raw_damage_per = base_damage / n

        # 如果开启了高伤害模式，对每个分摊者的伤害进行“保留4位小数向上取整”
        if self.high_damage_mode.get():
            # 向上取整到4位小数：例如 0.7333333 -> 0.7334
            # 使用 math.ceil(raw_damage_per * 10000) / 10000
            damage_per_person = math.ceil(raw_damage_per * 10000) / 10000
            # 但注意：ceil(1.0*10000)/10000 = 1.0，正确。
        else:
            damage_per_person = raw_damage_per  # 普通模式不做额外处理，但保留原精度

        # 应用伤害
        for i in same_elect_indices:
            self.survivors[i].hp = max(0, self.survivors[i].hp - damage_per_person)

        # 受伤后，所有受到伤害的求生者变为不带电
        for i in same_elect_indices:
            if self.survivors[i].elect != "无":
                self.survivors[i].elect = "无"
                # 同步UI中的下拉框和背景色
                self.change_elect(i, "无")

        # 更新显示
        self.update_display()

        # 构建提示信息
        names = [self.survivors[i].name for i in same_elect_indices]
        mode_str = "（高伤模式）" if self.high_damage_mode.get() else ""
        msg = f"攻击 {target.name}（{elect}电）{mode_str}\n" \
              f"总伤害 {base_damage} 分摊给 {', '.join(names)}，每人受到 {damage_per_person:.4f} 伤害\n" \
              f"受伤后他们全部变为不带电"
        self.info_label.config(text=msg)

        # 检查是否有人倒地
        downed = [s.name for s in self.survivors if s.hp <= 0]
        if downed:
            messagebox.showwarning("倒地提示", f"{', '.join(downed)} 已倒地！")

    def update_display(self):
        for idx, s in enumerate(self.survivors):
            self.frames[idx].hp_label.config(text=f"血量: {s.hp:.1f}")
            # 同步下拉框的当前电极
            for child in self.frames[idx].winfo_children():
                if isinstance(child, ttk.Combobox):
                    child.set(s.elect)
                    break
            # 更新背景色
            color = self.elect_colors.get(s.elect, "#3c3f41")
            self.frames[idx].configure(bg=color)
            for child in self.frames[idx].winfo_children():
                if isinstance(child, (tk.Label, tk.Frame)):
                    child.configure(bg=color)

    def reset_hp(self):
        for s in self.survivors:
            s.hp = 2.0
        # 注意：重置血量不改变电极（保留用户设置的电极）
        self.update_display()
        self.info_label.config(text="血量已重置，所有求生者恢复 2.0 血，电极保持不变")

if __name__ == "__main__":
    root = tk.Tk()
    app = FifthPersonalityDamageCalc(root)
    root.mainloop()