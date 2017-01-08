"""Custom settings for Sublime Text."""

import sublime_plugin
import re
import Default

from os import path

node_modules_bin_path = None


class SublimeOnSaveBuild(sublime_plugin.EventListener):

    """Build the view on save if the view is a js file."""

    def __init__(self):
        """Set filename filter."""

        self.filename_filter = "\\.(js)$"

    def on_post_save(self, view):
        """After saving, check the type file and finally build it."""

        if not re.search(self.filename_filter, view.file_name()):
            return

        self.set_node_modules_bin_path(view)
        view.window().run_command("build")

    def set_node_modules_bin_path(self, view):
        """Set node_modules_bin_path for the current file."""

        global node_modules_bin_path

        curr_file = view.file_name()

        if curr_file:
            cwd = path.dirname(curr_file)

            if cwd:
                node_modules_bin_path = self.rev_parse_bin_path(cwd)

    def rev_parse_bin_path(self, cwd):

        """
        Search parent directories for package.json.
        Starting at the current working directory. Go up one directory
        at a time checking if that directory contains a package.json
        file. If it does, return that directory.
        """

        name = "package.json"
        package_path = path.normpath(path.join(cwd, name))

        bin_path = path.join(cwd, "node_modules/.bin/")

        if path.isfile(package_path) and path.isdir(bin_path):
            return bin_path

        parent = path.normpath(path.join(cwd, "../"))

        if parent == "/" or parent == cwd:
            return None

        return self.rev_parse_bin_path(parent)


class ExecCommand(Default.exec.ExecCommand):

    """Extend exec command using local eslint."""

    def run(self, cmd=None, shell_cmd=None,
            file_regex="", line_regex="", working_dir="",
            encoding="utf-8", env={}, quiet=False, kill=False,
            update_phantoms_only=False, hide_phantoms_only=False,
            word_wrap=True, syntax="Packages/Text/Plain text.tmLanguage",
            # Catches "path" and "shell"
            **kwargs):
        """Run the text command."""

        global node_modules_bin_path

        super(ExecCommand, self).run(cmd, shell_cmd,
                                     file_regex, line_regex,
                                     working_dir, encoding, env, quiet, kill,
                                     update_phantoms_only, hide_phantoms_only,
                                     word_wrap, syntax,
                                     **kwargs)

    def on_finished(self, proc):
        """Close the output panel if there are not errors."""

        super(ExecCommand, self).on_finished(proc)

        exit_code = proc.exit_code()
        errors_len = len(self.output_view.find_all_results())

        if (exit_code is not None and exit_code != 0) or errors_len > 0:
            self.window.run_command("show_panel", {"panel": "output.exec"})
        else:
            self.window.run_command("hide_panel", {"panel": "output.exec"})
