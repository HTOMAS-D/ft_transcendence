console.log("SPA loaded");

// Loads a partial and returns the html
async function loadPartial(endpoint) {
    const res = await fetch(endpoint);
    const t = await res.text();
    return t;
}

// Renders a partial and appends it to the location html element
// vars is a dictionary with tags to find and replace (a tag looks like `{{NAME}}`)
function renderPartial(text, location, vars = {}) {
    frag = document.createDocumentFragment();
    temp = document.createElement('div');
    for (const [key, value] of Object.entries(vars))
    {
        text = text.replaceAll(`{{${key}}}`, value);
    }
    temp.innerHTML = text;
    if (temp.firstChild)
    {
        frag.appendChild(temp.firstChild)
    }
    location.appendChild(frag)

    // Start replacing the script tags so they run
    Array.from(location.querySelectorAll("script")).forEach(s =>
        {
            new_s = document.createElement("script");
            new_s.innerHTML = s.innerHTML;
            for (a in s.attributes){
                new_s.setAttribute(a.name, a.value);
            }

            s.parentNode.replaceChild(new_s, s);
        })

}

// Renders a page, removing any html that was inside a location and updating the history
async function renderPage(endpoint, title, location) {
    // Set the title of the page
    document.getElementsByTagName('title')[0].innerText = title
    // Add the page to our history
    history.pushState(title, null, endpoint)

    // Clear any existing data inside the location
    location.innerText = '';
    // Load the new page
    renderPartial(await loadPartial(`/partials/page${endpoint}.html`), location);
}

async function loadInitial(){
    let p = window.location.pathname;
    if (p == '/')
        p = '/home';
    const t = p.substring(p.lastIndexOf('/'));
    const l = document.getElementById('content');
    renderPage(p, t, l);
}

addEventListener("popstate", loadInitial)