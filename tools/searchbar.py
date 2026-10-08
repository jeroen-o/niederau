"""Markup van de zoekbalk bovenaan elke pagina (NL/EN/DE); de logica staat in assets/search.js."""
TXT = {
    "nl": ("Zoek op de hele site", "Zoek op de hele site…", "Zoekresultaten"),
    "en": ("Search the whole site", "Search the whole site…", "Search results"),
    "de": ("Die ganze Website durchsuchen", "Die ganze Website durchsuchen …", "Suchergebnisse"),
}

def bar(lang):
    lab, ph, res = TXT[lang]
    return (f'<div class="searchbar" role="search"><div class="wrap"><label class="sr-only" for="q">{lab}</label>'
            f'<svg class="q-ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="m15.5 15.5 5 5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
            f'<input id="q" type="text" enterkeyhint="search" placeholder="{ph}" autocomplete="off" spellcheck="false" role="combobox" aria-expanded="false" aria-controls="q-res" aria-autocomplete="list">'
            f'<ul id="q-res" class="q-res" role="listbox" aria-label="{res}" hidden></ul>'
            f'<div id="q-st" class="sr-only" role="status" aria-live="polite"></div></div></div>')

NOSCRIPT = ''  # zoekbalk is standaard verborgen en verschijnt via html.js (zie CSS)
