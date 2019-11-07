<script context="module">
    import {BLOG_POSTS, client} from './index.json'

    export async function preload({params, query}) {
        // return this.fetch(`blog.json`).then(r => r.json()).then(posts => {
        // 	return { posts };
        // });
        return {
            cache: await client.query({query: BLOG_POSTS})
        }
    }
</script>

<script>
    export let posts;
</script>

<style>
    ul {
        /*margin: 0 0 1em 0;*/
        line-height: 1.5;
    }
</style>

<svelte:head>
    <title>Blog</title>
</svelte:head>

<h1>Coming soon!</h1>

<!--<ul>-->
<!--	{#each posts as post}-->
<!--		&lt;!&ndash; we're using the non-standard `rel=prefetch` attribute to-->
<!--				tell Sapper to load the data for the page as soon as-->
<!--				the user hovers over the link or taps it, instead of-->
<!--				waiting for the 'click' event &ndash;&gt;-->
<!--		<li><a rel='prefetch' href='blog/{post.slug}'>{post.title}</a></li>-->
<!--	{/each}-->
<!--</ul>-->