import sublime
import sublime_plugin
import re

import importlib
defaultExec = importlib.import_module("Default.exec")

output_errors = {}

class ExecCommand(defaultExec.ExecCommand):
    def on_finished(self, proc):
        global output_errors

        super(ExecCommand, self).on_finished(proc)

        view = self.window.active_view()
        output_view = self.output_view
        errs = output_view.find_all_results()

        key = sublime.active_window().active_view().file_name()
        key.replace("\\","/")

        if (len(errs) == 0 and proc.exit_code() == 0):
            self.window.run_command("hide_panel", {"cancel": True})
            view.erase_regions("exec_errors")
            del output_errors[key]

        else:
            output_errors[key] = self.getErrors(output_view)

            regions = output_errors[key]["error_regions"]
            view.add_regions("exec_errors", regions, "keyword", "dot",
                    sublime.DRAW_EMPTY_AS_OVERWRITE |
                    sublime.DRAW_NO_FILL |
                    sublime.DRAW_NO_OUTLINE |
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
        region = sublime.Region(text_point, text_point)

        return region

    def getErrors(self, view):
        view_errors = {
            "view": view,
            "errors": [],
            "error_regions": [],
            "error_messages": [],
            "output_regions": []
        }

        file_regex = str(view.settings().get("result_file_regex"))
        err_regions = view.find_all(file_regex)
        for err_region in err_regions:
            buf = str(view.substr(err_region))
            error = re.findall(file_regex, buf)[0]
            region = self.getAdjustedRegion(error[1], error[2])
            message = error[3]
            view_errors["errors"].append((region, message, err_region))

        view_errors["errors"] = sorted(view_errors["errors"])

        for i, error in enumerate(view_errors["errors"]):
            view_errors["error_regions"].append(view_errors["errors"][i][0])
            view_errors["error_messages"].append(view_errors["errors"][i][1])
            view_errors["output_regions"].append(view_errors["errors"][i][2])

        return view_errors

class SublimeOnSaveBuild(sublime_plugin.EventListener):
    def on_post_save(self, view):
        filename_filter = "\\.(js|json|jshintrc|sublime-[\\w]+)$"
        if not re.search(filename_filter, view.file_name()):
            return

        view.window().run_command("build")

class GotoError(sublime_plugin.TextCommand):
    def run(self, edit, direction):
        global output_errors

        key = sublime.active_window().active_view().file_name()
        key.replace("\\","/")

        if (key not in output_errors):
            return;

        output_view = output_errors[key]["view"]
        error_regions = output_errors[key]["error_regions"]
        error_messages = output_errors[key]["error_messages"]
        output_regions = output_errors[key]["output_regions"]

        if (len(error_regions) == 0):
            return

        if (direction == "prev"):
            error_messages = [x for x in reversed(error_messages)]
            output_regions = [x for x in reversed(output_regions)]
            error_regions = [x for x in reversed(error_regions)]

        caret = self.view.sel()[0].begin()
        for i, err_region in enumerate(error_regions):
            err_region_end = err_region.end()
            if ((direction == "next" and (caret < err_region_end)) or
                (direction == "prev" and (caret > err_region_end))):
                self.updateEditAndOutputView(output_view,
                    error_regions[i], error_messages[i], output_regions[i])
                break
        else:
            self.updateEditAndOutputView(output_view,
                error_regions[0], error_messages[0], output_regions[0])

    def updateEditAndOutputView(self, view, region, message, output):
        self.highlightBuildError(view, output)
        sublime.status_message(message)
        self.setCaret(self.view, region)

    def setCaret(self, view, position):
        view.sel().clear()
        view.sel().add(sublime.Region(position.begin(), position.end()))
        view.show_at_center(position.end())

    def highlightBuildError(self, view, position):
        self.setCaret(view, position)
        sublime.active_window().run_command("hide_panel", {"cancel": True})
        sublime.active_window().run_command("show_panel",
            {"panel": "output.exec"})

class GotoNextError(GotoError):
    def run(self, edit):
        super(GotoNextError, self).run(edit, "next")

class GotoPrevError(GotoError):
    def run(self, edit):
        super(GotoPrevError, self).run(edit, "prev")
