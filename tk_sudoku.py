import random
import tkinter as tk
import tkinter.font as fnt

from sudoku import Sudoku
from tkinter import filedialog


def menu_ui() -> None:
    """Create the menu frame that appears when starting this program."""
    menu_frame = tk.Frame(root, borderwidth=1, relief=tk.SOLID,
                          padx=50, pady=50,
                          background=WHITE)
    menu_frame.grid(row=0, column=0)

    menu_label1 = tk.Label(menu_frame, text="Generate new Sudoku",
                           font=FONT_VERY_LARGE, foreground=COLOR1,
                           background=WHITE)
    menu_label1.grid(row=0, column=0, columnspan=2, sticky=tk.W)

    menu_difficulty_label = tk.Label(menu_frame, text="Difficulty",
                                     font=FONT_SMALL,
                                     background=WHITE)
    menu_difficulty_label.grid(row=1, column=0)

    difficulty = tk.DoubleVar()
    menu_difficulty_scale = tk.Scale(menu_frame, orient=tk.HORIZONTAL,
                                     from_=1, to=5, resolution=1,
                                     variable=difficulty, showvalue=False,
                                     background=COLOR2,
                                     troughcolor=COLOR2,
                                     activebackground=COLOR2_SHADE,
                                     highlightbackground=COLOR2_SHADE)
    menu_difficulty_scale.set(3)
    menu_difficulty_scale.grid(row=1, column=1)

    button_width = 18
    menu_generate_button = tk.Button(menu_frame, text="Generate New",
                                     justify=tk.CENTER, font=FONT_MEDIUM,
                                     width=button_width,
                                     background=COLOR2,
                                     foreground=WHITE,
                                     activebackground=COLOR2_SHADE,
                                     activeforeground=WHITE,
                                     takefocus=1,
                                     highlightcolor=COLOR2_SHADE,
                                     command=lambda: initialize_sudoku(menu_frame,
                                                                       difficulty.get()))
    menu_generate_button.grid(row=2, column=0, columnspan=2)

    menu_label2 = tk.Label(menu_frame, text="or", font=FONT_SMALL,
                           background=WHITE)
    menu_label2.grid(row=3, column=0, columnspan=2)

    menu_load_button = tk.Button(menu_frame,
                                 text="Load From File",
                                 justify=tk.CENTER, font=FONT_MEDIUM,
                                 width=button_width,
                                 background=COLOR2,
                                 foreground=WHITE,
                                 activebackground=COLOR2_SHADE,
                                 activeforeground=WHITE,
                                 command=lambda: load_from_file(menu_frame, False))
    menu_load_button.grid(row=4, column=0, columnspan=2)

    for child in menu_frame.winfo_children():
        child.grid_configure(padx=2.5, pady=5)

        if isinstance(child, tk.Button):
            child.bind("<Enter>", on_enter)
            child.bind("<Leave>", on_leave)


