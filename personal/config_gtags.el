;; Install global, speedbar
;; global is from the AUR.
;; configure.

;; Start by adding a few lines to your init.el to do a basic setup for Global.
;; First, tell Emacs where your gtags.el file, if it is someplace other than the standard macro directory.
;; (I installed Global via apt-get on Debian, and the gtags.el was in /usr/share/emacs/site-lisp/global,
;; so I didn't need to modify the load-path)

;; (setq load-path (cons "/path/to/gtags.el" load-path))
;; (setq load-path (cons "/usr/share/emacs/site-lisp/global" load-path))


;; Next, tell Emacs to load gtags on start-up:
;; autoload 'gtags-mode "gtags" "" t)
(autoload 'gtags-mode "gtags" "" t)


;; The next part is preference. If you would like Emacs to go into gtags mode whenever you enter c mode, add the following section. (If instead you would rather control when gtags mode starts, omit this section and turn on gtags mode when you want it, via M-x gtags-mode)
(add-hook 'c-mode-hook
          '(lambda ()
             (gtags-mode t)
             ))
(add-hook 'c++-mode-hook
          '(lambda ()
             (gtags-mode t)
             ))
;; Note: I have actually set Emacs to use c++-mode even when I am editing C files. If you've done that,
;; then you want to add-hook to c++-mode-hook rather than c-mode-hook)



;; Additional, I like to have Speedbar start when I run Emacs. To do that,
;; add the following section to init.el.
;; (If you want to start Speedbar manually instead, omit this and use M-x speedbar
;; Start speedbar automatically if we're using a window system like X, etc

;; on
;; (when window-system
;;   (speedbar t))
;; off
(when window-system
  (speedbar nil))
(speedbar nil)


;; To Begin:____________________________________________________________________
;; The simplest way to make a set of tags is to go to the top directory in your
;; source tree and run


;; >>> gtags -v


;; This will recursively tag all the files in the tree, including C, C++,
;; Java, PHP, assembler, and YACC source

;; If you wish to limit the files Global tags (or add more) look in the Global documentation, including the settings in the ~/.globalrc config file.

;; This simple script is something I used for an ARM Linux kernel source project,
;; to specify which parts of the source tree I want to tag. It uses gtag's -f
;; option to read the list of files to tag from a file.
;; #!/bin/bash
;; rm .files2gtag
;; for f in block crypto Documentation drivers firmware fs include init ipc kernel lib \
;;          mm net samples scripts security sound tools usr virt
;; do
;;    find $f -iregex '.*\(c\|h\)'  >>.files2gtag
;; done

;; for f in boot common configs include kernel lib mach-dove mm nwfpe oprofile \
;;          plat-orion tools
;; do
;;    find arch/arm/$f -iregex '.*\(c\|h\)'  >>.files2gtag
;; done
;; gtags -v -f .files2gtag
