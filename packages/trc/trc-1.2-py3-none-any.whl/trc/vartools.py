# vartools.py
# Import modules
import random, itertools, inspect, trc, re

# Remove characters from a string
@trc.cache
def clean(string: str = "Hello World!", mode: str = "clean", chars: str = "") -> str:
    if mode == "clean":
        if not isinstance(string, str):
            raise TypeError("string must be a string")
        translation_table = str.maketrans("", "", chars)
        return string.translate(translation_table)
    # accept only chars from the chars param
    elif mode == "only":
        if not isinstance(string, str):
            raise TypeError("string must be a string")
        return "".join(char for char in string if char in chars)
    elif mode == "ascii":
        if not isinstance(string, str):
            raise TypeError("string must be a string")
        return "".join(char for char in string if char.isascii())
    else:
        raise ValueError("mode must be 'clean' or 'only'")

# Merge multiple lists or dictionaries
@trc.cache
def merge(*args: list | dict, duplicate: bool = False, deep: bool = False) -> list | dict:
    if not args:
        raise ValueError("No arguments provided")
    first_type = type(args[0])
    if not all(isinstance(arg, first_type) for arg in args):
        return False
    if first_type is list:
        if duplicate:
            return list(itertools.chain(*args))
        return list(dict.fromkeys(itertools.chain(*args)))
    elif first_type is dict:
        result = {}
        for d in args:
            if deep:
                for key, value in d.items():
                    if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                        result[key] = merge(result[key], value, deep=True)
                    else:
                        result[key] = value
            else:
                result.update({k: v for k, v in d.items() if k not in result})
        return result
    raise TypeError(f"Unsupported type/s: {', '.join(type(arg).__name__ for arg in args)}")

# Remove duplicates
@trc.cache
def unique(obj: list | str, preserve_order: bool = True) -> list | str:
    if preserve_order:
        return list(dict.fromkeys(obj))
    else:
        return list(set(obj))

# Flatten a nested list
@trc.cache
def flatten(lst: list) -> list:
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    flat_list = []
    for element in lst:
        if isinstance(element, list):
            flat_list.extend(flatten(element))
        else:
            flat_list.append(element)
    return flat_list

# Generate a random string
def random_string(length: int, charset: str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') -> str:
    return ''.join(random.choice(charset) for _ in range(length))

# Check if any item in a is in b
@trc.cache
def any_in(a: list | str, b: list | str) -> bool:
    if not isinstance(a, (list, str)) or not isinstance(b, (list, str)):
        raise TypeError("a and b must be lists or strings")
    return any(item in b for item in a)

# Check if all items in a are in b
@trc.cache
def all_in(a: list | str, b: list | str) -> bool:
    if not isinstance(a, (list, str)) or not isinstance(b, (list, str)):
        raise TypeError("a and b must be lists or strings")
    return all(item in b for item in a)

# Format duration
@trc.cache
def format_duration(seconds: int | float | str = 0, type: str = "HH:MM:SS") -> str:
    # type variants: HH:MM:SS, HH"h" MM"m" SS"s"
    if isinstance(seconds, str):
        seconds = float(seconds)
    if type == "HH:MM:SS":
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
    elif type == "Hh:Mm:Ss":
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
    return f"{seconds}s"

# Reverse each objekt in a list or string
@trc.cache
def reverse(obj: list | str) -> list | str:
    if isinstance(obj, (list, tuple)):
        return type(obj)(item[::-1] if isinstance(item, (str, list, tuple)) else item for item in obj)
    elif isinstance(obj, str):
        return obj[::-1]
    return obj

# Get or set a variable
def var(name: str, value: any = None) -> any:
    caller_frame = inspect.currentframe().f_back
    caller_locals = caller_frame.f_locals
    caller_globals = caller_frame.f_globals

    if value is not None:
        if name in caller_locals:
            caller_locals[name] = value
        else:
            caller_globals[name] = value

    if name in caller_locals:
        return caller_locals[name]
    elif name in caller_globals:
        return caller_globals[name]
    else:
        raise NameError(f"Variable '{name}' not found in local or global scope.")

# Slugify a text into an url-friendly string
@trc.cache
def slugify(text: str="Hello World!") -> str:
    text = clean(string=re.sub(r'\W+', '-', text).lower(), mode="ascii")
    if text.endswith("-"):
        text = text[:-1]
    elif text.startswith("-"):
        text = text[1:]
    return text

# Count the words in a text
@trc.cache
def count_words(text: str) -> int:
    return len(text.split())

# Count the characters in a text
@trc.cache
def count_chars(text: str) -> int:
    return len(text)

# Remove all accents from a text
def remove_accents(text: str) -> str:
    return re.sub(r'[^\w\s]', '', text)

# Detect the style of a text
def detect_case(text: str) -> str:
    if re.fullmatch(r'[a-z]+(_[a-z]+)+', text):
        return "snake_case"
    if re.fullmatch(r'[a-z]+(-[a-z]+)+', text):
        return "kebab-case"
    if re.fullmatch(r'[A-Z]+(_[A-Z]+)+', text):
        return "CONSTANT_CASE"
    if re.fullmatch(r'[a-z]+([A-Z][a-z0-9]+)+', text):
        return "camelCase"
    if re.fullmatch(r'([A-Z][a-z0-9]+)+', text):
        return "PascalCase"
    if re.fullmatch(r'([A-Z][a-z0-9]*)( [A-Z][a-z0-9]*)*', text):
        return "Title Case"
    return "unknown"

# Split text into words
@trc.cache
def to_words(text: str) -> list[str]:
    style = detect_case(text)
    if style in ("snake_case", "CONSTANT_CASE"):
        words = text.lower().split('_')
    elif style == "kebab-case":
        words = text.lower().split('-')
    elif style in ("camelCase", "PascalCase"):
        # Insert space before each uppercase letter, then split
        words = re.sub(r'([A-Z])', r' \1', text).strip().split()
        words = [w.lower() for w in words]
    elif style == "Title Case":
        words = [w.lower() for w in text.split(' ')]
    else:
        # Fallback: split on non-alphanumeric
        words = re.findall(r'[A-Za-z0-9]+', text.lower())
    return words

# Snake Case
@trc.cache
def snake_case(text: str) -> str:
    words = to_words(text)
    return '_'.join(words)

# Kebab Case
@trc.cache
def kebab_case(text: str) -> str:
    words = to_words(text)
    return '-'.join(words)

# Constant Case
@trc.cache
def constant_case(text: str) -> str:
    words = to_words(text)
    return '_'.join(w.upper() for w in words)

# Pascal Case
@trc.cache
def pascal_case(text: str) -> str:
    words = to_words(text)
    return ''.join(w.capitalize() for w in words)

# Camel Case
@trc.cache
def camel_case(text: str) -> str:
    p = pascal_case(text)
    return p[0].lower() + p[1:] if p else p

# Title Case
@trc.cache
def title_case(text: str) -> str:
    words = to_words(text)
    return ' '.join(w.capitalize() for w in words)

# Check if an object is a palindrome
@trc.cache
def palindrome(text: str | int | list | tuple) -> bool:
    return text == text[::-1]

# Truncate a text to a maximum length
@trc.cache
def truncate(text: str, max_length: int, ellipsis: str = "...") -> str:
    if len(text) > max_length:
        return text[:max_length - 3] + ellipsis
    return text

# Split a text into words. every word only once in the list
@trc.cache
def list_words(text: str) -> list:
    return list(set(text.split()))