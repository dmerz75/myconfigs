;;; package: --- Summary

;;; Code:
(setq yas-snippet-dirs
      '(;; "~/mount1/snippets"
        "~/ext2/snippets"
        ;; "~/.emacs.d/snippets"
        ;; "/home/dale/.emacs.d/personal/yasnippet/yasmate/snippets"
        ))

;; (add-to-list 'load-path "~/.emacs.d/personal/yasnippet")
;; (add-to-list 'load-path "~/snippets")
;; (add-to-list 'load-path "$MOUNT1/snippets")
;; (add-to-list 'load-path "~/mount1/snippets")

(require 'yasnippet)
(yas-global-mode 1)

(setq hippie-expand-try-functions-list
      (cons 'yas/hippie-try-expand hippie-expand-try-functions-list)
      )


;;; Commentary:
