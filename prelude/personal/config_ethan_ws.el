;;; package --- Summary

;;; Commentary:
;; Emacsredux.com - begin
;; (require 'whitespace)
(setq whitespace-line-column 80) ;; limit line length
;; (setq whitespace-style '(face lines-tail))
;; (add-hook 'prog-mode-hook 'whitespace-mode)
;; (global-whitespace-mode +1)


;; (add-hook 'before-save-hook 'delete-trailing-whitespace)

;; keybind for whitespace
;; (global-set-key (kbd "C-c w") 'delete-trailing-whitespace)


;; Previous fail?
;; (defun makefile-tabs-are-less-evil ()
;;   (setq ethan-wspace-errors (remove 'tabs ethan-wspace-errors))
;;   (add-hook 'makefile-mode-hook 'makefile-tabs-are-less-evil))

;; (add-hook 'makefile-mode-hook 'indent-tabs-mode)

(defun makefile-tabs-are-less-evil ()
  (setq ethan-wspace-errors (remove 'tabs ethan-wspace-errors))
(add-hook 'makefile-mode-hook 'makefile-tabs-are-less-evil))

;; ethan-wspace
(require 'ethan-wspace)
(global-ethan-wspace-mode 1)


;; prelude
(setq prelude-clean-whitespace-on-save nil)

;; did it work?
;; so that ethan wspace supercedes all other wspace and newline preferences
(setq mode-require-final-newline nil)
