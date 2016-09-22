import sublime
import sublime_plugin
import re

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
