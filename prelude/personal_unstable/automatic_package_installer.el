;;; package --- Summary
;;; Commentary:

(require 'cl)

;; http://clojure-doc.org/articles/tutorials/emacs.html
;; make sure packages are installed.
(defvar my-packages '(better-defaults
                      ;; bib-retrieve
                      projectile
                      ebib
                      clojure-mode
                      elpy               ;; comment here
                      jedi
                      flymake-python-pyflakes ;; may be misnamed
                      anaconda-mode
                      ac-anaconda
                      ac-c-headers
                      ac-cider
                      auctex
                      auto-complete
                      ethan-wspace
                      function-args
                      ;; bash-completion
                      cider)
  "A list of packages to ensure are installed at launch.")


;; Comment out if you've already loaded this package...



(defun my-packages-installed-p ()
  (loop for p in my-packages
        when (not (package-installed-p p)) do (return nil)
        finally (return t)))

(unless (my-packages-installed-p)
  ;; check for new packages (package versions)
  (package-refresh-contents)
  ;; install the missing packages
  (dolist (p my-packages)
    (when (not (package-installed-p p))
      (package-install p))))


;;   ebib               20150614.1019 obsolete              a BibTeX database manager
;;   elisp-slime-nav    20141224.854  obsolete              Make M-. and M-, work in elisp like they do in slime
;;   ethan-wspace       20140709.543  obsolete              whitespace customizations for emacs
;;   ethan-wspace       20151217.1810 obsolete              whitespace customizations for emacs
;;   flx                20140921.739  obsolete              fuzzy matching with good sorting
;;   flx-ido            20140821.2033 obsolete              flx integration for ido
;;   flycheck           20150626.1527 obsolete              On-the-fly syntax checking
;;   function-args      20150731.646  obsolete              C++ completion for GNU Emacs
;;   function-args      20151022.551  obsolete              C++ completion for GNU Emacs
;;   gh                 20150126.1125 obsolete              A GitHub library for Emacs
;;   guru-mode          20140905.702  obsolete              Become an Emacs guru
;;   irony              20151217.1058 obsolete              C/C++ minor mode powered by libclang
;;   slime              20150627.1630 obsolete              Superior Lisp Interaction Mode for Emacs
;;   slime-company      20150703.718  obsolete              slime completion backend for company mode



;; (dolist (p my-packages)
;;   (unless (package-installed-p p)
;;     (package-install p)))

;; (unless (package-installed-p 'cider)
;;   (package-install 'cider))
