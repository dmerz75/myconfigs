;; To change the default font for new (non special-display) frames,
;; put either of these in your init file:
(add-to-list 'default-frame-alist '(font .  "Mono-10" ))
(set-face-attribute 'default t :font  "Mono-10" )

;; To change the default font for the current frame, as well as future frames,
;; put either of these in your init file:
(set-face-attribute 'default nil :font  "Mono-10" )
(set-frame-font   "Mono-10" nil t)

;; (print (font-family-list))
;; Mono-10
;; -- ok.
;; Proggy Square 80
;; -- doesn't work.

;; The simplest way to set the Emacs font is just to add the following in your .emacs (or init.el):
;; (set-default-font "Inconsolata-12")
;; This code will set the Emacs font to Inconsolata (my favorite monospaced font) with font size 12pt.
;; The problem with this approach is that it will not work with a X Emacs client (emacsclient -c)
;; connecting to an Emacs daemon (emacs —daemon), because the code will get run when the server
;; starts and will basically mean nothing to it. You can alleviate this problem by using the
;; appropriate hook for X clients, but I find this distasteful. A much simpler solution is to forget
;; about set-default-font altogether and simply create a file named .Xdefaults in your home folder.
;; Put the following in it:

;; Emacs.font: Inconsolata-12
;; $ xrdb -merge ~/.Xdefaults
;; At this point you can start Emacs (in normal or daemon mode) and your new font settings should be in effect.



;; general.el --------------------------------------------------------------
(defun buffer-mode (buffer-or-string)
  "Returns the major mode associated with a buffer."
  (interactive)
  (with-current-buffer buffer-or-string
    major-mode))

(defun which-active-modes ()
  "Give a message of which minor modes are enabled in the current buffer."
  (interactive)
  (let ((active-modes))
    (mapc (lambda (mode) (condition-case nil
                             (if (and (symbolp mode) (symbol-value mode))
                                 (add-to-list 'active-modes mode))
                           (error nil) ))
          minor-mode-list)
    (message "Active modes are %s" active-modes)))
;; general.el --------------------------------------------------------------


;; fix the PATH variable ---------------------------------------------------
(defun set-exec-path-from-shell-PATH ()
  (let ((path-from-shell (shell-command-to-string "TERM=vt100 $SHELL -i -c 'echo $PATH'")))
    (setenv "PATH" path-from-shell)
    (setq exec-path (split-string path-from-shell path-separator))))
(when window-system (set-exec-path-from-shell-PATH))
;; fix the PATH variable ---------------------------------------------------

;; w3m ---------------------------------------------------------------------
;; (require 'w3m-load-list)
;; w3m ---------------------------------------------------------------------

;; Set cursor color to white #ffffff
(set-cursor-color "#ffffdd")
