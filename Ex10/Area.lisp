(defun area-circle (r)
  (* 3.14 r r)
)

(format t "Enter radius: ")
(setq r (read))

(format t "Area = ~a" (area-circle r))
