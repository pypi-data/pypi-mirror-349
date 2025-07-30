/* Tooltip properties
    including theme, placement, animation, arrow, etc
    */
// Match Tooltip's theme with Material's color scheme
function getCurrentTheme() {
    const scheme = document.body?.getAttribute('data-md-color-scheme') || 'default';
    return scheme === 'slate' ? 'material' : 'light';
}
// Configure the properties of the Tooltip here, available documents: https://atomiks.github.io/tippyjs/
const tippyInstances = tippy('[data-tippy-content]', {

    theme: getCurrentTheme(),   // configurable: light material, or custom theme in document-dates.config.css
    placement: 'bottom',        // placement: top bottom left right auto
    offset: [0, 5],             // placement offset: [horizontal, vertical]
    // interactive: true,          // content in Tooltip is interactive

    animation: 'scale',         // animation type: scale shift-away
    inertia: true,              // animation inertia
    // arrow: false,               // whether to allow arrows

    // animateFill: true,          // determines if the background fill color should be animated

    // delay: [400, null],         // delay: [show, hide], show delay is 400ms, hide delay is the default
});


/* Automatic theme switching
    Set Tooltip's theme to change automatically with the Material's light/dark color scheme
    If you don't need this feature, just delete the code below
    */
const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.attributeName === 'data-md-color-scheme') {
            const newTheme = getCurrentTheme();
            tippyInstances.forEach(instance => {
                instance.setProps({ theme: newTheme });
            });
        }
    });
});
observer.observe(document.body, {
    attributes: true,
    attributeFilter: ['data-md-color-scheme']
});
