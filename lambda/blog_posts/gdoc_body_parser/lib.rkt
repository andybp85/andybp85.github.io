#lang racket

(require sxml)

(provide (all-defined-out))

(define (color? style)
  (and (string-prefix? style "color:")
       (not (or
             (string-contains? style "#222222")
             (string-contains? style "#000000")))))

(define (background-color? style)
  (string-prefix? style "background-color:"))

(define (underline? style)
  (string=? style "text-decoration:underline"))

(define (not-link? span)
  (if (empty? (sxml:content span))
      #t
      (not ((select-first-kid (ntype-names?? '(a))) (sxml:content span)))))

(define (check-bold styles-list)
  (if (member "font-weight:700" styles-list)
      '(strong)
      #f))

(define (check-italics styles-list)
  (if (member "font-style:italic" styles-list)
      '(em)
      #f))

(define (styles-list elm)
  (if (sxml:attr elm 'style)
      (string-split (sxml:attr elm 'style) ";")
      '()))
  
(define (empty-attr? attr)
  (not (non-empty-string? (second attr))))

(define (style? attr)
  (eq? (car attr) 'style))

(define (id? attr)
  (eq? (car attr) 'id))

(define (class? attr)
  (eq? (car attr) 'class))

(define (href? attr)
  (eq? (car attr) 'href))

(define (fix-href href-attr)

  (define (make-href href)
    (list
     (car href-attr)
     href))

  (make-href
   (first (string-split
           (first (string-split
                   (second href-attr)
                   "https://www.google.com/url?q=")) "&amp;sa=D"))))

;  (define original-href
;    (second href-attr))
;
;  (define suggested-href
;    (first (string-split
;            (first (string-split
;                    original-href
;                    "https://www.google.com/url?q=")) "&amp;sa=D")))
;
;  (displayln (~a "Original href: " original-href))
;  (displayln (~a "Suggested href: " suggested-href))
;  (display "Accept? [Y/<url>] ")
;
;  (define user-input
;    (read-line (current-input-port)))
;
;  (if (regexp-match #rx"^Y$|^$" user-input)
;      (make-href suggested-href)
;      (make-href user-input)))

(define (parse-attrs attrs)
  (if (empty? attrs)
      empty
      (let ([attr (car attrs)])
        (if (or (empty-attr? attr) (style? attr) (id? attr) (class? attr))
            (parse-attrs (rest attrs))
            (cons 
             (if (href? attr)
                 (fix-href attr)
                 attr)
             (parse-attrs (rest attrs)))))))

(define (empty-html-element? elm)
  ; img is in here despite being parsed seperately below to accurately reflect the spec
  (member
   (sxml:element-name elm)
   '(area base br col embed hr img input link meta param source track wbr)))

(define (parse-elm-attrs elm)
  (sxml:clean
   (sxml:change-attrlist elm (parse-attrs (sxml:attr-list elm)))))

