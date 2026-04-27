(defun calculator (a b op)
  (cond
    ((eq op '+) (+ a b))
    ((eq op '-) (- a b))
    ((eq op '*) (* a b))
    ((eq op '/) (/ a b))
    (t (format t "Invalid Operator"))
  )
)

(format t "Enter first number: ")
(setq a (read))

(format t "Enter second number: ")
(setq b (read))

(format t "Enter operator (+ - * /): ")
(setq op (read))

(format t "Result = ~a" (calculator a b op))
