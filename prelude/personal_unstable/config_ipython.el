;; config_ipython.el


;; load notebook list if Emacs is idle for 3 sec after start-up
(run-with-idle-timer 3 nil #'ein:notebooklist-load)

;; (add-hook 'ein-mode-hook (lambda () ('load-theme leuven)))

(when (executable-find "ipython")
  ;; (setq python-shell-interpreter "ipython")
  (setq python-shell-interpreter "ipython"
        python-shell-interpreter-args "-i"))
