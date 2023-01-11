from tkinter import *

# ---------------------------- CONSTANTS --------------------------------- #
PINK = "#DE714E"
RED = "#F1583F"
GREEN = "#379B46"
YELLOW = "#f7f5dd"
FONT = ("Courier", 24, "bold")
BG = YELLOW

WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

REPS_TO_DO = 4
reps_done = 0
breaks_done = 0
timer = None
timer_active = False


# ---------------------------- TIMER RESET ------------------------------- #
def reset():
    global reps_done, breaks_done, timer, timer_active
    window.after_cancel(timer)
    reps_done = 0
    breaks_done = 0
    update_status("Timer", GREEN)
    canvas.itemconfig(timer_text, text="00:00")
    timer_active = False


# ---------------------------- TIMER MECHANISM --------------------------- #
def start():
    global timer_active, reps_done, breaks_done
    if timer_active:
        return
    if reps_done < REPS_TO_DO and reps_done == breaks_done:
        update_status("Work", GREEN)
        start_timer(WORK_MIN)
    else:
        # set break timer
        if reps_done != REPS_TO_DO:
            update_status("Break", PINK)
            start_timer(SHORT_BREAK_MIN)
        else:
            update_status("Long Break", RED)
            start_timer(LONG_BREAK_MIN)


def start_timer(length):
    global timer_active
    timer_active = True
    count_down(length * 60)
    # use this one for testing with seconds
    # count_down(length)


# ---------------------------- COUNTDOWN MECHANISM ----------------------- #
def count_down(total_seconds):
    global reps_done, breaks_done, timer
    if breaks_done == REPS_TO_DO:
        return

    minutes = total_seconds // 60
    seconds = total_seconds % 60
    time = f"{minutes:02d}:{seconds:02d}"

    if total_seconds >= 0:
        canvas.itemconfig(timer_text, text=time)
        timer = window.after(1000, count_down, total_seconds - 1)
    else:
        window.bell()
        bring_to_front()
        if reps_done == breaks_done:
            reps_done += 1
        else:
            breaks_done += 1
        start()


# ---------------------------- UI SETUP ---------------------------------- #
def get_checks():
    global reps_done
    checked = "🗹"
    unchecked = "-"
    checks = ""
    for i in range(REPS_TO_DO):
        if i < reps_done:
            checks += checked
        else:
            checks += unchecked
    return checks


def update_status(label_text, color):
    status_label.config(text=label_text, fg=color)
    reps_label.config(text=get_checks())


def bring_to_front():
    # Restore if window is minimized
    window.state("normal")
    # Bring to top level above all windows
    window.attributes("-topmost", True)
    # Allows other windows to top level again
    window.attributes("-topmost", False)


window = Tk()
window.title("Pomodoro Timer")
window.config(padx=25, pady=25, bg=BG)

width = 225
height = 225

status_label = Label(text="Timer", fg=GREEN, bg=BG, font=FONT)
status_label.grid(column=1, row=0)

canvas = Canvas(width=width, height=height, bg=BG, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(width / 2, height / 2, image=tomato_img)
timer_text = canvas.create_text(width / 2, height / 1.66, text="00:00", fill="white", font=FONT)
canvas.grid(column=1, row=1)

reps_label = Label(text=f"{get_checks()}", fg=GREEN, bg=BG, font=FONT)
reps_label.grid(column=1, row=2, pady=15)

start_button = Button(text="Start", padx=10, pady=5, highlightthickness=0, command=start)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", padx=10, pady=5, highlightthickness=0, command=reset)
reset_button.grid(column=2, row=2)

window.mainloop()
