(defun remove-newlines-in-region ()
  "Removes all newlines in the region."
  (interactive)
  (save-restriction
    (narrow-to-region (point) (mark))
    (goto-char (point-min))
    (while (search-forward "\n" nil t) (replace-match "" nil t))))

;; (global-set-key [f8] 'remove-newlines-in-region)
(global-set-key (kbd "C-c q") 'remove-newlines-in-region)
