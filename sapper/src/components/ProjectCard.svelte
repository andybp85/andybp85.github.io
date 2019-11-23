<script>
    export let title;
    export let graphic;
    export let blurb;
    export let link;
</script>

<style lang="scss">
    section {
        display: grid;
        grid-column-gap: 15px;
        grid-template-areas: "title title"
                             "blurb thumb"
                             "link link";

        h1 {
            grid-area: title;
        }

        p {
            grid-area: blurb;
        }

        img {
            grid-area: thumb;
            margin-top: 20px;
        }

        footer {
            grid-area: link;
        }

    }

</style>

<section>

    <h1>{title}</h1>

    <p>
        {@html blurb}
    </p>

    {#if graphic}
    <img alt={title} src={graphic} />
    {/if}


    {#if link}
    <footer>
        <a href={link}>More</a>
    </footer>
    {/if}

</section>