def sudoku_ui(unsolved_sudoku_board: list[list[int | None]],
              solved_sudoku_board: list[list[int | None]]) -> None:
    """Create the main sudoku window with all its functionality.

    Bonus: Keep track of remaining hearts and hints."""
    global elapsed_time
    global is_done
    global errors
    global hints
    elapsed_time = -1
    is_done = False
    errors = 0
    hints = 0

    global solved_sudoku_as_one_list
    solved_sudoku_as_one_list = [
        str(x) for sublist in solved_sudoku_board for x in sublist]
    unsolved_sudoku_as_one_list = [None if x is None else str(
        x) for sublist in unsolved_sudoku_board for x in sublist]

    global main_frame
    main_frame = tk.Frame(root, borderwidth=1, relief=tk.SOLID,
                          padx=40, pady=40, background=WHITE)
    main_frame.grid(row=0, column=0)

    global label_and_button_frame
    label_and_button_frame = tk.Frame(main_frame, background=WHITE)
    label_and_button_frame.grid(row=0, column=0, rowspan=2, columnspan=5)

    label_font = FONT_SMALL
    difficulty_level = get_difficulty_level(unsolved_sudoku_as_one_list)
    global game_difficulty_text
    game_difficulty_text = f"Difficulty = {difficulty_level}"
    game_difficulty_label = tk.Label(label_and_button_frame,
                                     text=game_difficulty_text,
                                     font=label_font,
                                     background=WHITE)
    game_difficulty_label.grid(row=0, column=0)
    game_timer_label = tk.Label(label_and_button_frame, text="Time: 00:00:00",
                                font=label_font,
                                background=WHITE)
    game_timer_label.grid(row=0, column=4)
    status_text = f"Hearts: {ERROR_THRESHOLD} | Hints: {HINT_THRESHOLD}"
    game_status_label = tk.Label(label_and_button_frame, text=status_text,
                                 font=label_font,
                                 background=WHITE)
    game_status_label.grid(row=0, column=1, columnspan=3)

    button_font = FONT_MEDIUM
    button_width = 13
    game_hint_button = tk.Button(label_and_button_frame, text="Get Hint",
                                 font=button_font, justify=tk.CENTER,
                                 width=button_width,
                                 background=COLOR2,
                                 foreground=WHITE,
                                 activebackground=COLOR2_SHADE,
                                 activeforeground=WHITE,
                                 command=get_hint)
    game_hint_button.grid(row=1, column=0)
    game_solution_button = tk.Button(label_and_button_frame, text="Show Solution",
                                     font=button_font, justify=tk.CENTER,
                                     width=button_width,
                                     background=COLOR2,
                                     foreground=WHITE,
                                     activebackground=COLOR2_SHADE,
                                     activeforeground=WHITE,
                                     command=show_solution)
    game_solution_button.grid(row=1, column=1)
    game_clear_button = tk.Button(label_and_button_frame, text="Clear Input",
                                  font=button_font, justify=tk.CENTER,
                                  width=button_width,
                                  background=COLOR2,
                                  foreground=WHITE,
                                  activebackground=COLOR2_SHADE,
                                  activeforeground=WHITE,
                                  command=clear_input)
    game_clear_button.grid(row=1, column=2)
    game_load_button = tk.Button(label_and_button_frame, text="Load From File",
                                 font=button_font, justify=tk.CENTER,
                                 width=button_width,
                                 background=COLOR2,
                                 foreground=WHITE,
                                 activebackground=COLOR2_SHADE,
                                 activeforeground=WHITE,
                                 command=lambda: confirmation_ui(True))
    game_load_button.grid(row=1, column=3)
    game_generate_button = tk.Button(label_and_button_frame, text="Generate New",
                                     font=button_font, justify=tk.CENTER,
                                     width=button_width,
                                     background=COLOR2,
                                     foreground=WHITE,
                                     activebackground=COLOR2_SHADE,
                                     activeforeground=WHITE,
                                     command=lambda: confirmation_ui())
    game_generate_button.grid(row=1, column=4)

    for child in label_and_button_frame.winfo_children():
        if isinstance(child, tk.Button):
            child.grid_configure(padx=3, pady=(10, 25))
            child.bind("<Enter>", on_enter)
            child.bind("<Leave>", on_leave)

    global entry_frame
    entry_frame = tk.Frame(main_frame, background=COLOR1)
    entry_frame.grid(row=2, column=0, columnspan=5)

    entries = []
    entry_width = 3
    for i in range(81):
        row = i // 9
        column = i % 9
        entry = tk.Entry(entry_frame, justify=tk.CENTER,
                         width=entry_width, font=FONT_ENTRY)
        entry.grid(row=row, column=column)
        entries.append(entry)

        # 1. fill sudoku blueprint with values
        # 2. add binding events
        if unsolved_sudoku_as_one_list[i] is None:
            true_input = str(solved_sudoku_as_one_list[i])
            entry.bind("<KeyRelease>",
                       lambda e, s=true_input: auto_check_input(e, s))
        else:
            entry.insert(0, str(unsolved_sudoku_as_one_list[i]))
            entry["state"] = tk.DISABLED

    for idx, child in enumerate(entry_frame.winfo_children()):
        padding = 7

        # top and bottom padding
        if idx < 9:
            child.grid_configure(pady=(padding, 0))
        elif idx > 71:
            child.grid_configure(pady=(0, padding))

        # left and right padding
        if idx % 9 == 0:
            child.grid_configure(padx=(padding, 0))
        elif idx % 9 == 8:
            child.grid_configure(padx=(0, padding))

        # right padding in between
        if idx % 9 == 2 or idx % 9 == 5:
            child.grid_configure(padx=(0, padding))

        # bottom padding in between
        if idx // 9 == 2 or idx // 9 == 5:
            child.grid_configure(pady=(0, padding))

    update_timer()


