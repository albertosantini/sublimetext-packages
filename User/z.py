import sublime
import sublime_plugin
import re

import importlib
defaultExec = importlib.import_module("Default.exec")

class ExecCommand(defaultExec.ExecCommand):
    def on_finished(self, proc):
        super(ExecCommand, self).on_finished(proc)

        view = self.window.active_view()
        errs = self.output_view.find_all_results()

        if (len(errs) == 0 and proc.exit_code() == 0):
            self.window.run_command("hide_panel", {"cancel": True})
            view.erase_regions("exec_errors")

        else:
            regions = []

            for err in errs:
                line = int(err[1]) - 1
                line_begin = view.text_point(line, 0)
                line_region = view.full_line(line_begin)
                buf = view.substr(line_region)
                tab_length = len(re.findall("\t", buf))
                isSpacesIndentation = view.settings().get(
                    "translate_tabs_to_spaces")
                tab_size = 1
                if (not isSpacesIndentation):
                    tab_size = view.settings().get("tab_size")

                col = int(err[2]) - 1 - (tab_size * tab_length) + tab_length

                text_point = view.text_point(line, col)
                region = view.word(text_point)
                regions.append(region)

            view.add_regions("exec_errors", regions, "keyword", "dot",
                    sublime.DRAW_EMPTY |
                    sublime.DRAW_NO_FILL |
                    sublime.DRAW_NO_OUTLINE |
                    sublime.DRAW_SQUIGGLY_UNDERLINE |
                    sublime.HIDE_ON_MINIMAP)

class SublimeOnSaveBuild(sublime_plugin.EventListener):
    def on_post_save(self, view):
        filename_filter = "\\.(js|json|jshintrc|sublime-[\\w]+)$"
        if not re.search(filename_filter, view.file_name()):
            return

        view.window().run_command("build")
