Sublime Text configuration
==========================

This repository contains the configuration of Sublime Text editor (ST3).

I have been using the following plugins:

- [Dracula Color Scheme](http://zenorocha.github.io/dracula-theme/)
- [EasyMotion](https://github.com/tednaleid/sublime-EasyMotion)
- [ExportHtml](https://github.com/facelessuser/ExportHtml)
- [Git](https://github.com/kemayo/sublime-text-git)
- [Open-Include](https://github.com/SublimeText/Open-Include)
- [Theme - Soda](http://buymeasoda.github.com/soda-theme/)

Then in `User/z.py` I added a few customizations:

- Build on save for a few files.
- Close build results view if there are not errors.
- Show a dot icon in the gutter area if there is an error.

Note
----

You should clone the repository in `Data/Packages` overwriting the folder.

Don't forget to install [Package Control](https://sublime.wbond.net/), after
cloning the repo, and to restart the editor: the plugins will be installed
automatically.

Read also the note about the syncing: [Package Control Syncing](https://sublime.wbond.net/docs/syncing).
