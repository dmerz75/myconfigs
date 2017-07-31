;;; package --- Summary:

;;; Commentary:

;;; Code:
;; Switching to ibuffer puts the cursor on the most recent buffer
(defadvice ibuffer (around ibuffer-point-to-most-recent) ()
  "Open ibuffer with cursor pointed to most recent buffer name"
  (let ((recent-buffer-name (buffer-name)))
    ad-do-it
    (ibuffer-jump-to-buffer recent-buffer-name)))
(ad-activate 'ibuffer)

;; Use human readable Size column instead of original one
(define-ibuffer-column size-h
  (:name "Size" :inline t)
  (cond
   ((> (buffer-size) 1000000) (format "%6.1fM" (/ (buffer-size) 1000000.0)))
   ((> (buffer-size) 100000) (format "%6.0fk" (/ (buffer-size) 1000.0)))
   ((> (buffer-size) 1000) (format "%6.1fk" (/ (buffer-size) 1000.0)))
   (t (format "%5d" (buffer-size)))))

;; Modify the default ibuffer-formats
(setq ibuffer-formats
      '((mark modified read-only " "
              (name 30 30 :left :elide)
              " "
              (size-h 8 -1 :right)
              " "
              (mode 14 14 :left :elide)
              " "
              filename-and-process)))


;; Enable ibuffer-filter-by-filename to filter on directory names too.
(eval-after-load "ibuf-ext"
  '(define-ibuffer-filter filename
       "Toggle current view to buffers with file or directory name matching QUALIFIER."
     (:description "filename"
                   :reader (read-from-minibuffer "Filter by file/directory name (regexp): "))
     (ibuffer-awhen (or (buffer-local-value 'buffer-file-name buf)
                        (buffer-local-value 'dired-directory buf))
       (string-match qualifier it))))




;; Enable ibuffer-filter-by-filename to filter on directory names too.
;; (eval-after-load "ibuf-ext"
;;   '(define-ibuffer-filter filename
;;        "Toggle current view to buffers with file or directory name matching QUALIFIER."
;;      (:description "filename"
;;                    :reader (read-from-minibuffer "Filter by file/directory name (regexp): "))
;;      (ibuffer-awhen (or (buffer-local-value 'buffer-file-name buf)
;;                         (buffer-local-value 'dired-directory buf))
;;        (string-match qualifier it))))



;; (setq ibuffer-formats
;;       '((mark modified read-only " "
;;               (name 30 30 :left :elide) " "
;;               (size 9 -1 :right) " "
;;               (mode 16 16 :left :elide) " " filename-and-process)
;;         (mark " " (name 16 -1) " " filename)))

;; (defun my-ibuffer-hook ()
;;   ;; add another sorting method for ibuffer (allow the grouping of
;;   ;; filenames and dired buffers

;;   (ibuffer-define-sorter pathname
;;                          (:documentation
;;                           "Sort the buffers by their pathname."
;;                           :description "path")
;;                          (string-lessp (with-current-buffer (car a)
;;                                          (or buffer-file-name
;;                                              (if (eq major-mode 'dired-mode)
;;                                                  (expand-file-name dired-directory))
;;                                              ;; so that all non pathnames are at the end
;;                                              "~"))
;;                                        (with-current-buffer (car b)
;;                                          (or buffer-file-name
;;                                              (if (eq major-mode 'dired-mode)
;;                                                  (expand-file-name dired-directory))
;;                                              ;; so that all non pathnames are at the end
;;                                              "~"))))
;;   ;; add key binding
;;   (define-key ibuffer-mode-map (kbd "s p") 'ibuffer-do-sort-by-pathname))
;; (add-hook 'ibuffer-mode-hooks 'my-ibuffer-hook)
