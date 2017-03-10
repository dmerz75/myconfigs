;; config_autocomplete.el

(ac-config-default)


;; Show 0.8 second later
(setq ac-auto-show-menu 0.3)
(setq ac-quick-help-delay 0.4)


;; ac-menu-map is a keymap for completion on completion menu which is enabled when ac-use-menu-map is t.
(setq ac-use-menu-map t)
;; Default settings
(define-key ac-menu-map "\C-n" 'ac-next)
(define-key ac-menu-map "\C-p" 'ac-previous)



;; 20 lines
(setq ac-menu-height 20)


;; Just ignore case
(setq ac-ignore-case t)
