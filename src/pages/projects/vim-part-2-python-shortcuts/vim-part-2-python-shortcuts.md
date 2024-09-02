date:          2024-08-21
categories:    tech|how-to

_August 21, 2024_

## Vim Part 2: Python Shortcuts

My next moves in getting vim set up are getting some of the stuff that I use all the time in PyCharm working (I know 
the stackoverflow answer to this is "well if you want PyCharm-like just use PyCharm". I've always wanted to say this 
to those people: go fuck yourselves). We already get highlighting for free with vim, so the first thing we'll need is 
syntax checking.

### Syntax and Formatting: ALE

It looks like [ALE](https://github.com/dense-analysis/ale) is the way to go for this, so 
