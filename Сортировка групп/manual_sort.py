import customtkinter as ctk
from PIL import Image
from utils import Screenshots, Pool, pool_path

ctk.set_appearance_mode("dark")
systemFont: tuple
numberFont: tuple
bigButtonsFont: tuple
smallButtonsFont: tuple

ratio_image_width = 0.5
indentX_image = 0.1
pb_height: int

RED = "#8B0000"
GREEN = "#006400"
GRAY = "gray"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.ss = Screenshots(Pool(pool_path))


        self.title("Сортировка групп")
        self.screen_width, self.screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        global pb_height, systemFont, bigButtonsFont, smallButtonsFont, numberFont
        if self.screen_width == 1280:
            self.spawn_x, self.spawn_y = -11, -1
            pb_height = 20
            systemFont = ('Trebuchet MS', 20, 'bold')
            bigButtonsFont = ('Trebuchet MS', 110, 'bold')
            smallButtonsFont = ('Trebuchet MS', 75, 'bold')
            numberFont = ('Trebuchet MS', 35, 'bold')
        else:
            pb_height = 30
            self.spawn_x, self.spawn_y = -8, -1
            systemFont = ('Trebuchet MS', 30, 'bold')
            numberFont = ('Trebuchet MS', 50, 'bold')
            bigButtonsFont = ('Trebuchet MS', 150, 'bold')
            smallButtonsFont = ('Trebuchet MS', 100, 'bold')
        self.geometry(f"{self.screen_width}x{self.screen_height}{self.spawn_x}{self.spawn_y}")
        self.resizable(False, False)

        # Image + wrapper
        self.current_club = self.ss.get_next_unclear_club()
        self.current_wrapper_color = GRAY
        if self.current_club is None:
            self.current_club = self.ss.clubs[-1]
            if self.ss.decisions[-1] == 'positive':
                self.current_wrapper_color = GREEN
            elif self.ss.decisions[-1] == 'negative':
                self.current_wrapper_color = RED
            else:
                print("Something went wrong. Please, contact the developer.")
                exit(-1)
        self.image_width = int(self.screen_width * ratio_image_width)
        self.image_height = int(self.image_width * 7 / 10)
        self.lImageWrapper = ctk.CTkLabel(self,
                                          width=int(self.image_width * 1.2),
                                          height=int(self.image_height * 1.2),
                                          fg_color=self.current_wrapper_color)
        self.lImageWrapper.place(relx=indentX_image-0.05, rely=0.5, anchor="w")
        self.image = ctk.CTkImage(dark_image=Image.open(f"screenshots/{self.current_club}.png"), size=(self.image_width, self.image_height))
        self.image_label = ctk.CTkLabel(self, image=self.image)
        self.image_label.place(relx=indentX_image, rely=0.5, anchor="w")

        # Image number
        self.no = self.ss.clubs.index(self.current_club) + 1
        indentY_wrapper_rel = 0.5 - self.image_height * 1.2 / self.screen_height / 2
        self.image_number = ctk.CTkLabel(self, font=numberFont, width=int(self.screen_width * 0.05), height=int(self.screen_height * 0.1), fg_color="black", text=str(self.no))
        self.image_number.place(relx=indentX_image-0.05, rely=indentY_wrapper_rel, anchor="nw")

        # Progress bar
        self.done = self.ss.calculate_progress()
        self.total = len(self.ss)
        self.pb_info = ctk.CTkLabel(self, font=systemFont, width=int(self.screen_width * 0.9), height=30, fg_color="transparent", text=f"✅  {self.done} / {self.total}  ✅")
        self.pb_info.place(relx=0.5, rely=0.03, anchor="center")
        self.pb_width = int(self.screen_width * 0.9)
        self.pb_background = ctk.CTkLabel(self, width=self.pb_width, height=pb_height, fg_color="white", text="")
        self.pb_background.place(relx=0.5, rely=0.075, anchor="center")
        self.pb_success_color = "#8b7500"
        self.pb_slider = ctk.CTkLabel(self, width=int(self.pb_width * self.done / self.total), height=pb_height, fg_color="black" if self.done != self.total else self.pb_success_color, text="")
        self.pb_slider.place(relx=0.05, rely=0.075, anchor="w")

        # Red button
        left_space = 0.3
        space_between_x, space_between_y = 0.01, 0.01 * self.screen_width / self.screen_height
        block_width_rel = (left_space - 0.02 - space_between_x) / 2
        block_height_rel = 0.2
        block_width = int(self.screen_width * block_width_rel)
        block_height = int(self.screen_height * block_height_rel)
        self.red_button = ctk.CTkButton(self,
                                        text="Удалить",
                                        width=block_width,
                                        height=block_height,
                                        fg_color=RED,
                                        hover_color="#780000",
                                        font=systemFont,
                                        command=self.pressed_red_button)
        self.red_button.place(relx=0.67, rely=indentY_wrapper_rel, anchor="nw")

        # Green button
        self.green_button = ctk.CTkButton(self,
                                          text="Оставить",
                                          width=block_width,
                                          height=block_height,
                                          fg_color=GREEN,
                                          hover_color="#31572c",
                                          font=systemFont,
                                          command=self.pressed_green_button)
        self.green_button.place(relx=0.67 + block_width_rel + space_between_x, rely=indentY_wrapper_rel, anchor="nw")

        # Big arrow buttons
        big_arrow_color = "#0080fe"
        self.big_arrow_left = ctk.CTkButton(self,
                                            text="<",
                                            fg_color=big_arrow_color,
                                            width=block_width,
                                            height=block_height,
                                            font=bigButtonsFont,
                                            command=self.pressed_big_arrow_left)
        self.big_arrow_left.place(relx=0.67, rely=indentY_wrapper_rel + block_height_rel + space_between_y, anchor="nw")
        self.big_arrow_right = ctk.CTkButton(self,
                                             text=">",
                                             fg_color=big_arrow_color,
                                             width=block_width,
                                             height=block_height,
                                             font=bigButtonsFont,
                                             command=self.pressed_big_arrow_right)
        self.big_arrow_right.place(relx=0.67 + block_width_rel + space_between_x, rely=indentY_wrapper_rel + block_height_rel + space_between_y, anchor="nw")
        
        # Small arrow buttons
        small_arrow_color = "#191970"
        small_arrow_hover_color = "#011627"
        self.small_arrow_left = ctk.CTkButton(self,
                                              text="<<",
                                              fg_color=small_arrow_color,
                                              hover_color=small_arrow_hover_color,
                                              width=block_width,
                                              height=block_height // 2,
                                              font=smallButtonsFont,
                                              command=self.pressed_small_arrow_left)
        self.small_arrow_left.place(relx=0.67, rely=indentY_wrapper_rel + block_height_rel * 2 + space_between_y * 2, anchor="nw")
        self.small_arrow_right = ctk.CTkButton(self,
                                               text=">>",
                                               fg_color=small_arrow_color,
                                               hover_color=small_arrow_hover_color,
                                               width=block_width,
                                               height=block_height // 2,
                                               font=smallButtonsFont,
                                               command=self.pressed_small_arrow_right)
        self.small_arrow_right.place(relx=0.67 + block_width_rel + space_between_x, rely=indentY_wrapper_rel + block_height_rel * 2 + space_between_y * 2, anchor="nw")

        # Exit button
        indentY_exit = 0.5 + self.image_height * 1.2 / self.screen_height / 2
        ctk.CTkButton(self, text="Выход", width=int(self.screen_width * (block_width_rel * 2 + space_between_x)), height=int(self.screen_width * block_width_rel / 4), font=systemFont, command=self.pressed_exit).place(relx=0.67, rely=indentY_exit, anchor="sw")

    def pressed_red_button(self):
        if self.current_wrapper_color == RED:
            self.ss.write_decision("unclear", self.no)
            self.current_wrapper_color = GRAY
            self.paint_wrapper()
        else:
            self.ss.write_decision("negative", self.no)
            next_possible_club = self.ss.get_next_unclear_club(self.no)
            if next_possible_club is None:
                self.current_wrapper_color = RED
                self.lImageWrapper.configure(fg_color=self.current_wrapper_color)
                self.ss.make_pool_file()
            else:
                self.current_club = next_possible_club
                self.no = self.ss.clubs.index(self.current_club) + 1
                self.update_image()
                self.update_image_number()
        self.update_progress_bar()
        self.ss.save()

    def pressed_green_button(self):
        if self.current_wrapper_color == GREEN:
            self.ss.write_decision("unclear", self.no)
            self.current_wrapper_color = GRAY
            self.paint_wrapper()
        else:
            self.ss.write_decision("positive", self.no)
            next_possible_club = self.ss.get_next_unclear_club(self.no)
            if next_possible_club is None:
                self.current_wrapper_color = GREEN
                self.lImageWrapper.configure(fg_color=self.current_wrapper_color)
                self.ss.make_pool_file()
            else:
                self.current_club = next_possible_club
                self.no = self.ss.clubs.index(self.current_club) + 1
                self.update_image()
                self.update_image_number()
        self.update_progress_bar()
        self.ss.save()


    def pressed_big_arrow_left(self):
        self.no -= 1
        if self.no < 1:
            self.no = len(self.ss)
        self.current_club = self.ss.clubs[self.no - 1]
        self.update_image_number()
        self.update_image()

    def pressed_big_arrow_right(self):
        self.no += 1
        if self.no > len(self.ss):
            self.no = 1
        self.current_club = self.ss.clubs[self.no - 1]
        self.update_image_number()
        self.update_image()
    
    def pressed_small_arrow_left(self):
        if self.current_wrapper_color == GRAY:
            return
        next_possible_club = self.ss.get_previous_unclear_club(self.no)
        if next_possible_club is not None:
            self.current_club = next_possible_club
            self.no = self.ss.clubs.index(self.current_club) + 1
            self.update_image()
            self.update_image_number()
    
    def pressed_small_arrow_right(self):
        if self.current_wrapper_color == GRAY:
            return
        next_possible_club = self.ss.get_next_unclear_club(self.no)
        if next_possible_club is not None:
            self.current_club = next_possible_club
            self.no = self.ss.clubs.index(self.current_club) + 1
            self.update_image()
            self.update_image_number()

    def paint_wrapper(self):
        self.lImageWrapper.configure(fg_color=self.current_wrapper_color)

    def pressed_exit(self):
        self.ss.save()
        self.destroy()

    def update_image(self):
        self.image = ctk.CTkImage(dark_image=Image.open(f"screenshots/{self.current_club}.png"), size=(self.image_width, self.image_height))
        self.image_label.configure(image=self.image)

    def update_image_number(self):
        self.image_number.configure(text=str(self.no))
        prev_wrapper_color = self.current_wrapper_color
        if self.ss.decisions[self.no - 1] == 'positive':
            self.current_wrapper_color = GREEN
        elif self.ss.decisions[self.no - 1] == 'negative':
            self.current_wrapper_color = RED
        elif self.ss.decisions[self.no - 1] == 'unclear':
            self.current_wrapper_color = GRAY
        if prev_wrapper_color != self.current_wrapper_color:
            self.paint_wrapper()

    def update_progress_bar(self):
        self.done = self.ss.calculate_progress()
        self.pb_slider.configure(width=int(self.pb_width * self.done / self.total))
        current_slider_color = self.pb_slider.cget("fg_color")
        if self.done == self.total and current_slider_color == "black":
            self.pb_slider.configure(fg_color=self.pb_success_color)
        elif self.done != self.total and current_slider_color != "black":
            self.pb_slider.configure(fg_color="black")
        self.pb_info.configure(text=f"✅  {self.done} / {self.total}  ✅")


root = App()
root.mainloop()
