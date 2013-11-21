import sublime
import Default

class ExecCommand(Default.exec.ExecCommand):
    def on_finished(self, proc):
        super(ExecCommand, self).on_finished(proc)

        errs = self.output_view.find_all_results()
        if len(errs) == 0:
            self.window.run_command("hide_panel", {"cancel": True})
            view = self.window.active_view()
            view.erase_regions("exec_errors")

        else:
            regions = []
            view = self.window.active_view()

            for err in errs:
                text_point = view.text_point(int(err[1]) - 1, int(err[2]) - 1)
                region = view.word(text_point)
                regions.append(region)

            view.add_regions("exec_errors", regions, "keyword", "dot",
                    sublime.DRAW_EMPTY |
                    sublime.DRAW_NO_FILL |
                    sublime.DRAW_NO_OUTLINE |
                    sublime.DRAW_SQUIGGLY_UNDERLINE |
                    sublime.HIDE_ON_MINIMAP)
