import sublime
import sublime_plugin
import re
import Default

class SublimeOnSaveBuild(sublime_plugin.EventListener):
    def on_post_save(self, view):
        filename_filter = "\\.(js)$"

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
