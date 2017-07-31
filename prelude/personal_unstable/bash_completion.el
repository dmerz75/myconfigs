(autoload 'bash-completion-dynamic-complete
  "bash-completion"
  "BASH completion hook")
(add-hook 'shell-dynamic-complete-functions
          'bash-completion-dynamic-complete)

;; turn off yas in term-mode to get bash-completion.
(add-hook 'term-mode-hook (lambda()
                            (yas-minor-mode -1)))
