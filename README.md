Sublime Text configuration
==========================

This repository contains the configuration of Sublime Text editor (ST3).

I have been using the following plugins:

- [Build Next](https://github.com/albertosantini/sublimetext-buildnext)
- [Dracula Color Scheme](http://zenorocha.github.io/dracula-theme/)
- [EasyMotion](https://github.com/tednaleid/sublime-EasyMotion)
- [ExportHtml](https://github.com/facelessuser/ExportHtml)
- [Git](https://github.com/kemayo/sublime-text-git)
- [Theme - Soda](http://buymeasoda.github.com/soda-theme/)

Then in `User/z.py`, if it exists, I added a few customizations.

Basically I have been programming in JavaScript (in Node.js and in the browers), HTML, CSS and R. Indeed there are some build setups and customizations (rulers, extensions, etc.) for those languages.

Installation
------------

Install [Package Control](https://sublime.wbond.net/installation) and stop the editor.

Then you should clone the repository in `Data/Packages` overwriting the folder.

`$ cd Data/Packages`

```
git init
git remote add origin https://github.com/albertosantini/sublimetext-packages.git
git fetch
git checkout -t origin/master
```

Restart the editor and the plugins will be installed automatically.
Maybe during the installation of the theme it is displayed an error: restart the editor again.

Notes
-----

Read also the note about the syncing: [Package Control Syncing](https://sublime.wbond.net/docs/syncing).
