// Theme toggle: cycles auto -> light -> dark. "auto" removes html[data-theme] so
// CSS falls back to prefers-color-scheme; light/dark pin it. The inline <head>
// script applies a stored choice before first paint; this keeps them in sync.
const THEME_CYCLE = ["auto", "light", "dark"]

const THEME_ICON = {
    auto: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
                <circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 0 0 18z" fill="currentColor" stroke="none"/></svg>`,
    dark: `<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>`,
    light: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
                <circle cx="12" cy="12" r="4"/>
                <path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M19.1 4.9l-1.4 1.4M6.3 17.7l-1.4 1.4"/></svg>`,
}

const storedTheme = () => localStorage.getItem("theme") || "auto"

const applyTheme = theme => {
    const root = document.documentElement
    if (theme === "auto") delete root.dataset.theme
    else root.dataset.theme = theme
}

// The header/nav is server-rendered HTML now (no layout shift on load), so JS
// only enhances the theme button that's already in the DOM: fills its icon and
// wires the click. Module scripts are deferred, so the button exists by now.
const wireThemeToggle = () => {
    const button = document.querySelector(".theme-toggle")
    if (!button) return

    const showTheme = theme => {
        applyTheme(theme)
        button.innerHTML = THEME_ICON[theme]
        button.title = `Theme: ${theme}`
        button.setAttribute("aria-label", `Theme: ${theme}. Activate to change.`)
    }

    button.addEventListener("click", () => {
        const next = THEME_CYCLE[(THEME_CYCLE.indexOf(storedTheme()) + 1) % THEME_CYCLE.length]
        localStorage.setItem("theme", next)
        showTheme(next)
    })
    showTheme(storedTheme())
}

wireThemeToggle()

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
