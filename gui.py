import logging
import tkinter as tk

from files import get_data


def prompt_user_data() -> tuple[str, str, str]:
    result: tuple[str, str, str] = ("", "", "")
    cancelled = True
    stopped = False

    def on_ok():
        nonlocal result, cancelled, stopped

        # Seems I need both of them??
        # popup_window.quit()
        popup_window.destroy()

        result = (token_var.get(), id_var.get(), port_var.get())
        cancelled = False
        stopped = True
        logging.info("OK pressed")

    popup_window = tk.Toplevel()
    popup_window.title("Enter Details")
    popup_window.geometry("300x269")

    token_var = tk.StringVar(popup_window)
    id_var = tk.StringVar(popup_window)
    port_var = tk.StringVar(popup_window)

    data = get_data()
    if data is None:
        logging.warn(
            "Could not open GUI cuz JSON was incorrect. Defaulting to blank values"
        )
    else:
        token_var.set(data.get("token", ""))
        id_var.set(data.get("user_id", ""))
        port_var.set(data.get("port", ""))

    title = tk.Label(popup_window, text="Enter/Edit your data.")
    title.pack(pady=(10, 0))

    token_label = tk.Label(popup_window, text="Bot Token")
    token_label.pack(pady=(10, 0))
    token_entry = tk.Entry(popup_window, show="*", textvariable=token_var)
    token_entry.pack(pady=(0, 10))

    user_id_label = tk.Label(popup_window, text="User ID")
    user_id_label.pack(pady=(10, 0))
    user_id_entry = tk.Entry(popup_window, textvariable=id_var)
    user_id_entry.pack(pady=(0, 10))

    port_label = tk.Label(popup_window, text="Port")
    port_label.pack(pady=(10, 0))
    port_entry = tk.Entry(popup_window, textvariable=port_var)
    port_entry.pack(pady=(0, 10))

    ok_button = tk.Button(popup_window, text="OK", command=on_ok)
    ok_button.pack(pady=10)

    def print_size():
        logging.debug(
            f"Window is {popup_window.winfo_width()}x{popup_window.winfo_height()}"
        )
        if stopped:
            return
        popup_window.after(1000, print_size)

    popup_window.after(0, print_size)
    popup_window.wait_window()
    stopped = True
    if cancelled:
        logging.info("Window closed without saving")
        raise Exception("Window has been closed without saving")
    logging.info("Window closed with OK")
    return result
