import tkinter as tk

def prompt_user_data():
    result: list[tuple[str, str]] = []

    def on_ok():
        token_value = token_entry.get()
        user_id_value = user_id_entry.get()
        popup_window.destroy()
        result.append((token_value, user_id_value))

    popup_window = tk.Tk()
    popup_window.title("Enter Details")
    popup_window.geometry("300x150")

    token_label = tk.Label(popup_window, text="Token")
    token_label.pack(pady=(10, 0))
    token_entry = tk.Entry(popup_window)
    token_entry.pack(pady=(0, 10))

    user_id_label = tk.Label(popup_window, text="User ID")
    user_id_label.pack(pady=(10, 0))
    user_id_entry = tk.Entry(popup_window)
    user_id_entry.pack(pady=(0, 10))

    ok_button = tk.Button(popup_window, text="OK", command=on_ok)
    ok_button.pack(pady=10)

    popup_window.grab_set()
    popup_window.mainloop()
    return result[0] if result else (None, None)
