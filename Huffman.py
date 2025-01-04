import os

# obliczenie ile razy występuje dany znak
def calculate_frequencies(text):
    frequencies = []

    for char in text:
        found = False
        # tworzenie par: (znak, liczba_wystąpień)
        for i in range(len(frequencies)):
            if frequencies[i][0] == char:
                frequencies[i] = (frequencies[i][0], frequencies[i][1] + 1)
                found = True
                break
        if not found:
            frequencies.append((char, 1))
    return frequencies

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
    build_min_heap(Q)

    # if node['label'] is None:
    #     label = f"'{node['left']['label']}{node['right']['label']}'"
    # else:
    #     label = f"'{node['label']}'"
    # print(f"Insert(Q, {label}:{node['freq']})")

def pop_from_queue(Q):
    n = len(Q)
    if n == 0:
        return None
    # root - najmniejszy element
    root = Q[0]
    if n > 1:
        Q[0] = Q.pop()
        heapify(Q, len(Q), 0)
    else:
        Q.pop(0)
    return root

def build_priority_queue(frequencies):
    Q = []
    # tworzenie węzłów
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

def generate_codes(node, current_code="", codes=None):
    if codes is None:
        codes = []

    # jeśli węzeł jest liściem - nie ma dzieci
    if node['left'] is None and node['right'] is None:
        if current_code:
            codes.append((node['label'], current_code))
        else:
            codes.append((node['label'], 0))
    else:
        # przechodzi rekurencyjnie przez lewe i prawe poddrzewo
        if node['left']:
            generate_codes(node['left'], current_code + '0', codes)
        if node['right']:
            generate_codes(node['right'], current_code + '1', codes)

    return dict(codes)

def encoding(text, codes):
    encoded = ""
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
    # stworzenie pustego korzenia
    root = {
        'label': None,
        'left': None,
        'right': None
    }

    for char, code in codes.items():
        current = root
        for bit in code:
            # idzie na lewo po drzewie
            if bit == '0':
                if current['left'] is None:
                    # stworzenie lewego dziecka
                    current['left'] = {
                        'label': None,
                        'left': None,
                        'right': None
                    }
                current = current['left']
            else:
                # idzie na prawo po drzewie
                if current['right'] is None:
                    # stworzenie prawego dziecka
                    current['right'] = {
                        'label': None,
                        'left': None,
                        'right': None
                    }
                # przejście do prawego dziecka
                current = current['right']
        current['label'] = char
    return root

def read_encoded_file(filename):
    # rb - otworzenie pliku w trybie binarnym
    with open(filename, 'rb') as f:
        # odczytanie nagłówka z kodami
        header_bytes = b""
        while not header_bytes.endswith(b"\n\n"):
            header_bytes += f.read(1)
        # dekoduje z postaci binarnej na tekst
        header_text = header_bytes.decode('utf-8').strip()
        # stworzenie słownika z kodami
        codes = {}
        for line in header_text.split():
            char, code = line.split(":")
            # znaki specjalne
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


        # odczytanie wypełnienia
        padding = f.read(1)[0]
        # odczytanie zakodowanego tekstu
        encoded_bytes = f.read()

        # formatuje bajty do ciągu 0 i 1 oraz łączy te ciągi
        encoded_bits = ''
        for byte in encoded_bytes:
            # zamiana bajtu na 8 bitów
            bits = format(byte, '08b')
            encoded_bits += bits

        # usunięcie wypełnienia
        if padding == 0:
            encoded_string = encoded_bits
        else:
            encoded_string = encoded_bits[:-padding]

        return codes, encoded_string

def save_encoded_file(filename, codes, encoded_text):
    output_filename = f"szyfr-{os.path.splitext(filename)[0]}.txt"

    # stworzenie nagłówka z kodami
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

    # obliczenie ile zer trzeba dodać na koniec pliku
    padding = 8 - (len(encoded_text) % 8)
    if padding == 8:
        padding = 0
    encoded_text += "0" * padding

    # zamiana ciągu 0 i 1 na bajty
    encoded_bytes = bytearray()
    for i in range(0, len(encoded_text), 8):
        # wycina 8 bitów
        byte = encoded_text[i:i + 8]
        # zamienia na liczbę i dodaje do tablicy
        encoded_bytes.append(int(byte, 2))

    # zapisanie do pliku
    try:
        with open(output_filename, 'wb') as f:
            # czytelny nagłówek
            f.write(header.encode('utf-8'))
            # informacja o wielkości wypełnienia
            f.write(bytes([padding]))
            # nieczytelna reszta - zakodowane dane
            f.write(encoded_bytes)
    except Exception as e:
        print(f"Nie udało się zapisać pliku {output_filename}. Błąd: {e}")
        return None

    return output_filename

def save_decoded_file(decoded_text, filename):
    output_filename = f"deszyfr-{os.path.splitext(filename)[0].replace('szyfr-', '')}.txt"

    try:
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write(decoded_text)
    except Exception as e:
        print(f"Nie udało się zapisać pliku {output_filename}. Błąd: {e}")
        return None

    return output_filename

def process_file(filename, mode):
    if mode == 'encrypt':
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                text = file.read()
        except Exception as e:
            print(f"Nie udało się otworzyć pliku {filename}. Błąd: {e}")
            return

        if len(text) == 0:
            print("Plik jest pusty")
            return

        frequencies = calculate_frequencies(text)
        queue = build_priority_queue(frequencies)
        root = build_tree(queue)
        codes = generate_codes(root)
        encoded_text = encoding(text, codes)
        output_filename = save_encoded_file(filename, codes, encoded_text)
        if output_filename is not None:
            print(f"Zapisano zaszyfrowany plik jako: {output_filename}")

    elif mode == 'decrypt':
        codes, encoded_text = read_encoded_file(filename)
        root = build_tree_from_codes(codes)
        decoded_text = decoding(encoded_text, root)
        output_filename = save_decoded_file(decoded_text, filename)
        if output_filename is not None:
            print(f"Zapisano odszyfrowany plik jako: {output_filename}")

while True:
    choice = input("Wybierz: szyfruj (s) / deszyfruj (d) / zakończ (z): ").strip().lower()
    if choice == 'z':
        break
    elif choice in ('s', 'd'):
        number_of_files = 0
        while number_of_files <= 0:
            user_input = input("Podaj liczbę plików: ")
            if user_input.isdigit():
                number_of_files = int(user_input)
                if number_of_files <= 0:
                    print("Liczba plików musi być większa od zera")
            else:
                print("Liczba plików musi być całkowita")

        for i in range(number_of_files):
            while True:
                filename = input(f"Podaj nazwę pliku {i+1}: ").strip()
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
