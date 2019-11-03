#lang racket

(require net/url
         sxml)

(provide parse-img)

(define (parse-img img)

  (define src
    (sxml:attr img' src))

  (define-values (port headers)
    (get-pure-port/headers
     (string->url src)))

  (define filename
    (second (regexp-match #rx"filename=\"(.*?)\"" headers)))

  (define out-img
    (sxml:change-attrlist
     img `((src ,(string-append (getenv "FILES_BASE_URI") filename)))))
  
;  (define img-path
;    (build-path (getenv "FILES_BASE_PATH") filename))
;
;  (unless (file-exists? img-path)
;    (with-output-to-file img-path
;      (λ () (display (port->bytes port #:close? #t)))))

  out-img)