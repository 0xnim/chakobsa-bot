import re
import urllib.request


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

    print(f"Lookup was:\n{lookup}")

    return lookup


def get_chakobsa_page(word: str) -> str:
    """
    Get the corresponding wiki page for a Chakobsa word.
    @param word The Chakobsa word to get the wiki page for
    @return The wiki page in HTML, or an empty string if the page is not found
    """
    lookup = get_chakobsa_lemma_lookup()
    route = lookup[word]
    if not route:
        # Didn't find the route for the page, early out
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


def parse_page(text: str) -> dict[str, str]:
    """
    Parse a wiki page returning only the relevant Chakobsa section fields and
    their values
    @param text The html text of the page to parse
    @return A dictionary containing the the Chakobsa sections and their values,
            hierarchically
    """
    if not text:
        return {"Error": "Unable to find page matching that word."}

    return {}


def format_definition(sections: dict[str, str]) -> str:
    """
    Format a series of sections and values in plaintext as a word definition.
    @param sections The sections of the Chakobsa part of the wiki page and
                    their values
    @return The formatted sections as a plaintext definition
    """
    return ""


def get_definition(word: str, in_chakobsa=True) -> str:
    """
    Get the definition of a word in plaintext.
    @param word         The word to get the definition of
    @param in_chakobsa  Is the word parameter in Chakobsa?
    """
    page_text = get_page(word, in_chakobsa)
    sections = parse_page(page_text)
    return format_definition(sections)


if __name__ == "__main__":
    print(f"Lookup for Zama returned:\n{get_chakobsa_page('zama')}")
