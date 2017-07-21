(add-hook 'ediff-load-hook
          (lambda ()
            (set-face-foreground
             ediff-current-diff-face-B "#000080")
            (set-face-background
             ediff-current-diff-face-B "#ffdead")
            ;; (set-face-foreground
            ;;  ediff-current-diff-face-A "#000080")
            (set-face-background
             ;; ediff-current-diff-face-A "#98fb98")
             ;; ediff-current-diff-face-A "#c1ffc1")
             ;; ediff-current-diff-face-A "#ffec8b")
             ediff-current-diff-face-A "#ccd39b")
            ))


(setq-default indent-tabs-mode nil) ;; Prevents extraneous tabs
(fset 'yes-or-no-p 'y-or-n-p)       ;; accept y or n in lieu of yes or no
(toggle-scroll-bar -1)
(setq visible-bell t)
(setq major-mode 'text-mode)
(setq scroll-step 1)                ;; scroll one line at end of page
(setq-default tab-width 4)          ;; indent to 4 characters by default
;; (setq c-basic-offset 4)             ;; C, use 4 spaces
;; (auto-indent-global-mode)
(setq auto-indent-mode -1)
(put 'erase-buffer 'disabled nil)
(electric-pair-mode -1)

;; my Kill to end of buffer C-c E
(defun delete-to-end-of-buffer (add-to-kill-ring-p)
  "Deletes from point to end of buffer.
  If prefix argument is given, kill the region, adding it to the kill ring."
  (interactive "P")
  (if add-to-kill-ring-p
      (kill-region (point) (point-max))
    (delete-region (point) (point-max))))

(defun copy-current-line-and-paste ()
  "copy the current line, comment it, and paste it uncommented"
  (interactive)
  (move-beginning-of-line nil)
  (kill-line)
  (yank)
  (open-line 1)
  (next-line 1)
  (yank))




(defun comment-or-uncomment-line ()
  "Comments or uncomments the current line."
  (interactive)
  (if (region-active-p)
      (comment-or-uncomment-region (region-beginning) (region-end))
    (comment-or-uncomment-region (line-beginning-position) (line-end-position))
    )
)
;; (global-set-key (kbd "C-x c") 'comment-or-uncomment-line)
;; (global-set-key (kbd "C-c c") 'comment-region)
;; (global-set-key (kbd "C-c u") 'uncomment-region)
;; (global-set-key (kbd "C-x c") 'comment-or-uncomment-line)
(global-set-key (kbd "C-c c") 'comment-or-uncomment-line)
;; (global-set-key (kbd "C-c u") 'uncomment-kbd)




(defun find-user-init-file ()
  "Edit the `user-init-file', in another window."
  (interactive)
  (find-file-other-window user-init-file)
  (delete-other-windows))
(global-set-key (kbd "C-c I") 'find-user-init-file)

;; windmove
(when (fboundp 'windmove-default-keybindings)
  (windmove-default-keybindings))
(global-set-key (kbd "C-c <left>") 'windmove-left)
(global-set-key (kbd "C-c <right>") 'windmove-right)
(global-set-key (kbd "C-c <up>") 'windmove-up)
(global-set-key (kbd "C-c <down>") 'windmove-down)
;; end windmove

;; auto-mode-alist
(add-to-list 'auto-mode-alist '("\\.py\\'" . python-mode))
(add-to-list 'auto-mode-alist '("\\.cpp'" . c++-mode))
;; (add-to-list 'auto-mode-alist '("\\.pdb'" . text/enriched))
(add-to-list 'auto-mode-alist '("\\.pdb'" . text-mode))


;; prelude-open-with
;; (global-set-key (kbd "C-c o") 'prelude-open-with)

;; shells
;; (global-set-key (kbd "C-u M-x") ')
;; (global-set-key (kbd "C-x M-s") 'shell)

(defun new-shell ()
  (interactive)
  (let (
        (currentbuf (get-buffer-window (current-buffer)))
        ;; (newbuf     (generate-new-buffer-name "*shell*"))
        (newbuf     (generate-new-buffer-name "*shell*"))
        )
    (generate-new-buffer newbuf)
    (set-window-dedicated-p currentbuf nil)
    (set-window-buffer currentbuf newbuf)
    (shell newbuf)
    )
  )

(defun goto-recent-shell ()
  (interactive)
  (message "goto-recent-shell")
  (message list-buffers)
  )

;; (global-set-key [f1] 'new-shell) ;; into current working directory
;; (global-set-key [f2] 'goto-recent-shell) ;; goto-recent-shell
;; (global-set-key [f7] 'shell) ;; home directory

;; Enigma Curry blog - C-c T - ansi-term
(require 'term)
(defun visit-ansi-term ()
  "If the current buffer is:
     1) a running ansi-term named *ansi-term*, rename it.
     2) a stopped ansi-term, kill it and create a new one.
     3) a non ansi-term, go to an already running ansi-term
        or start a new one while killing a defunt one"
  (interactive)
  (let ((is-term (string= "term-mode" major-mode))
        (is-running (term-check-proc (buffer-name)))
        (term-cmd "/bin/bash")
        (anon-term (get-buffer "*ansi-term*")))
    (if is-term
        (if is-running
            (if (string= "*ansi-term*" (buffer-name))
                (call-interactively 'rename-buffer)
              (if anon-term
                  (switch-to-buffer "*ansi-term*")
                (ansi-term term-cmd)
                ;; (delete-other-windows)
                )
              )
          (kill-buffer (buffer-name))
          (ansi-term term-cmd)
          ;; (delete-other-windows)
          )
      (if anon-term
          (if (term-check-proc "*ansi-term*")
              (switch-to-buffer "*ansi-term*")
            (kill-buffer "*ansi-term*")
            (ansi-term term-cmd)
            (delete-other-windows)
            )
        (ansi-term term-cmd)
        )))
  ;; (delete-other-windows)
  )
;; (global-set-key (kbd "C-c T") 'visit-ansi-term)

;; (global-set-key [f1] 'ansi-term) ;; into current working directory
(global-set-key [f4] 'visit-ansi-term) ;; visit-ansi-term
;; (global-set-key [f7] 'shell) ;; home directory
(global-set-key [f1] 'shell) ;; into current working directory
(global-set-key [f2] 'new-shell) ;; into current working directory
;; (global-set-key [f2] 'goto-recent-shell) ;; goto-recent-shell
;; F7 is currently owned by kde

;; (global-set-key [f2] 'multi-eshell) ;; into current working directory
;; (global-set-key [f2] 'new-eshell) ;; into current working directory
;; (global-set-key [f2] 'multi-eshell-switch) ;; into current working directory
;; (global-set-key [f] 'multi-eshell-go-back)



(add-hook 'shell-mode-hook 'ansi-color-for-comint-mode-on)
(add-to-list 'comint-output-filter-functions 'ansi-color-process-output)


;; count-words
(global-set-key (kbd "C-c w") 'count-words)
(key-chord-define-global "ii" 'copy-current-line-and-paste)


;; region - key binds
(global-set-key (kbd "C-c E") 'delete-to-end-of-buffer)
(global-set-key (kbd "C-l") 'goto-line)

(global-set-key (kbd "C-c C") 'compile)
(global-set-key (kbd "C-c R") 'replace-regexp)
(global-set-key (kbd "C-x u") 'undo)
;; overrides: It is bound to C-h C-k, <help> C-k., (find-function-on-key KEY)
(global-set-key (kbd "C-h C-k") 'free-keys)
(global-set-key (kbd "C-M-y") 'clipboard-yank)
;; (global-set-key (kbd "C-c l") 'copy-current-line-and-paste)

;; ...C-c b,rename buffer
;; ...C-c C-c,comment-region
(message "
...C-c C,compile
...C-l,line
...C-c C,compile
...C-c c,uncomment-region
...C-x u,undo")


(provide 'default_kbd) ;;; default_kbd.el ends here
 ;;; default_kbd.el ends here