def confirmation_ui(from_file: bool = False):
    """Create a screen that asks a user for confirmation if they really
    want to load/generate a new sudoku."""
    frame = tk.Frame(root, borderwidth=1, relief=tk.SOLID, padx=50, pady=50,
                     background=BACKGROUND_COLOR)
    frame.grid(row=0, column=0)

    label = tk.Label(frame, text="Do you really want to quit?",
                     font=FONT_VERY_LARGE, foreground=COLOR1,
                     background=WHITE)
    label.grid(row=0, column=0, columnspan=2)

    sub_frame = tk.Frame(frame, background=BACKGROUND_COLOR)
    sub_frame.grid(row=1, column=0, columnspan=2)

    width = 10
    match from_file:
        case False:
            yes_button = tk.Button(sub_frame, text="Yes", font=FONT_MEDIUM,
                                   justify=tk.CENTER, width=width,
                                   background=COLOR2,
                                   foreground=WHITE,
                                   activebackground=COLOR2_SHADE,
                                   activeforeground=WHITE,
                                   command=lambda: difficulty_scale_ui(frame))
        case True:
            yes_button = tk.Button(sub_frame, text="Yes", font=FONT_MEDIUM,
                                   justify=tk.CENTER, width=width,
                                   background=COLOR2,
                                   foreground=WHITE,
                                   activebackground=COLOR2_SHADE,
                                   activeforeground=WHITE,
                                   command=lambda: load_from_file(frame, True))
    yes_button.grid(row=0, column=0)

    no_button = tk.Button(sub_frame, text="No", font=FONT_MEDIUM, width=width,
                          justify=tk.CENTER,
                          background=COLOR2,
                          foreground=WHITE,
                          activebackground=COLOR2_SHADE,
                          activeforeground=WHITE,
                          command=frame.destroy)
    no_button.grid(row=0, column=1)

    for child in sub_frame.winfo_children():
        child.grid_configure(padx=5, pady=(15, 20))

        if isinstance(child, tk.Button):
            child.bind("<Enter>", on_enter)
            child.bind("<Leave>", on_leave)

    # focus this frame and block interaction with sudoku frame until
    # user decided if she/he really wants to quit
    frame.focus()
    frame.grab_set()


def difficulty_scale_ui(old_frame: tk.Frame):
    """Let the user select the difficulty of the newly generated 
    Sudoku."""
    old_frame.destroy()
    main_frame.destroy()

    frame = tk.Frame(root, borderwidth=1, relief=tk.SOLID, padx=50, pady=50,
                     background=BACKGROUND_COLOR)
    frame.grid(row=0, column=0)

    label = tk.Label(frame, text="Select Difficulty",
                     font=FONT_VERY_LARGE, foreground=COLOR1,
                     background=WHITE)
    label.grid(row=0, column=0)

    difficulty = tk.DoubleVar()
    difficulty_scale = tk.Scale(frame, orient=tk.HORIZONTAL,
                                from_=1, to=5, resolution=1,
                                variable=difficulty, showvalue=False,
                                background=COLOR2,
                                troughcolor=COLOR2,
                                activebackground=COLOR2_SHADE,
                                highlightbackground=COLOR2_SHADE)
    difficulty_scale.set(3)
    difficulty_scale.grid(row=1, column=0)

    generate_button = tk.Button(frame, text="Generate New", font=FONT_MEDIUM,
                                justify=tk.CENTER, width=15,
                                background=COLOR2,
                                foreground=WHITE,
                                activebackground=COLOR2_SHADE,
                                activeforeground=WHITE,
                                command=lambda: initialize_sudoku(frame,
                                                                  difficulty.get()))
    generate_button.grid(row=2, column=0)

    for child in frame.winfo_children():
        if isinstance(child, tk.Button):
            child.grid_configure(pady=10)
            child.bind("<Enter>", on_enter)
            child.bind("<Leave>", on_leave)
        else:
            child.grid_configure(pady=5)


def on_enter(e):
    """Change the background color when hovering over a Button.

    Only when button is not disabled."""
    if e.widget["state"] != tk.DISABLED:
        e.widget['background'] = COLOR2_SHADE


def on_leave(e):
    """Reset the background color when not hovering over a Button 
    anymore.

    Only when button is not disabled."""
    if e.widget["state"] != tk.DISABLED:
        e.widget['background'] = COLOR2


