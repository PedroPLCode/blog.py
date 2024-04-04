import { settings } from "./settings.js";
import CheckAndSetFieldVisibility from "./CheckAndSetFieldVisibility.js";

export const app = {
  init: function() {
    this.checkNewCategoryField = new CheckAndSetFieldVisibility(
        settings.selectors.category,
        settings.selectors.newCategory,
        );
  }
}

app.init();