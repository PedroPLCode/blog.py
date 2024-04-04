import { settings } from "./settings.js";

class CheckAndSetFieldVisibility {
  constructor(select, custom) {
  this.select = select;
  this.custom = custom;
  this.getElements();
  this.initActions();
  }
  
  getElements = () => {
    this.dom = {
      selectField: document.getElementById(this.select),
      customField: document.querySelector(this.custom),
    }
  }
  
  initActions = () => {
    if (this.dom.selectField && this.dom.customField) {
      this.checkAndSetcustomFieldVisibility();
    this.dom.selectField.addEventListener('change', () => {
      this.checkAndSetcustomFieldVisibility();
    });
    }
  }

  checkAndSetcustomFieldVisibility = () => {
    const options = this.dom.selectField.querySelectorAll(settings.selectors.option);
    let customOptionSelected = false;
    for (let option of options) {
      if (option.value === 'new category' && option.selected) {
        customOptionSelected = true;
        break;
      }
    }
    if (customOptionSelected) {
      this.dom.customField.style.opacity = '1';
    } else {
      this.dom.customField.style.opacity = '.25';
    }
  };
}
  
export default CheckAndSetFieldVisibility;