def initialize_sudoku(frame: tk.Frame, difficulty: float) -> None:
    """Initialize the sudoku UI with the given difficulty.

    Sudoku can only be made with difficulty values greater than 0 and 
    lower than 1, therefore it is necessary to change the difficulty
    values when they are provided via a scale."""
    frame.destroy()

    difficulty = convert_slider_difficulty(difficulty)

    global solution_count
    generated_sudoku_count = 1
    while True:
        solution_count = 0
        unsolved_sudoku = Sudoku(3, seed=random.randint(
            1, 1_000_000)).difficulty(difficulty)
        solve_and_count_solutions(unsolved_sudoku.board)

        # found a sudoku that has only a single solution
        if solution_count == 1:
            break
        print(
            f"Generated Sudoku {generated_sudoku_count} had multiple solutions.")
        generated_sudoku_count += 1

    solved_sudoku = unsolved_sudoku.solve()
    sudoku_ui(unsolved_sudoku.board, solved_sudoku.board)


def solve_and_count_solutions(board):
    global solution_count
    if solution_count > 1:
        return

    for y in range(9):
        for x in range(9):
            if board[y][x] is None:
                for n in range(1, 10):
                    if possible_value_for_cell(y, x, n, board):
                        board[y][x] = n
                        solve_and_count_solutions(board)
                        board[y][x] = None
                return
    solution_count += 1


