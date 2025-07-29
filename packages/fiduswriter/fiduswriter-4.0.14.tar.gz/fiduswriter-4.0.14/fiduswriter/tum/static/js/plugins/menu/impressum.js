// Adds a link to the impressum on the overview pages.

export class ImpressumMenuItem {
    constructor(menu) {
        this.menu = menu
    }

    init() {
        this.menu.navItems.push({
            id: "impressum",
            title: gettext("Impressum"),
            url: "/pages/impressum/",
            text: "Impressum",
            order: 10
        })
    }
}
