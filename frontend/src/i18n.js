function _(key, lang) {
  let keys = {
    'nn': {
      'Type here to search': "Søk etter eit ord her",
      'Choose a word from list to the left': "Vel eit ord frå lista til venstre",
      'Copyright notice': <>Data på denne sida er samla frå <a href="http://en.wiktionary.org">Wikiordboka, eit Wikimedia-prosjekt</a>.</>,
      'Read more': ''// <>Du kan lesa om korleis dette fungerer <a href="/blog/2022/01/16/...">på bloggen min</a></>
    },
    'en': {
      'Copyright notice': <>Data provided is collected from <a href="http://en.wiktionary.org">Wiktionary, a Wikimedia project</a>.</>,
      'Read more': ''// <>You can read about how this page works at <a href="/blog/2022/01/16/...">my blog</a></>
    }
  }

  let internationalized = keys[lang][key]
  if (internationalized === undefined) {
    return key;
  }
  return internationalized;
}

export default _;