def possible_value_for_cell(y, x, n, board):
    """Check whether a given value is possible in the given cell."""
    # check row
    for i in range(9):
        if board[y][i] == n:
            return False

    # check column
    for i in range(9):
        if board[i][x] == n:
            return False

    # check square
    y0 = (y//3) * 3
    x0 = (x//3) * 3
    for i in range(3):
        for j in range(3):
            if board[y0+i][x0+j] == n:
                return False
    return True


def convert_slider_difficulty(difficulty: float) -> float:
    """Convert the selected slider position into a difficulty that makes
    sense for a Sudoku.

    Based on ChatGPT suggestion and the fact that generating very hard
    Sudokus with a single solution takes ages.
    0.39 -> 31 cells unfilled -> 50 cells filled
    0.45 -> 36 cells unfilled -> 45 cells filled
    0.51 -> 41 cells unfilled -> 40 cells filled
    0.57 -> 46 cells unfilled -> 35 cells filled
    0.63 -> 51 cells unfilled -> 30 cells filled
    """
    match difficulty:
        case 1:
            difficulty = DIFFICULTIES[0]
        case 2:
            difficulty = DIFFICULTIES[1]
        case 3:
            difficulty = DIFFICULTIES[2]
        case 4:
            difficulty = DIFFICULTIES[3]
        case 5:
            difficulty = DIFFICULTIES[4]
    return difficulty


def get_difficulty_level(unsolved_sudoku_as_one_list) -> str:
    """Get the difficulty level by checking how many cells are empty."""
    filled_cells = 0
    for value in unsolved_sudoku_as_one_list:
        if value is not None:
            filled_cells += 1

    difficulty_level = ""
    if filled_cells <= 30:
        difficulty_level = "Very Hard"
    elif filled_cells <= 35:
        difficulty_level = "Hard"
    elif filled_cells <= 40:
        difficulty_level = "Medium"
    elif filled_cells <= 45:
        difficulty_level = "Easy"
    else:
        difficulty_level = "Very Easy"

    return difficulty_level


def auto_check_input(event: tk.Event, true_input: str) -> None:
    """Automatically validate inputs and give user instant feedback.

    Bonus: Keep track of errors and if user has too many errors lock
    UI."""
    entry = event.widget
    current_value = entry.get()
    if current_value not in ALLOWED_CHARS:
        entry.delete(0, tk.END)
        entry["background"] = DEFAULT_ENTRY_COLOR
    elif current_value == "":
        entry["background"] = DEFAULT_ENTRY_COLOR
    elif current_value == true_input:
        entry["background"] = DEFAULT_ENTRY_COLOR
        if check_sudoku_solved():
            lock_game_ui(SUCCESS_MESSAGE, SUCCESS_COLOR)
    else:
        entry["background"] = FAIL_COLOR
        global errors
        errors += 1
        update_status_label()

    if errors >= ERROR_THRESHOLD:
        global is_done
        is_done = True
        lock_game_ui(FAIL_MESSAGE, FAIL_COLOR)


def get_hint() -> None:
    """Users can ask for a hint, if they get stuck. The hint is the
    correct value for one of the EMPTY cells.

    Bonus: Keep track of how many hints remain. If user has used
    the threshold disable button."""
    global hints
    hints += 1

    entries = [entry for entry in entry_frame.winfo_children()
               if isinstance(entry, tk.Entry)]
    current_board = get_current_board()
    if "" in current_board:
        indexes = [idx for idx, value in enumerate(
            current_board) if value == ""]
        random_index = random.choice(indexes)
        entries[random_index].insert(
            0, solved_sudoku_as_one_list[random_index])
        update_status_label()

        # change the background of the hint to highlight it more
        # and remove it after x milliseconds
        entries[random_index]["background"] = COLOR2
        entries[random_index].after(
            1000, lambda e=entries[random_index]: e.configure(background=BACKGROUND_COLOR))

        # check if sudoku is now solved
        if check_sudoku_solved():
            lock_game_ui(SUCCESS_MESSAGE, SUCCESS_COLOR)

    if hints == HINT_THRESHOLD:
        for button in label_and_button_frame.winfo_children():
            if isinstance(button, tk.Button) and button.cget("text") == "Get Hint":
                button["background"] = BUTTON_DISABLED_COLOR
                button["state"] = tk.DISABLED
                break


def show_solution() -> None:
    """Show the solution to this sudoku and lock the UI."""
    for idx, entry in enumerate(entry_frame.winfo_children()):
        if isinstance(entry, tk.Entry) and entry["state"] == tk.NORMAL:
            entry.delete(0, tk.END)
            entry["background"] = DEFAULT_ENTRY_COLOR
            entry.insert(0, solved_sudoku_as_one_list[idx])
    if check_sudoku_solved():
        lock_game_ui(FAIL_MESSAGE, FAIL_COLOR)


def clear_input() -> None:
    """Clear all the user inputs so far and reset colors."""
    for entry in entry_frame.winfo_children():
        if isinstance(entry, tk.Entry) and entry["state"] == tk.NORMAL:
            entry.delete(0, tk.END)
            entry["background"] = DEFAULT_ENTRY_COLOR


def load_from_file(frame: tk.Frame, from_confirmation_ui: bool) -> None:
    """Load a possible sudoku grid from file and check if it is 
    compatible with the expected format and can be solved."""
    frame.destroy()
    if from_confirmation_ui:
        main_frame.destroy()

    path = filedialog.askopenfilename()

    wrong_file = "Wrong Path/File\n"\
        + f"{path} is not a valid '.txt' file.\nFile has to be a '.txt' "\
        + "file with exactly 9 lines, each containing "\
        + "exactly 9 chars [0-9]. 0 represents an empty field."

    unsolvable_sudoku = "Unsolvable Sudoku\n"\
        + f"{path} contains an unsolvable Sudoku."

    if not path:
        root.destroy()
        raise Exception(wrong_file)

    with open(path, "r") as file:
        content = [l.strip() for l in file.readlines()]
        if file_validation(content):
            board = [[None if char == '0' else int(
                char) for char in s] for s in content]

            # use the loaded sudoku to create an instance of Sudoku class
            unsolved_sudoku = Sudoku(3, 3, board=board)
            try:
                solved_sudoku = unsolved_sudoku.solve(True)

                global solution_count
                solution_count = 0
                solve_and_count_solutions(unsolved_sudoku.board)
                if solution_count == 1:
                    print("Sudoku from file has a single solution.")
                else:
                    print("Sudoku from file has multiple solutions.")

                sudoku_ui(unsolved_sudoku.board, solved_sudoku.board)
            except Exception:
                root.destroy()
                raise Exception(unsolvable_sudoku)

        else:
            root.destroy()
            raise Exception(wrong_file)


def file_validation(content: list) -> bool:
    """Perform some basic file content validation.

    The file has to be a .txt file with exactly 9 lines, each containing
    exactly 9 numbers in the range [0-9]. 0 represents an empty field."""
    if not isinstance(content, list):
        return False

    # check that we have 9 lines
    if len(content) != 9:
        return False

    # check that we have 9 items per line
    length_per_line = [len(l) for l in content]
    if length_per_line.count(9) != 9:
        return False

    # check that we have only numbers from 0 to 9
    for line in content:
        for char in line:
            if char not in ALLOWED_CHARS_FOR_FILE:
                return False

    return True


def update_status_label() -> None:
    """Update the status label with the remaining hearts and hints."""
    for child in label_and_button_frame.winfo_children():
        if isinstance(child, tk.Label) and child.cget("text")[0:6] == "Hearts":
            child["text"] = f"Hearts: {ERROR_THRESHOLD - errors} | Hints: {HINT_THRESHOLD - hints}"


def check_sudoku_solved() -> bool:
    """Check if the sudoku has been solved."""
    if get_current_board() == solved_sudoku_as_one_list:
        global is_done
        is_done = True
        return True
    return False


def lock_game_ui(message: str, color: str):
    """Lock most of the game UI widgets after sudoku is solved.

    Bonus: If ERROR_THRESHOLD is reached or user pressed on 
    "show solution" display a different message."""
    unlocked_buttons = ["Load From File", "Generate New"]
    for child in label_and_button_frame.winfo_children():
        if isinstance(child, tk.Button):
            if child.cget("text") not in unlocked_buttons:
                child["background"] = BUTTON_DISABLED_COLOR
                child["state"] = tk.DISABLED

        elif isinstance(child, tk.Label):
            child["foreground"] = WHITE
            child["background"] = color
            if child.cget("text") == game_difficulty_text:
                child["text"] = message

    for entry in entry_frame.winfo_children():
        entry["state"] = tk.DISABLED


def update_timer() -> None:
    """Update the timer. This gets executed every 1000 milliseconds and
    therefore works like a stopwatch."""
    if not is_done:
        global elapsed_time
        elapsed_time += 1

        # get correct format
        hours = elapsed_time // 3600
        minutes = (elapsed_time % 3600) // 60
        seconds = elapsed_time % 60
        for child in label_and_button_frame.winfo_children():
            if isinstance(child, tk.Label)\
                    and child.cget("text")[0:4] == "Time":
                child["text"] = f"Time: {hours:02}:{minutes:02}:{seconds:02}"

        # Schedule the function to run again after 1000ms (1 second)
        main_frame.after(1000, update_timer)


def get_current_board() -> list[str]:
    """Return the current state of the board"""
    return [entry.get() for entry in entry_frame.winfo_children() if isinstance(entry, tk.Entry)]


if __name__ == "__main__":
    root = tk.Tk()

    solution_count = 0

    FAIL_MESSAGE = "You can do better!"
    SUCCESS_MESSAGE = "Good job!"
    ALLOWED_CHARS = [str(x) for x in range(1, 10)]
    ALLOWED_CHARS_FOR_FILE = [str(x) for x in range(0, 10)]
    DIFFICULTIES = [0.39, 0.45, 0.51, 0.57, 0.63]
    ERROR_THRESHOLD = 3
    HINT_THRESHOLD = 3

    FONT_VERY_SMALL = fnt.Font(family="Arial", size=10)
    FONT_SMALL = fnt.Font(family="Arial", size=12, weight="bold")
    FONT_MEDIUM = fnt.Font(family="Arial", size=14, weight="bold")
    FONT_LARGE = fnt.Font(family="Arial", size=16, weight="bold")
    FONT_VERY_LARGE = fnt.Font(family="Arial", size=18, weight="bold")
    FONT_ENTRY = fnt.Font(family="Arial", size=26, weight="bold")

    BACKGROUND_COLOR = "white"
    COLOR1 = "#264653"
    COLOR2 = "#2A9D8F"
    COLOR2_SHADE = "#228176"
    COLOR3 = "#E9C46A"
    COLOR4 = "#F4A261"
    COLOR5 = "#E76F51"
    WHITE = "white"
    BLACK = "black"
    DEFAULT_ENTRY_COLOR = "SystemWindow"
    BUTTON_DISABLED_COLOR = "darkgray"
    FAIL_COLOR = COLOR5
    SUCCESS_COLOR = COLOR2

    root.title("Play Sudoku")
    root["background"] = COLOR3

    # start root fullscreen and add keybindings to get out of fullscreen
    # and back into it
    root.state("zoomed")
    root.bind("<Escape>", lambda event: root.state("normal"))
    root.bind("<F11>", lambda event: root.state("zoomed"))

    root.columnconfigure(index=0, weight=1)
    root.rowconfigure(index=0, weight=1)

    menu_ui()
    root.mainloop()
