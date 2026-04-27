(defun gcd (a b)
  (if (= b 0)
      a
      (gcd b (mod a b))
  )
)

(format t "Enter first number: ")
(setq a (read))

(format t "Enter second number: ")
(setq b (read))

(format t "GCD = ~a" (gcd a b))
