#lang racket/base

(require racket/list
         racket/string
         html-parsing
         sxml
         "lib.rkt"
         "parse-img.rkt")

(provide parse-gdoc/post)

(define (parse-span span)

  (define (((make-next-content contents) res) r)
    (sxml:change-content r res))

  (define parsed-contents
    (parse-nodes (sxml:content span)))
    
  (define make-next
    (make-next-content parsed-contents))

  (define (get-decorations styles-list)
    (let ([decos (filter (λ (style)
                           (or
                            (and (color? style) (not-link? span))
                            (background-color? style)
                            (and (underline? style) (not-link? span))))
                         styles-list)])
      (if (empty? decos)
          #f
          decos)))

  (define (make-span colors)
    `(span (@ (style ,(string-join (flatten `(,colors "")) ";")))))

  (define (check-color-and-highlight styles-list)
    (cond
      [(get-decorations styles-list) => make-span]
      [else #f]))
    
  (define ((apply-check styles-list) check res)
    (cond
      [(apply check `(,styles-list)) => (make-next res)]
      [else res]))
  
  (foldl
   (apply-check (styles-list span))
   parsed-contents
   `(,check-bold ,check-italics ,check-color-and-highlight)))
  
(define (parse-node node)
  (cond
    [((ntype-names?? '(img)) node) (parse-img node)]
    [(and
      ((ntype-names?? '(p)) node)
      (equal? (sxml:text (sxml:content node)) "<!-- more -->"))
     '(*COMMENT* " more ")]
    ;     '(p (*COMMENT* " more "))]
    [(empty-html-element? node) (parse-elm-attrs node)]
    [(sxml:element? node) (sxml:change-content (parse-elm-attrs node) (parse-nodes (sxml:content node)))]
    [else node]))


(define (parse-nodes nodes)

  (define (empty-a? node) 
    (and
     ((ntype-names?? '(a)) node)
     (equal? '() (sxml:content node))))

  (define (fold-node node result)
    (cond
      [(or
        (empty-a? node)
        (equal? '(& nbsp) node)
        (equal? " " node))
       result]
      [((ntype-names?? '(span)) node) (let ([parsed (parse-span node)])
                                        (if (sxml:element? parsed)
                                            `(,@result ,parsed " ")
                                            `(,@result ,@parsed)))]
      [else `(,@result ,(parse-node node))]))

  (foldl fold-node '() nodes))


(define (parse-gdoc/post content)
  (srl:sxml->html-noindent 
   (parse-nodes
    (sxml:content
     (first ((sxpath '("html" "body")) (html->xexp content)))))))
