## About Me {#about-me}

> It means something being from New Jersey. It means you have a sense of humor.  
> *&mdash; Anthony Bourdain*

I'm your typical programmer/musician with a ton of hobbies, including biking, history, electronics, 
and spicy food. By day I work for NBCUniversal (née CNBC) as a principal software engineer for 
the CMS. Nights and weekends I do music, including sound at one of the best bars (and with some 
of the best people) I've ever stumbled upon, The Laundromat in Morristown, NJ. I also play bass 
in a blues rock band, Kru Kerly, which is based out of my hometown of Jersey City, NJ.

## About This Site {#about-site}

### Design

KISS. It also has a light and dark mode, but you don't have to click a button for it; it uses 
a [media query](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme) to 
detect what you have your OS set to.

#### Fonts

I used a [type scale](https://type-scale.com/) based on perfect fourths for the sizing. I wanted 
to use the golden ratio or perfect fifths, but the size gets too huge too quickly.

##### Headings: [B612](https://b612-font.com/)

This font was developed by AirBus to have high visibility on airplane cockpit screens, which is just
 about the coolest thing I've ever heard about a font. I'd love to use it as a programming font 
(there's a monospace version), but the parentheses look far too close to square brackets.

##### Body: [Inter](https://rsms.me/inter/)

I found this font from 
this [fascinating Quora answer](https://www.quora.com/What-is-the-most-readable-font-for-the-screen).
 The site has some super interesting info as well.

##### Code: [Berkeley Mono](https://berkeleygraphics.com/typefaces/berkeley-mono/)

Never thought I'd pay for a coding font, but I love its retro look, and I was able to get a 7 with a
 slash through it.

### Build

I do Javascript all day at work for well over a decade now. I'm not going to say I'm sick of it, 
because there's plenty I like about using a multi-paradigm Scheme derivative (and Typescript is 
huge improvement on vanilla JS). But, there's several other languages I like far more, especially 
Python. So I used Python for the site builder. I've done a bunch of work with Python, 
and I think it nails everything I want in an everyday language. For details on how this works, 
check out the [ReadMe](https://github.com/andybp85/andybp85.github.io). I'm also using real Sass, 
without the bleeping curly braces. (I swear it's like my industry has Stockholm Syndrome for
noisy code...)

Will I write any JS for this site? It's definitely not going to be a SPA, which I don't think 
actually makes for a great UX (and frankly does make for a damn-near nightmarish dev experience, 
which is why we need these bloated-ass frameworks to make web apps). I use 
[Clicky](https://clicky.com/) for less-sketchy analytics, so there's the JS code for that, 
although I didn't write it. Maybe embedded in the HTML for animations or something...but 
definitely not for the kind of breaking-the-back-button behavior that's all the rage these days.

Honestly, the thing I hate most about JS is what the community has decided on as the "standard 
style" (and don't get me started on Prettier). Rather than get into exactly why, I'll just post 
some links below that I think explain my thoughts for me.

* [Linux kernel coding style: Indentation](https://www.kernel.org/doc/html/v4.10/process/coding-style.html#indentation)
* [Hissp Style Guid](https://hissp.readthedocs.io/en/latest/style_guide.html)
* [Eloquent Javascript: Introduction](https://eloquentjavascript.net/2nd_edition/00_intro.html), specifically the "On Programming" section
