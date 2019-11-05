<style lang="scss">
	.wrapper {
		display: grid;
		grid-column-gap: 15px;
		grid-template-columns: auto 300px;
		grid-template-rows: auto;
		grid-template-areas: "intro sidebar";
	}

	.intro {
		display: flex;
		flex-wrap: wrap;
		grid-area: intro;
	}

	.links {
		display: grid;
		grid-template-columns: auto auto auto;
		grid-column-gap: 10px;

		a {
			height: 32px;
			width: 32px;
		}

		.github-andybp85 {
			background-color: #aaaaaa;
			border-radius: 4px;
			display: inline-block;
			height: 30px;
			padding: 2px 1px 0 1px;
			width: 30px;

			img {
				height: 28px;
				width: 30px;
			}
		}
	}

	.me {
		border-radius: 5px;
		grid-area: sidebar;
	}
</style>

<svelte:head>
	<title>Andy's Site</title>
</svelte:head>

Hiya!

<div class="wrapper">
	<div class="intro">
		<p>
			I'm Andy, a software engineer and musician living my dreams in Jersey City, NJ. I have a ton of interests
			and always have several side projects going. This is my place to share my work and ideas with the world.
		</p>

		<div class="links">
			<a class="github-andybp85" href="https://github.com/andybp85">
				<img alt="andy's Github" src="GitHub-Mark-32px.png">
			</a>
			<a href="https://www.facebook.com/andrew.stanish">
				<img alt="andy's Github" src="f_logo_RGB-Blue_1024.png">
			</a>
			<a href="https://twitter.com/andybp85">
				<img alt="andy's Github" src="Twitter_Social_Icon_Rounded_Square_Color.png">
			</a>
		</div>
	</div>


	<img class="me" alt='me' src='me.jpg'>
</div>