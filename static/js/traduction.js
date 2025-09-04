function googleTranslateElementInit() {
    new google.translate.TranslateElement(
      {
        pageLanguage: 'fr', 
        includedLanguages: 'en,fr',
        autoDisplay: false
      }, 
      'google_translate_element'
    );
  }

  function translateLanguage(lang) {
    var selectField = document.querySelector("select.goog-te-combo");
    if (selectField) {
      selectField.value = lang;
      selectField.dispatchEvent(new Event("change"));
    }
  }