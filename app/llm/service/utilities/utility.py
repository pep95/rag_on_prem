import re

def find_real_end(current_start, current_end, text, limit_single_chunk):
    chunk = text[current_start:current_end]
    interruzioni = re.findall("\.\s+", chunk)

    check_dot_newline = False

    for element in interruzioni:
        if "\n" in element:
            check_dot_newline = True
            pattern = "\.\s+"

    if not check_dot_newline:
        interruzioni = re.findall("\n+", chunk)
        check_dot_newline = False
        for element in interruzioni:
            if "\n" in element:
                check_dot_newline = True
                pattern = "\n+"
    if not check_dot_newline:
        interruzioni = re.findall("\.+", chunk)
        check_dot_newline = False
        for element in interruzioni:
            if "\." in element:
                check_dot_newline = True
                pattern = "\.+"

    if not check_dot_newline:
        interruzioni = re.findall("\s+", chunk)
        pattern = "\s+"

    interruzioni = re.finditer(pattern, chunk)
    interruzioni = [element.span() for element in interruzioni]

    try:
        end_real = interruzioni[-1][1]
    except:
        end_real = current_end

    nearest_to_half_chunk = current_start
    distance = limit_single_chunk

    for element in interruzioni:
        current_distance = abs((limit_single_chunk / 2) - element[1])
        if current_distance < distance:
            distance = current_distance
            nearest_to_half_chunk = element[1]

    return end_real, nearest_to_half_chunk + current_start


def split_text_equally(text, limit_single_chunk=1700):
    chunks_nor = []
    chunks_inter = []
    current_start = 0
    current_end = current_start + limit_single_chunk

    while current_end < len(text):
        current_end_real, intermediate_start = find_real_end(current_start, current_end, text, limit_single_chunk)
        chunks_nor.append(text[current_start:current_start + current_end_real])

        intermediate_end = intermediate_start + limit_single_chunk
        intermediate_end_real, _ = find_real_end(intermediate_start, intermediate_end, text, limit_single_chunk)
        chunks_inter.append(text[intermediate_start:intermediate_end_real + intermediate_start])

        current_start += current_end_real
        current_end = current_start + limit_single_chunk

    current_end = len(text) - 1
    current_end_real, intermediate_start = find_real_end(current_start, current_end, text, limit_single_chunk)
    chunks_nor.append(text[current_start:current_start + current_end])

    new_chunk_interm = []
    for intermedio in chunks_inter:
        check = False
        for norm in chunks_nor:
            if intermedio in norm:
                check = True
        if not check:
            new_chunk_interm.append(intermedio)
    chunks = chunks_nor + new_chunk_interm
    return chunks


def create_prompt_with_context(prompt1_path, prompt2_path, context, query):
    file1 = open(prompt1_path, "r")
    prompt1 = file1.read()
    file1.close()

    file2 = open(prompt2_path, "r")
    prompt2 = file2.read()
    file2.close()
    return prompt1 + context + prompt2 + query + " [/INST]"
def create_prompt_without_context(prompt1_path, query):
    file1 = open(prompt1_path, "r")
    prompt1 = file1.read()
    file1.close()
    return prompt1 + query + " [/INST]"
