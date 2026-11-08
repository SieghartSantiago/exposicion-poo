export function escapeHtml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

const PY_TOKEN_RE =
  /("""[^"]*"""|f?"[^"]*"|f?'[^']*'|#.*$|@\w+|\b(?:class|def|if|elif|else|for|in|or|and|not|is|return|raise|try|except|as|assert|from|import|pass|lambda|with|None|True|False|super)\b|\b(?:ABC|Protocol|dataclass|abstractmethod|property|ValueError|TypeError|AttributeError|NotImplementedError|float|int|str|bool|list|dict|tuple|Iterable|Callable|Any|Self|print|sum|map|filter|len|isinstance|id|self)\b|\b\d[\d_.]*\b)/g;

const KEYWORDS = new Set([
  "class",
  "def",
  "if",
  "elif",
  "else",
  "for",
  "in",
  "or",
  "and",
  "not",
  "is",
  "return",
  "raise",
  "try",
  "except",
  "as",
  "assert",
  "from",
  "import",
  "pass",
  "lambda",
  "with",
  "None",
  "True",
  "False",
  "super",
]);

const TYPES_AND_BUILTINS = new Set([
  "ABC",
  "Protocol",
  "dataclass",
  "abstractmethod",
  "property",
  "ValueError",
  "TypeError",
  "AttributeError",
  "NotImplementedError",
  "float",
  "int",
  "str",
  "bool",
  "list",
  "dict",
  "tuple",
  "Iterable",
  "Callable",
  "Any",
  "Self",
  "print",
  "sum",
  "map",
  "filter",
  "len",
  "isinstance",
  "id",
  "self",
]);

export function highlightPythonLine(line: string): string {
  if (!line) return "&nbsp;";

  let result = "";
  let lastIndex = 0;

  for (const match of line.matchAll(PY_TOKEN_RE)) {
    const idx = match.index ?? 0;
    if (idx > lastIndex) {
      result += escapeHtml(line.slice(lastIndex, idx));
    }

    const token = match[0];
    const escaped = escapeHtml(token);

    if (token.startsWith("#")) {
      result += `<span class="tok-com">${escaped}</span>`;
    } else if (
      token.startsWith('"') ||
      token.startsWith("'") ||
      token.startsWith('f"') ||
      token.startsWith("f'")
    ) {
      result += `<span class="tok-str">${escaped}</span>`;
    } else if (token.startsWith("@")) {
      result += `<span class="tok-dec">${escaped}</span>`;
    } else if (KEYWORDS.has(token)) {
      result += `<span class="tok-kw">${escaped}</span>`;
    } else if (TYPES_AND_BUILTINS.has(token)) {
      result += `<span class="tok-type">${escaped}</span>`;
    } else {
      result += `<span class="tok-num">${escaped}</span>`;
    }

    lastIndex = idx + token.length;
  }

  if (lastIndex < line.length) {
    result += escapeHtml(line.slice(lastIndex));
  }

  return result;
}
