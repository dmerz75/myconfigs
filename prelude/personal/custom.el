
(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(ansi-color-faces-vector
   [default default default italic underline success warning error])
 '(ansi-color-names-vector
   ["#3F3F3F" "#CC9393" "#7F9F00" "#F0DFAF" "#8CD0D3" "#DC8CC3" "#73A0E3" "#DCDCCC"])
 '(custom-enabled-themes (quote (tango-2)))
 '(custom-safe-themes
   (quote
    ("cf205b711e61963020e2d1561e87cdbe7727679b58af25dcabfe5073572b16f0" "4f5bb895d88b6fe6a983e63429f154b8d939b4a8c581956493783b2515e22d6d" "c74e83f8aa4c78a121b52146eadb792c9facc5b1f02c917e3dbb454fca931223" "12b4427ae6e0eef8b870b450e59e75122d5080016a9061c9696959e50d578057" "9cb6358979981949d1ae9da907a5d38fb6cde1776e8956a1db150925f2dad6c1" "ad950f1b1bf65682e390f3547d479fd35d8c66cafa2b8aa28179d78122faa947" "a27c00821ccfd5a78b01e4f35dc056706dd9ede09a8b90c6955ae6a390eb1c1e" "f04122bbc305a202967fa1838e20ff741455307c2ae80a26035fbf5d637e325f" "da7fa7211dd96fcf77398451e3f43052558f01b20eb8bee9ac0fd88627e11e22" "8abee8a14e028101f90a2d314f1b03bed1cde7fd3f1eb945ada6ffc15b1d7d65" "96998f6f11ef9f551b427b8853d947a7857ea5a578c75aa9c4e7c73fe04d10b4" "0c29db826418061b40564e3351194a3d4a125d182c6ee5178c237a7364f0ff12" "987b709680284a5858d5fe7e4e428463a20dfabe0a6f2a6146b3b8c7c529f08b" "46fd293ff6e2f6b74a5edf1063c32f2a758ec24a5f63d13b07a20255c074d399" "3cd28471e80be3bd2657ca3f03fbb2884ab669662271794360866ab60b6cb6e6" "e9776d12e4ccb722a2a732c6e80423331bcb93f02e089ba2a4b02e85de1cf00e" "58c6711a3b568437bab07a30385d34aacf64156cc5137ea20e799984f4227265" "e8825f26af32403c5ad8bc983f8610a4a4786eb55e3a363fa9acb48e0677fe7e" "cdd26fa6a8c6706c9009db659d2dffd7f4b0350f9cc94e5df657fa295fffec71" "a2e7b508533d46b701ad3b055e7c708323fb110b6676a8be458a758dd8f24e27" "18a33cdb764e4baf99b23dcd5abdbf1249670d412c6d3a8092ae1a7b211613d5" "ba9be9caf9aa91eb34cf11ad9e8c61e54db68d2d474f99a52ba7e87097fa27f5" "29b652383ce8b04163146f05f522d8f000ddd97173c9715d7416998278edecd8" "0ba649556dc51762e6794b92017f6f7406754ae3136eafef686d81c6da176cc5" "40bc0ac47a9bd5b8db7304f8ef628d71e2798135935eb450483db0dbbfff8b11" "603a9c7f3ca3253cb68584cb26c408afcf4e674d7db86badcfe649dd3c538656" "b3775ba758e7d31f3bb849e7c9e48ff60929a792961a2d536edec8f68c671ca5" "14225e826195202fbc17dcf333b94d91deb6e6f5ca3f5a75357009754666822a" "4c42b4a782b9568dbb7011bb5919e1e74754a0a13b2f9ba1dc017f9b50ef4dfe" "f1af57ed9c239a5db90a312de03741e703f712355417662c18e3f66787f94cbe" "3cc2385c39257fed66238921602d8104d8fd6266ad88a006d0a4325336f5ee02" "72a81c54c97b9e5efcc3ea214382615649ebb539cb4f2fe3a46cd12af72c7607" "3d5ef3d7ed58c9ad321f05360ad8a6b24585b9c49abcee67bdcbb0fe583a6950" "7bde52fdac7ac54d00f3d4c559f2f7aa899311655e7eb20ec5491f3b5c533fe8" "dba244449b15bdc6a3236f45cec7c2cb03de0f5cf5709a01158a278da86cb69b" "d725097d2547e9205ab6c8b034d6971c2f0fc64ae5f357b61b7de411ca3e7ab2" "cedd3b4295ac0a41ef48376e16b4745c25fa8e7b4f706173083f16d5792bb379" "7b4d9b8a6ada8e24ac9eecd057093b0572d7008dbd912328231d0cada776065a" "3632cf223c62cb7da121be0ed641a2243f7ec0130178722554e613c9ab3131de" "d44939ef462b7efb9bb5739f2dd50b03ac9ecf98c4df6578edcf145d6a2d188d" "33bb2c9b6e965f9c3366c57f8d08a94152954d4e2124dc621953f5a8d7e9ca41" "b880872e60d1c7090fcd3d89f287d2a5681e57be9ac90d4682ea442149f5135f" "39f98624caf410e66c4e03f36a1c373ea8ed9177cd9d12dfd6c0a53825599f60" "282606e51ef2811142af5068bd6694b7cf643b27d63666868bc97d04422318c1" default)))
 '(ein:use-auto-complete t)
 '(ensime-sem-high-faces
   (quote
    ((var :foreground "#9876aa" :underline
          (:style wave :color "yellow"))
     (val :foreground "#9876aa")
     (varField :slant italic)
     (valField :foreground "#9876aa" :slant italic)
     (functionCall :foreground "#a9b7c6")
     (operator :foreground "#cc7832")
     (param :foreground "#a9b7c6")
     (class :foreground "#4e807d")
     (trait :foreground "#4e807d" :slant italic)
     (object :foreground "#6897bb" :slant italic)
     (package :foreground "#cc7832"))))
 '(fci-rule-color "#383838")
 '(hl-paren-background-colors (quote ("#0287c8" "#40883f" nil)))
 '(hl-paren-colors (quote ("#f8fced" "#f8fced" "#b85c57")))
 '(linum-format " %7i ")
 '(nrepl-message-colors
   (quote
    ("#CC9393" "#DFAF8F" "#F0DFAF" "#7F9F7F" "#BFEBBF" "#93E0E3" "#94BFF3" "#DC8CC3")))
 '(package-selected-packages
   (quote
    (cmake-mode pygen org-ac flycheck-clangcheck flycheck-clojure flycheck-cstyle vimrc-mode virtualenvwrapper virtualenv pyenv-mode pyenv-mode-auto pydoc pydoc-info pyimport pyimpsort pylint pytest python python-cell python-django python-docstring python-info python-mode python-switch-quotes python-test python-x jedi shell-command seti-theme screenshot projectile-git-autofetch escreen eproject eldoc-eval cd-compile markdown-mode pkg-info popup pos-tip projectile python-environment pythonic pyvenv queue request rich-minority s sbt-mode scala-mode seq spinner swiper websocket with-editor yasnippet ace-jump-mode anaconda-mode async auctex auto-complete avy chinese-pyim chinese-pyim-basedict cider clojure-mode company concurrent ctable dash deferred dired-hacks-utils distel-completion-lib ebib ein epc epl eval-sexp-fu f find-file-in-project flx flycheck flymake-easy ggtags gh git-commit go-eldoc go-guru go-mode go-rename helm helm-core helm-swoop highlight highlight-indentation ht hydra ido-completing-read+ ivy javap-mode jedi-core json-reformat json-snatcher key-chord keyfreq logito macrostep magit magit-popup makey marshal math-symbol-lists noflet parsebib pcache helm-gtags ebib-handy windresize openwith org latest-clojure-libraries latex-extra latex-math-preview latex-pretty-symbols latex-preview-pane latex-unicode-math-mode git dired-imenu dired-k dired-sort-menu dired-sort-menu+ dired-subtree diredful ctags color-theme color-theme-approximate autopair cider-decompile cider-eval-sexp-fu cider-profile cider-spy clojure-cheatsheet clojure-mode-extra-font-locking clojure-quick-repls clojure-snippets auto-complete-auctex auto-complete-chunk auto-complete-clang auto-complete-clang-async auto-complete-distel auto-dictionary zop-to-char zenburn-theme yari xcscope xclip which-key volatile-highlights undo-tree tango-2-theme smex smartrep smartparens smart-mode-line slime scss-mode ruby-tools rainbow-mode rainbow-delimiters ov operate-on-number multishell multi-eshell move-text key-seq json-mode js2-mode inf-ruby imenu-anywhere ido-ubiquitous helm-projectile haskell-mode guru-mode grizzl gotest god-mode go-projectile gitignore-mode gitconfig-mode git-timemachine gist geiser function-args flymake-python-pyflakes flymake-cppcheck flylisp flx-ido expand-region ethan-wspace erlang ensime elpy elisp-slime-nav easy-kill discover-my-major disaster dired-sort dired-quick-sort dired+ diminish diff-hl crux company-go company-c-headers company-auctex company-anaconda coffee-mode cdlatex c-eldoc browse-kill-ring better-defaults beacon auto-complete-c-headers anzu achievements ace-window ace-isearch ace-flyspell ac-math ac-dabbrev ac-clang ac-cider ac-capf ac-c-headers ac-anaconda abyss-theme)))
 '(pdf-view-midnight-colors (quote ("#DCDCCC" . "#383838")))
 '(pos-tip-background-color "color-23")
 '(pos-tip-foreground-color "color-230")
 '(require-final-newline nil)
 '(sml/active-background-color "#98ece8")
 '(sml/active-foreground-color "#282828")
 '(sml/inactive-background-color "#4fa8a8")
 '(sml/inactive-foreground-color "#282828")
 '(vc-annotate-background "#2B2B2B")
 '(vc-annotate-color-map
   (quote
    ((20 . "#BC8383")
     (40 . "#CC9393")
     (60 . "#DFAF8F")
     (80 . "#D0BF8F")
     (100 . "#E0CF9F")
     (120 . "#F0DFAF")
     (140 . "#5F7F5F")
     (160 . "#7F9F7F")
     (180 . "#8FB28F")
     (200 . "#9FC59F")
     (220 . "#AFD8AF")
     (240 . "#BFEBBF")
     (260 . "#93E0E3")
     (280 . "#6CA0A3")
     (300 . "#7CB8BB")
     (320 . "#8CD0D3")
     (340 . "#94BFF3")
     (360 . "#DC8CC3"))))
 '(vc-annotate-very-old-color "#DC8CC3")
 '(when
      (or
       (not
        (boundp
         (quote ansi-term-color-vector)))
       (not
        (facep
         (aref ansi-term-color-vector 0))))))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(default ((t (:background nil)))))
