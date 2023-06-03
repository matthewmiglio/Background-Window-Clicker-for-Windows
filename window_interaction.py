import ctypes
import win32con
import win32gui
import win32api
import win32process


def send_click_to_window(window_name, x, y, button="left"):
    # Get the handle of the currently active window
    active_window = win32gui.GetForegroundWindow()

    # Find the window based on the window name
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd == 0:
        print("Window not found.")
        return

    # Get the window's client area position
    left, top, right, bottom = win32gui.GetClientRect(hwnd)

    # Calculate the coordinates relative to the window
    click_x = left + x
    click_y = top + y

    # Convert coordinates to screen coordinates
    point = win32gui.ClientToScreen(hwnd, (click_x, click_y))
    click_x, click_y = point

    # Get the window's process ID and thread ID
    _, process_id = win32process.GetWindowThreadProcessId(hwnd)

    # Open the process with required permissions
    process_handle = win32api.OpenProcess(
        win32con.PROCESS_ALL_ACCESS, False, process_id
    )

    # Calculate the click position relative to the window's client area
    window_rect = win32gui.GetWindowRect(hwnd)
    client_rect = win32gui.GetClientRect(hwnd)
    client_offset_x = window_rect[2] - client_rect[2]
    client_offset_y = window_rect[3] - client_rect[3]
    click_x -= client_offset_x
    click_y -= client_offset_y

    # Send the click message to the window
    if button == "right":
        message = win32con.WM_RBUTTONDOWN, win32con.WM_RBUTTONUP
    elif button == "middle":
        message = win32con.WM_MBUTTONDOWN, win32con.WM_MBUTTONUP
    else:
        message = win32con.WM_LBUTTONDOWN, win32con.WM_LBUTTONUP

    ctypes.windll.user32.SendMessageW(
        hwnd, message[0], win32con.MK_LBUTTON, click_x + (click_y << 16)
    )
    ctypes.windll.user32.SendMessageW(hwnd, message[1], 0, click_x + (click_y << 16))

    # Restore focus to the previously active window
    win32gui.SetForegroundWindow(active_window)

    # Close the process handle
    win32api.CloseHandle(process_handle)


def list_window_names():
    def enum_window_callback(hwnd, window_names):
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            if window_title:
                window_names.append(window_title)

    window_names = []
    win32gui.EnumWindows(enum_window_callback, window_names)

    for n in window_names:
        print(n)


