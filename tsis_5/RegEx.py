import re

with open('row.txt', 'r', encoding='utf-8') as file:
    data = file.read()

matches_a_b = re.findall(r'a[b]*', data)
matches_a_bb = re.findall(r'a[b]{2,3}', data)
matches_underscore = re.findall(r'\b[a-z]+_[a-z]+\b', data)
matches_upper_lower = re.findall(r'\b[A-Z][a-z]+\b', data)
matches_a_any_b = re.findall(r'a.*b', data)
replace_chars = re.sub(r'[ ,.]', ':', data)
snake_to_camel = re.sub(r'(_[a-z])', lambda x: x.group(1)[1].upper(), data)
split_uppercase = re.split(r'(?=[A-Z])', data)
insert_spaces = re.sub(r'(?<!^)(?=[A-Z])', ' ', data)
camel_to_snake = re.sub(r'([a-z])([A-Z])', r'\1_\2', data).lower()

results = {
    "matches_a_b": matches_a_b,
    "matches_a_bb": matches_a_bb,
    "matches_underscore": matches_underscore,
    "matches_upper_lower": matches_upper_lower,
    "matches_a_any_b": matches_a_any_b,
    "replace_chars": replace_chars[:500],
    "snake_to_camel": snake_to_camel[:500],
    "split_uppercase": split_uppercase[:20],
    "insert_spaces": insert_spaces[:500],
    "camel_to_snake": camel_to_snake[:500],
}
