# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
from bs4.builder import HTMLTreeBuilder
from html.parser import HTMLParser
from typing import Any, Optional

class HTMLParseError(Exception): ...

class BeautifulSoupHTMLParser(HTMLParser):
    already_closed_empty_element: Any = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def error(self, msg: Any) -> None: ...
    def handle_startendtag(self, name: Any, attrs: Any) -> None: ...
    def handle_starttag(self, name: Any, attrs: Any, handle_empty_element: bool = ...) -> None: ...
    def handle_endtag(self, name: Any, check_already_closed: bool = ...) -> None: ...
    def handle_data(self, data: Any) -> None: ...
    def handle_charref(self, name: Any) -> None: ...
    def handle_entityref(self, name: Any) -> None: ...
    def handle_comment(self, data: Any) -> None: ...
    def handle_decl(self, data: Any) -> None: ...
    def unknown_decl(self, data: Any) -> None: ...
    def handle_pi(self, data: Any) -> None: ...

class HTMLParserTreeBuilder(HTMLTreeBuilder):
    is_xml: bool = ...
    picklable: bool = ...
    NAME: Any = ...
    features: Any = ...
    TRACKS_LINE_NUMBERS: bool = ...
    parser_args: Any = ...
    def __init__(self, parser_args: Optional[Any] = ..., parser_kwargs: Optional[Any] = ..., **kwargs: Any) -> None: ...
    def prepare_markup(self, markup: Any, user_specified_encoding: Optional[Any] = ..., document_declared_encoding: Optional[Any] = ..., exclude_encodings: Optional[Any] = ...) -> None: ...
    def feed(self, markup: Any) -> None: ...
