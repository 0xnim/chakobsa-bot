import re
import urllib.request

import html2text


def get_chakobsa_lemma_lookup() -> dict[str, str]:
    """
    Construct a mapping of Chakobsa terms to routes on the wiki.
    @return A dictionary that maps lowercase chakobsa words to routes, starting
            at /
    """
    # Grab the main page contents, has all known words on it
    contents = (
        urllib.request.urlopen(
            "https://wiki.languageinvention.com/index.php?title=Category:Chakobsa_lemmas"
        )
        .read()
        .decode()
    )

    # Narrow down to only lines that contain links to words, and construct a
    # dictionary
    lookup = dict(
        (value.lower(), key)
        for (key, value) in re.findall(
            r'^.*<li><a href="(\/index\.php\?title=([A-Za-z\']+))" .*<\/a><\/li>.*$',
            contents,
            re.MULTILINE,
        )
    )

    return lookup


def get_chakobsa_page(word: str) -> str:
    """
    Get the corresponding wiki page for a Chakobsa word.
    @param word The Chakobsa word to get the wiki page for
    @return The wiki page in HTML, or an empty string if the page is not found
    """
    lookup = get_chakobsa_lemma_lookup()
    route = ""

    try:
        route = lookup[word]
    except:
        # Failed the lookup, route/word doesn't exist
        return ""

    # We found the word, request the page
    contents = (
        urllib.request.urlopen(f"https://wiki.languageinvention.com{route}")
        .read()
        .decode()
    )

    return contents


def get_english_page(word: str) -> str:
    """
    Get the corresponding wiki page for the Chakobsa translation of the English
    word.
    @param word The English word to get the Chakobsa wiki page for
    @return The wiki page in HTML, or an empty string if the page is not found
    """
    # TODO: Implement English -> Chakobsa searching
    return ""


def get_page(word: str, in_chakobsa=True) -> str:
    """
    Get the corresponding wiki page for the word.
    @param word         The word to get the wiki page for
    @param in_chakobsa  Is the word parameter in Chakobsa?
    @return The wiki page in HTML, or an empty string if the page is not found
    """
    contents = ""
    if in_chakobsa:
        contents = get_chakobsa_page(word)
    else:
        contents = get_english_page(word)
    return contents


def parse_page(text: str) -> str:
    """
    Parse a wiki page returning only the relevant Chakobsa section fields and
    their values
    @param text The html text of the page to parse
    @return A plaintext formatting of the Chakobsa sections and their values
    """
    if not text:
        return "Error: Unable to find page matching that word."

    # Get only the relevant section
    match = re.search(
        r'<h2><span class="mw-headline" id="Chakobsa"><a href="\/index\.php\?ti'
        r'tle=Chakobsa_language" title="Chakobsa language">Chakobsa<\/a>'
        r"<\/span><\/h2>(.*?)<!--",
        text,
        re.MULTILINE | re.DOTALL,
    )

    if not match:
        return "Error: Unable to parse definition page."

    # Just the text
    body = match[1]

    # TODO: Include conjugation table. Since this will require a fair bit of
    #       formatting, I've opted to just snip them out for now.
    body = re.sub(r"<table.*</table>", "", body, flags=re.MULTILINE | re.DOTALL)

    # Parse and prettify
    text_maker = html2text.HTML2Text()
    text_maker.unicode_snob = True  # IMPORTANT! Needed for IPA
    text_maker.ignore_links = True  # Links make the message too long
    text_maker.body_width = 0  # Don't wrap

    text_maker.ignore_tables = True  # TODO: Maybe change when tables work

    formatted = text_maker.handle(body)

    # Clean up output by removing...
    # ... More than one consecutive newline
    formatted = re.sub(r"\s{2,}", "\n", formatted, flags=re.MULTILINE | re.DOTALL)
    # ... High level headers
    formatted = re.sub(r"^##", "", formatted, flags=re.MULTILINE)
    # ... Extraneous headers
    formatted = re.sub(
        r"^#+ Orthographic Form.*?#", "#", formatted, flags=re.MULTILINE | re.DOTALL
    )
    # TODO: When tables are added, come back to this
    formatted = re.sub(
        r"^#+ Inflection\n", "", formatted, flags=re.MULTILINE | re.DOTALL
    )
    return formatted


def get_definition(word: str, in_chakobsa=True) -> str:
    """
    Get the definition of a word in plaintext.
    @param word         The word to get the definition of
    @param in_chakobsa  Is the word parameter in Chakobsa?
    """
    page_text = get_page(word, in_chakobsa)
    formatted = parse_page(page_text)
    return formatted
