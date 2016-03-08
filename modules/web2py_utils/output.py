#
#  Copyright (C) 2009 Thadeus Burgess
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>
#

import re

def compress_output(response, 
                        startswith = [
                            '<pre',
                            '<textarea',
                            '<blockquote',
                        ],
                        funcs=[], 
                        debug=False,):

    def save_pre(match):
        s = match.group()
        for sw in startswith:
            if s.startswith(sw):
                return s
        return '' # this turns whitespace into nothing

    def compress_response(d):
        if callable(d):
            d = d()
        if isinstance(d, dict):
            cpat = re.compile(r'[\n\t\r\f\v]|(?s)\s\s\s|(?s)<pre(.*?)</pre>|(?s)<blockquote(.*?)</blockquote>|(?s)<textarea(.*?)</textarea>')
            d = cpat.sub(save_pre, response.render(d))
            for f in funcs:
                if callable(f):
                    f(d)
        return d

    if not debug:
        response._caller = compress_response


def html_entity_decode(text):
    """
    Removes HTML or XML character references and entities from a text string.
    
    @param text The HTML (or XML) source text.
    @return The plain text, as a Unicode string, if necessary.
    """
    import re, htmlentitydefs
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

def __highlight__(content, dom_element='pre', linenos=True, noclasses=True):
    """
    Performs syntax highlighting on text inside of dom_element
    Uses BeautifulSoup for processing and pygments for highlighting
    
    @param content The HTML (or XML) content to parse
    @param dom_element The dom tag to search and replace with highlighted
    @return The content with highlighted code withing dom_element
    
    """
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import HtmlFormatter
    from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
    
    decodedString=unicode(BeautifulStoneSoup(content,convertEntities=BeautifulStoneSoup.HTML_ENTITIES ))
    #decodedString=html_entity_decode(content.encode('utf-8'))
    soup = BeautifulSoup(content)
    
    formatter = HtmlFormatter(linenos=linenos, noclasses=noclasses)
    
    for tag in soup.findAll(dom_element):
        language = tag.get('lang') or 'text'
        try:
            lexer = get_lexer_by_name(language, encoding='UTF-8')
        except:
            lexer = get_lexer_by_name('text', encoding='UTF-8')
        tag.replaceWith(highlight(tag.renderContents(), lexer, formatter))
        pass
    return unicode(str(soup), 'utf-8', errors='ignore')
    
