from window_interaction import list_window_names, send_click_to_window


# method for listing the names of windows that are active
def print_all_window_names():
    list_window_names()


# method for clicking a window in the background
def click():
    window_name = "Your Window Name"
    x = 500
    y = 200
    button = "right"  # left, middle

    send_click_to_window(window_name, x, y, button)
