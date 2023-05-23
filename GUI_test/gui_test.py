import dearpygui.dearpygui as dpg

def save_callback(sender, data):
    print("Save Clicked")

with dpg.handler_registry():
    @dpg.handler(dpg.mvEventType.mvEVT_COMMAND)
    def on_click(sender, app_data):
        save_callback(sender, app_data)

with dpg.window(label="Example Window"):
    dpg.add_text("Hello, world!")
    dpg.add_button("Save", callback=on_click)
    dpg.add_input_text("string")
    dpg.add_slider_float("float")

dpg.create_context()
dpg.create_viewport(title='Example Window', width=600, height=300)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
