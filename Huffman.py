import os

# obliczenie ile razy występuje dany znak
def calculate_frequencies(text):
    frequencies = {}
    for char in text:
        if char in frequencies:
            frequencies[char] += 1
        else:
            frequencies[char] = 1
    return list(frequencies.items())

def heapify(heap, n, i):
    smallest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and heap[left]['freq'] < heap[smallest]['freq']:
        smallest = left

    if right < n and heap[right]['freq'] < heap[smallest]['freq']:
        smallest = right

    if smallest != i:
        heap[i], heap[smallest] = heap[smallest], heap[i]
        heapify(heap, n, smallest)

def build_min_heap(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

def insert_into_queue(Q, node):
    Q.append(node)
    i = len(Q) - 1
    while i > 0:
        parent = (i - 1) // 2
        if Q[i]['freq'] < Q[parent]['freq']:
            Q[i], Q[parent] = Q[parent], Q[i]
            i = parent
        else:
            break

    # if node['label'] is None:
    #     label = f"'{node['left']['label']}{node['right']['label']}'"
    # else:
    #     label = f"'{node['label']}'"
    # print(f"Insert(Q, {label}:{node['freq']})")

def pop_from_queue(Q):
    n = len(Q)
    if n == 0:
        return None
    if n == 1:
        return Q.pop(0)
    root = Q[0]
    Q[0] = Q.pop()
    heapify(Q, len(Q), 0)
    return root

def build_priority_queue(frequencies):
    Q = []
    for char, freq in frequencies:
        Q.append({
            'label': char,
            'freq': freq,
            'left': None,
            'right': None
        })
    build_min_heap(Q)
    return Q

def print_queue(Q):
    print("Q: ", end="")
    for node in Q:
        if node['label'] is None:
            label = f"'{node['left']['label']}{node['right']['label']}'"
        else:
            label = f"'{node['label']}'"
        print(f"{label}:{node['freq']}", end=" ")
    print()

def build_tree(Q):
    while len(Q) > 1:
        # print_queue(Q)
        x = pop_from_queue(Q)
        # print(f"z.left = '{node1['label']}':{node1['freq']}")
        # print_queue(Q)
        y = pop_from_queue(Q)
        # print(f"z.right = '{node2['label']}':{node2['freq']}")
        # print_queue(Q)

        new_node = {
            'label': f"{x['label']}{y['label']}",
            'freq': x['freq'] + y['freq'],
            'left': x,
            'right': y
        }

        insert_into_queue(Q, new_node)
        # print()

    return Q[0]

def generate_codes(node, current_code='', codes=None):
    if codes is None:
        codes = []

    # jeśli węzeł jest liściem (ma znak) - zapisujemy jego kod
    if node['left'] is None and node['right'] is None:
        codes.append((node['label'], current_code if current_code else '0'))
    else:
        # przejście rekurencyjne przez lewe (0) i prawe (1) poddrzewo
        if node['left']:
            generate_codes(node['left'], current_code + '0', codes)
        if node['right']:
            generate_codes(node['right'], current_code + '1', codes)

    return codes

def encoding(text, codes):
    encoded = ""
    codes = dict(codes)
    for char in text:
        encoded += codes[char]
    return encoded

def decoding(encoded_text, root):
    decoded = ""
    current_node = root

    for bit in encoded_text:
        if bit == '0':
            current_node = current_node['left']
        else:
            current_node = current_node['right']

        # dotarcie do liścia
        if current_node['left'] is None and current_node['right'] is None:
            # zapisuje znak
            decoded += current_node['label']
            # wraca do korzenia
            current_node = root

    return decoded

def build_tree_from_codes(codes):
    root = {'label': None, 'left': None, 'right': None}

    for char, code in codes.items():
        current = root

        for bit in code[:-1]:  # Process all bits except the last one
            if bit == '0':
                if current['left'] is None:
                    current['left'] = {'label': None, 'left': None, 'right': None}
                current = current['left']
            else:
                if current['right'] is None:
                    current['right'] = {'label': None, 'left': None, 'right': None}
                current = current['right']

        # Process the last bit and add the character
        if code[-1] == '0':
            current['left'] = {'label': char, 'left': None, 'right': None}
        else:
            current['right'] = {'label': char, 'left': None, 'right': None}

    return root

def read_encoded_file(filename):
    with open(filename, 'rb') as f:
        header = b""
        while not header.endswith(b"\n\n"):
            header += f.read(1)
        header = header.decode('utf-8').strip()
        codes = {}
        for line in header.split():
            char, code = line.split(":")
            if char == "\\s":
                char = ' '
            elif char == "\\n":
                char = '\n'
            elif char == "\\t":
                char = '\t'
            elif char == "\\r":
                char = '\r'
            else:
                char = eval("'" + char + "'")
            codes[char] = code

        padding = f.read(1)[0]
        bits = f.read()
        encoded = ''.join(format(byte, '08b') for byte in bits)

        if padding > 0:
            binary_str = encoded[:-padding]

        return codes, binary_str

def save_encoded_file(filename, codes, encoded_text):
    output_filename = f"{os.path.splitext(filename)[0]}-zaszyfrowane.txt"

    header = ""
    for char, code in codes.items():
        if char == ' ':
            char_repr = "\\s"
        elif char == '\n':
            char_repr = "\\n"
        elif char == '\t':
            char_repr = "\\t"
        elif char == '\r':
            char_repr = "\\r"
        else:
            char_repr = repr(char)[1:-1]
        header += f"{char_repr}:{code} "
    header += "\n\n"

    padding = 8 - (len(encoded_text) % 8)
    encoded_text += "0" * padding

    bits = bytearray(int(encoded_text[i:i + 8], 2) for i in range(0, len(encoded_text), 8))

    with open(output_filename, 'wb') as f:
        f.write(header.encode('utf-8'))
        f.write(bytes([padding]))
        f.write(bits)

    return output_filename

def save_decoded_file(decoded_text, filename):
    output_filename = f"{os.path.splitext(filename)[0].replace('-zaszyfrowane', '')}-odszyfrowane.txt"
    try:
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write(decoded_text)
    except:
        print(f"Nie udało się zapisać pliku {output_filename}")
    return output_filename

def process_file(filename, mode):
    if mode == 'encrypt':
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                text = file.read()
        except:
            print(f"Nie udało się otworzyć pliku {filename}")
            return

        if len(text) == 0:
            print("Plik jest pusty")
            return

        frequencies = calculate_frequencies(text)
        queue = build_priority_queue(frequencies)
        root = build_tree(queue)
        codes = dict(generate_codes(root))
        encoded_text = encoding(text, codes)
        print(f"Długość zakodowanego tekstu: {len(encoded_text)} bitów")
        output_filename = save_encoded_file(filename, codes, encoded_text)
        print(f"Zapisano zaszyfrowany plik jako: {output_filename}")

    elif mode == 'decrypt':
        try:
            codes, encoded_text = read_encoded_file(filename)
        except:
            print(f"Nie udało się odczytać pliku {filename}")
            return

        root = build_tree_from_codes(codes)
        decoded_text = decoding(encoded_text, root)
        output_filename = save_decoded_file(decoded_text, filename)
        print(f"Zapisano odszyfrowany plik jako: {output_filename}")

while True:
    choice = input("Co chcesz zrobić: szyfruj (s) / deszyfruj (d) / zakończ (z): ").strip().lower()
    if choice == 'z':
        break
    elif choice in ('s', 'd'):
        number_of_files = 0
        while number_of_files <= 0:
            user_input = input("Podaj liczbę plików do przetworzenia: ")
            if user_input.isdigit():
                number_of_files = int(user_input)
                if number_of_files <= 0:
                    print("Liczba plików musi być większa od zera")
            else:
                print("Liczba plików musi być całkowita")

        for i in range(1, number_of_files + 1):
            while True:
                filename = input(f"Podaj nazwę pliku {i}: ").strip()
                if os.path.exists(filename):
                    if choice == 's':
                        process_file(filename, 'encrypt')
                    else:
                        process_file(filename, 'decrypt')
                    break
                else:
                    print(f"Plik {filename} nie istnieje. Podaj poprawną nazwę.")
    else:
        print("Nieprawidłowy wybór")
