;; config_python.el

(elpy-enable)

;; setup jedi (auto-completion in python)
(add-hook 'prelude-python-mode-hook 'jedi:setup)
(setq jedi:complete-on-dot t)
(setq jedi:setup-keys t)



;; (add-hook 'python-mode-hook 'jedi:setup)
;; (setq jedi:complete-on-dot t)                 ; optional
;; (message "M-x jedi:install-server in Emacs")


;; ein
;; (require 'ein)

;; Enable auto-complete.el:
;; (setq ein:use-auto-complete t)
;; Or, to enable "superpack" (a little bit hacky improvements):
;; (setq ein:use-auto-complete-superpack t)

;; Enable smartrep.el:
;; (setq ein:use-smartrep t)

;; (require 'ipython)



;; Added January 2017
(add-hook 'python-mode-hook 'guess-style-guess-tabs-mode)
(add-hook 'python-mode-hook (lambda ()
                              (guess-style-guess-tab-width)))


(add-hook 'python-mode-hook
          (lambda ()
            (setq-default indent-tabs-mode t)
            (setq-default tab-width 4)
            (setq-default py-indent-tabs-mode t)
            (add-to-list 'write-file-functions 'delete-trailing-whitespace)))
