/** @odoo-module **/

import {Component} from "@odoo/owl";
import {registry} from "@web/core/registry";

export class WebCompanyLogo extends Component {
    setup() {
        var url = window.location.origin;
        var companyId = this.env.services.company.currentCompany.id;
        $.ajax({
            type: "GET",
            data: {company_id: companyId},
            url: `${url}/check_company_logo`,
            success: function (result) {
                var result2 = JSON.parse(result);
                if (result2.has_logo === true) {
                    $(
                        "#company-logo"
                    )[0].src = `${url}/web/image?model=res.company&id=${companyId}&field=logo`;
                } else {
                    $("#company-logo-link")[0].remove();
                }
            },
            error: function () {
                console.log("Error encountered");
            },
        });
    }
}
WebCompanyLogo.template = "web_company_logo.WebCompanyLogo";
registry
    .category("systray")
    .add("web_company_logo", {Component: WebCompanyLogo}, {sequence: 1000});
