import "semantic-ui-css";

import $ from "jquery";
import { MultipleOptionsSearchBar } from "@js/invenio_search_ui/components";
import React from "react";
import ReactDOM from "react-dom";
import { i18next } from "@translations/invenio_app_rdm/i18next";

/* sticky notification setup for test instance */
$(".ui.sticky.test-instance").sticky({
  context: "body",
});

/* load Zammad script on document ready
$(function () {
  importZammadScript();
});
*/

/* function to import Zammad script for feedback form
function importZammadScript() {
  let scriptNode = document.createElement("hidden");
  scriptNode.id = "zammad_form_script";
  scriptNode.src = "URL";
  document.head.appendChild(scriptNode);

  $.getScript("URL", () => {
    $("#feedback-form").ZammadForm({
      messageTitle: "Contact us",
      showTitle: true,
      messageSubmit: "Submit",
      messageThankYou: "Thank you for your message, (#%s). We will get back to you as quickly as possible!",
      modal: true,
    });
  });
}
*/

/* function to toggle visibility of an element by ID
export function toggleVisibility(id) {
  const element = document.getElementById(id);
  const isHidden = element.style.display === "none";
  element.style.display = isHidden ? "block" : "none";
}
window.toggleVisibility = toggleVisibility;
*/

document.addEventListener("DOMContentLoaded", function () {

  const frontpageSearchbar = document.getElementById("frontpage-search-bar");

  if (frontpageSearchbar) {
    const searchBarOptions = JSON.parse(frontpageSearchbar.dataset.options);

    ReactDOM.render(
      <div className="ui fluid input frontpage-search-container">
        <MultipleOptionsSearchBar
          options={searchBarOptions}
          placeholder={i18next.t("Search records...")}
        />
      </div>,
      frontpageSearchbar
    );
  }
});
