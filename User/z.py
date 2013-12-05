import sublime
import sublime_plugin
import re

import importlib
defaultExec = importlib.import_module("Default.exec")

output_error_messages = []

class ExecCommand(defaultExec.ExecCommand):
    def on_finished(self, proc):
        super(ExecCommand, self).on_finished(proc)

        output_view = self.output_view

        view = self.window.active_view()
        errs = output_view.find_all_results()

        if (len(errs) == 0 and proc.exit_code() == 0):
            self.window.run_command("hide_panel", {"cancel": True})
            view.erase_regions("exec_errors")

        else:
            regions = []

            global output_error_messages
            output_error_messages = self.getErrorMessages(output_view)

            for err in errs:
                region = self.getAdjustedRegion(err[1], err[2])
                regions.append(region)

            view.add_regions("exec_errors", regions, "keyword", "dot",
                    sublime.DRAW_EMPTY |
                    sublime.DRAW_NO_FILL |
                    sublime.DRAW_NO_OUTLINE |
                    sublime.DRAW_SQUIGGLY_UNDERLINE |
                    sublime.HIDE_ON_MINIMAP)

    def getAdjustedRegion(self, line, col):
        line = int(line) - 1
        view = self.window.active_view()
        settings = view.settings()
        line_begin = view.text_point(line, 0)
        line_region = view.full_line(line_begin)
        buf = view.substr(line_region)
        tab_length = len(re.findall("\t", buf))
        isSpacesIndentation = settings.get("translate_tabs_to_spaces")
        tab_size = 1
        if (not isSpacesIndentation):
            tab_size = settings.get("tab_size")
        col = int(col) - 1 - (tab_size * tab_length) + tab_length
        text_point = view.text_point(line, col)
        region = view.word(text_point)
        region.b = text_point

        return region

    def getErrorMessages(self, view):
        view_error_messages = []
        file_regex = str(view.settings().get("result_file_regex"))
        group_regex = 3
        err_regions = view.find_all(file_regex)
        for err_region in err_regions:
            buf = str(view.substr(err_region))
            error = re.findall(file_regex, buf)[0]
            message = error[group_regex]
            view_error_messages.append(message)

        return view_error_messages

class SublimeOnSaveBuild(sublime_plugin.EventListener):
    def on_post_save(self, view):
        filename_filter = "\\.(js|json|jshintrc|sublime-[\\w]+)$"
        if not re.search(filename_filter, view.file_name()):
            return

        view.window().run_command("build")

class GotoError(sublime_plugin.TextCommand):
    def run(self, edit, direction):
        global output_error_messages

        if (len(output_error_messages) == 0):
            return

        err_messages = output_error_messages
        err_regions = self.view.get_regions("exec_errors")
        err_len = len(err_regions)

        if (err_len == 0):
            return


        if (direction == "prev"):
            err_messages = [item for item in reversed(err_messages)]
            err_regions = [item for item in reversed(err_regions)]

        caret = self.view.sel()[0].begin()
        for index, err_region in enumerate(err_regions):
            err_region_end = err_region.end()
            if ((direction == "next" and (caret < err_region_end)) or
                (direction == "prev" and (caret > err_region_end))):
                self.setCaret(err_region_end)
                sublime.status_message(err_messages[index])
                break

        err_last = err_regions[err_len - 1]
        caret_new = self.view.sel()[0].begin()
        if ((direction == "next" and (caret_new > err_last.end())) or
            (direction == "prev" and (caret_new < err_last.end())) or
            caret_new == caret):
            self.setCaret(err_regions[0].end())
            sublime.status_message(err_messages[0])

    def setCaret(self, position):
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(position, position))
        self.view.show_at_center(position)

class GotoNextError(GotoError):
    def run(self, edit):
        super(GotoNextError, self).run(edit, "next")

class GotoPrevError(GotoError):
    def run(self, edit):
        super(GotoPrevError, self).run(edit, "prev")
