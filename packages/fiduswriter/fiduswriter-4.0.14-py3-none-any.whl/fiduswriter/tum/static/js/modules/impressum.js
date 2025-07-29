export class ImpressumLink {
    constructor(prelogin) {
        this.page = prelogin.page
    }

    init() {
        this.page.footerLinks.push({
            text: "Impressum",
            link: "/pages/impressum/"
        })
    }
}
