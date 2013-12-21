Sublime Text configuration
==========================

This repository contains the configuration of Sublime Text editor (ST3).

I have been using the following plugins:

- [Build Next](https://github.com/albertosantini/sublimetext-buildnext)
- [Dracula Color Scheme](http://zenorocha.github.io/dracula-theme/)
- [EasyMotion](https://github.com/tednaleid/sublime-EasyMotion)
- [ExportHtml](https://github.com/facelessuser/ExportHtml)
- [Git](https://github.com/kemayo/sublime-text-git)
- [Open-Include](https://github.com/SublimeText/Open-Include)
- [Theme - Soda](http://buymeasoda.github.com/soda-theme/)

Then in `User/z.py`, if it exists, I added a few customizations.

Basically I have been programming in JavaScript (in Node.js and in the browers), HTML, CSS and R. Indeed there are some build setups and customizations (rulers, extensions, etc.) for those languages.

Installation
------------

Starting from a fresh ST installation, install [Package Control](https://sublime.wbond.net/installation) and quit the editor.

Use the link of your forked repo in the commands below (or you may use the mine).

Then you should clone the repository  in `Data/Packages`.

```
$ cd Data/Packages
$ git init
$ git remote add origin git@github.com:albertosantini/sublimetext-packages.git
$ git fetch
$ git checkout -t origin/master
```

There is another approach.

```
$ cd Data
$ rm -rf Packages
$ git clone git@github.com:albertosantini/sublimetext-packages.git
```

Restart the editor and the plugins will be installed automatically. During the installation of the plugins a few errors are displayed. It is normal. When the plugins installation is ended (see the console view), you need to restart the editor again.

Notes
-----

Read also the note about the syncing: [Package Control Syncing](https://sublime.wbond.net/docs/syncing).
