const navLink = (href, text) => {
    const isCurrent = location.pathname === href || location.pathname.startsWith(href + '/')
    const current = isCurrent ? ' class="current" aria-current="page"' : ""
    return `<a href="${href}"${current}>${text}</a>`
}

customElements.define("site-header", class extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
            <header>
                <h1><a href="/">Andy Stanish</a></h1>
                <nav aria-label="Main">
                    ${navLink("/about", "About")}
                    ${navLink("/blog", "Blog")}
                    ${navLink("/projects", "Projects")}
                </nav>
            </header>`
    }
})

customElements.define("site-footer", class extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
            <footer>
                <div id="social-media-links">
                    <a href="https://github.com/andybp85" target="_blank" rel="noopener" title="Andy's Github (opens in new tab)">
                        <img id="github" alt="Andy's Github" src="/icons/GitHub-Mark-32px.png" height="32" width="32">
                    </a>
                    <a href="https://www.facebook.com/andrew.stanish" target="_blank" rel="noopener" title="Andy's Facebook (opens in new tab)">
                        <img alt="Andy's Facebook" src="/icons/f_logo_RGB-Blue_1024.png" height="32" width="32">
                    </a>
                    <a href="https://twitter.com/andybp85" target="_blank" rel="noopener" title="Andy's Twitter (opens in new tab)">
                        <img alt="Andy's Twitter" src="/icons/Twitter_Social_Icon_Rounded_Square_Color.png" height="32" width="32">
                    </a>
                    <a href="https://www.linkedin.com/in/andrewstanish/" target="_blank" rel="noopener" title="Andy's LinkedIn (opens in new tab)">
                        <img alt="Andy's LinkedIn" src="/icons/In-Blue-34.png" height="32" width="32">
                    </a>
                </div>
                <div id="clicky">
                    <a title="Web Analytics (opens in new tab)" href="https://clicky.com/101459580" target="_blank" rel="noopener">
                        <img alt="Clicky" src="/icons/click-badge.gif" height="15" width="80"></a>
                </div>
            </footer>`
        const clicky = document.createElement("script")
        clicky.async = true
        clicky.dataset.id = "101459580"
        clicky.src = "//static.getclicky.com/js"
        this.querySelector("#clicky").append(clicky)
    }
})
