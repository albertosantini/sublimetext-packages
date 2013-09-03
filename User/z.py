import sublime_plugin

class My(sublime_plugin.EventListener):
    def on_post_window_command(self, window, command_name, args):
            print(command_name, args)

            # if command_name == 'build':
            #     output_panel = window.get_output_panel('exec')
            #     errs = output_panel.find_all_results()
            #     # print('Errors: ' + str(len(errs)))
            #     if len(errs) == 0:
            #         output_panel.run_command('hide_panel', {'panel': 'output.exec'})

    # def on_post_text_command(self, window, command_name, args):
    #         print(command_name, args)