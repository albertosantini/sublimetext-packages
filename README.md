Sublime Text configuration
==========================

![](https://github.com/albertosantini/sublimetext-packages/workflows/CI/badge.svg)

This repository contains the configuration of Sublime Text editor (ST3).

I have been using the following plugins:

- [Git](https://github.com/kemayo/sublime-text-git)

Eventually `User/z.py` contains a few customizations.

Basically I have been mainly programming in JavaScript and R.

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

Alternate approach.

```
$ cd Data
$ rm -rf Packages
$ git clone git@github.com:albertosantini/sublimetext-packages.git Packages
```

Restart the editor and the plugins will be installed automatically. During the installation of the plugins a few errors are displayed. It is normal. When the plugins installation is ended (see the console view), you need to restart the editor again.

Notes
-----

Read also the note about the syncing: [Package Control Syncing](https://sublime.wbond.net/docs/syncing).
