# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
from .parser import Parser as Parser
from .tokenizer import tokenize as tokenize
from typing import Any

def parse_expression(exp: Any): ...
def parse_member_signature(sig: Any): ...
def parse_constructor_signature(sig: Any): ...
def parse_type(s: Any): ...
def parse_type_signature(sig: Any): ...
def parse(s: Any): ...
