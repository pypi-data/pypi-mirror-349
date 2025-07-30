import re
from datetime import datetime, date
from typing import List

def replace_pow_with_exp(sql_str):
    output = []
    i = 0
    while i < len(sql_str):
        char = sql_str[i]
        if char == 'p' and sql_str[i:i + 4] == 'pow(':
            # Start replacing 'pow(' with '^'
            i += 4  # Skip past 'pow('
            base = ""
            while not re.match(r'\s*,\s*', sql_str[i:i + 2]):
                base += sql_str[i]
                i += 1

            i += 1  # Skip past the comma

            exponent = ""
            paren_count = 1  # Counting the opening parenthesis of pow( itself
            while paren_count > 0:
                if sql_str[i] == '(':
                    paren_count += 1
                elif sql_str[i] == ')':
                    paren_count -= 1
                exponent += sql_str[i]
                i += 1

            exponent = exponent[:-1]  # Remove the last ')'

            if base.strip() == '10' or base.strip() == '5':
                output.append(f"{base.strip()} ^ {exponent}")
        else:
            output.append(char)
            i += 1
    return ''.join(output)


def convert_query_for_vfp(query: str, parameters: List = []):
    """
    Convert a query for VFP SQL syntax, it will also convert the column names and labels to the VFP syntax.
    Args:
        query (str): query to convert
        parameters (list): list of parameters to convert

    Returns:
        str: converted query

    """

    converted_parameters = []

    for param in parameters:
        if isinstance(param, str):
            converted_parameters.append(f"'{param}'")  # wrap strings in single quotes
        elif isinstance(param, int):
            converted_parameters.append(str(param))  # integers can be used as-is
        elif isinstance(param, float):
            converted_parameters.append(str(param))  # floats can be used as-is
        elif isinstance(param, datetime):
            converted_parameters.append(
                f"""{{ts '{param.strftime('%Y-%m-%d %H:%M:%S')}'}}"""
            )
        elif isinstance(param, date):
            converted_parameters.append(f"""{{d '{param.strftime('%Y-%m-%d')}'}}""")
        elif param is None:
            converted_parameters.append("NULL")  # handle None as SQL NULL
        else:
            converted_parameters.append(str(param))  # fallback: convert to string

    split_query = query.split("?")

    if len(split_query) - 1 != len(parameters):
        raise ValueError("Number of placeholders doesn't match number of parameters.")

    # Zip the split query and the converted parameters, concatenating each pair
    converted_query = "".join(
        [q + p for q, p in zip(split_query, converted_parameters)]
    )
    converted_query += split_query[-1]  # append the last part of the split query

    limit_offset_pattern = re.compile(
        r"\bLIMIT\s+(\d+)|\bOFFSET\s+(\d+)", re.IGNORECASE
    )

    def replacer(match):
        if match is None:
            return ""
        limit = match.group(1)
        offset = match.group(2)
        return f"{f'TOP {limit}' if limit else ''} {f'SKIP {offset}' if offset else ''}".strip()

    def custom_lstrip(target_str, pattern="SELECT "):
        if target_str.startswith(pattern):
            return target_str[len(pattern):]
        return target_str

    modified_query = re.sub(
        r"\bSELECT\b(.*?)(?=SELECT|\Z)",
        lambda m: "SELECT "
                  + replacer(re.search(limit_offset_pattern, m.group(0)))
                  + " "
                  + re.sub(limit_offset_pattern, "", custom_lstrip(m.group(0))),
        converted_query,
        flags=re.IGNORECASE | re.DOTALL,
    )

    return replace_pow_with_exp(convert_column_names_and_labels(modified_query.strip()))


def convert_column_names_and_labels(query):
    # Remove double quotes around column names in the pattern {table_name}."{column_name}"
    query = re.sub(r'"\w+"', lambda x: x.group().replace('"', ""), query)

    # Replace double quotes with single quotes in the pattern AS "{label}"
    query = re.sub(r'AS "([\w_]+)"', lambda x: f"AS '{x.group(1)}'", query)

    return query
