# import sublime_plugin

# class My(sublime_plugin.EventListener):
#     def on_post_window_command(self, window, command_name, args):
#         print(command_name, args)

#         # if command_name == 'build':

#     def on_post_save(self, view):
#         window = view.window()
#         output_view = window.create_output_panel('exec')
#         if output_view.window():
#             errs = output_view.find_all_results()
#             # output_view.substr(sublime.Region(0, output_view.size()))
#             if len(errs) == 0:
#                 window.run_command("hide_panel", {"panel": "output.exec", cancel": True})
#             # print(output_panel.substr(sublime.Region(0, view.size())))
#             # window.run_command("show_panel", {"panel": "output.exec"})
