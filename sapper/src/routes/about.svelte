<svelte:head>
	<title>About This Site</title>
</svelte:head>

<style>
	.b612 {
		font-family: B612-Regular, monospace;
	}
</style>

<h1>About This Site</h1>

<p>
	By day I work with Angular, so I wanted to use something completely different to make this site. I decided to go
	with Sapper, a Svelte framework based on next.js. I also haven't used Docker before and have need for handling
	different node versions, so I used this project to get started.
</p>

<p>
	I have a few ideas for cool sections of the site, so check back soon!
</p>

<h2>Design</h2>

<p>
	Yes, it's the default theme Sapper uses with some of the colors changed. I wanted something simple and
	I really liked it right off, so I'm sticking with it. At some point I'll do a portfolio piece of craziness, but I
	don't need one right now.
</p>

<h3>Tech</h3>

<p>
	Because Svelte's components are so simple, I originally didn't think I'd be using Sass, but that changed real quick.
	I also did the layout with CSS Grid - what a breath of fresh air compared to Bootstrap and Flexbox.
</p>

<h3>Fonts</h3>

<p>
	I used a <a href="https://type-scale.com/">type scale</a> based on perfect fourths for the sizing. I wanted to use
	the golden ratio or perfect fifths, but the size gets too huge too quickly.
</p>

<h4>Headings: <a href="https://b612-font.com/">B612</a></h4>

<p>
	This font was developed by AirBus to have high visibility on airplane cockpit screens, which is just about the
	coolest thing I've ever heard about a font. I'd love to use it as a programming font (there's a monospace version),
	but the parentheses look far too close to square brackets: <span class="b612">()</span>.
</p>

<h4>Body: <a href="https://rsms.me/inter/">Inter</a></h4>

<p>
	I found this front from this <a href="https://www.quora.com/What-is-the-most-readable-font-for-the-screen">
	fascinating Quora answer</a>. The site has some super interesting info as well.
</p>

<h4>Code: <a href="https://larsenwork.com/monoid/">Monoid</a> <a href="https://www.nerdfonts.com/">Nerdfont</a></h4>

<p>
	I picked <code>Monoid</code> as my main programming font a while ago because I found it super readable, it came with
	ligatures, and because <a href="https://james-iry.blogspot.com/2009/05/brief-incomplete-and-mostly-wrong.html">a
	monad is a monoid in the category of endofunctors</a>. I used to use vim as my main editor and still have it all
	tricked out	so I need Powerline support, and the extra glyphs in the NerdFont version come in handy from time to
	time.
</p>

<h2>Build</h2>

<p>
	The site is hosted on Github pages, which means the static files have to be in the <code>master</code> branch. So,
	I made a <code>sapper</code> branch to hold the application, which I put in the <code>app</code> folder.
</p>

<h2>Useful Resources</h2>

<ul>
	<li>
		<a href="https://svelte.dev/">Svelte</a>
	</li>
	<li>
		<a href="https://sapper.svelte.dev/">Sapper</a>
	</li>
	<li>
		<a href="https://blog.atulr.com/docker-local-environment/">
			Simplified guide to using Docker for local development environment
		</a>
	</li>
	<li>
		<a href="https://medium.com/@sean_27490/svelte-sapper-with-sass-271fff662da9">Svelte / Sapper with Sass!</a>
	</li>
	<li>
		<a href="https://css-tricks.com/snippets/css/complete-guide-grid/#prop-grid-auto-columns-rows">
			A Complete Guide to Grid
		</a>
	</li>
</ul>

<p>
	For <a href="/">About Me</a>, go to the homepage.
</p>
