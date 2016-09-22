import sublime
import sublime_plugin
import re
import Default

# Credits to https://github.com/alexnj/SublimeOnSaveBuild
class SublimeOnSaveBuild(sublime_plugin.EventListener):
    def on_post_save(self, view):
        global_settings = sublime.load_settings(self.__class__.__name__+ ".sublime-settings")

        should_build = view.settings().get("build_on_save", global_settings.get("build_on_save", True))

        filename_filter = "\\.(js)$"

        if not should_build:
            return

        if not re.search(filename_filter, view.file_name()):
            return

        view.window().run_command("build")

class ExecCommand(Default.exec.ExecCommand):
    def on_finished(self, proc):
        super(ExecCommand, self).on_finished(proc)

        exit_code = proc.exit_code()
        errors_len = len(self.output_view.find_all_results())

        if (exit_code != None and exit_code != 0) or errors_len > 0:
            self.window.run_command("show_panel", {"panel": "output.exec"})
        else:
            self.window.run_command("hide_panel", {"panel": "output.exec"})
