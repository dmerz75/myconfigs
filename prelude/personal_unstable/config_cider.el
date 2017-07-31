;; cider:

;; Don't prompt and don't save
(setq cider-prompt-save-file-on-load nil)
;; Just save without prompting
(setq cider-prompt-save-file-on-load 'always-save)



;; Change the result prefix for REPL evaluation (by default there's no prefix):
(setq cider-repl-result-prefix ";; =< ")

(setq cider-repl-wrap-history t)
(setq cider-repl-history-size 1000) ; the default is 500
;; (require 'icomplete)




(message "cider_config.el loaded!")
