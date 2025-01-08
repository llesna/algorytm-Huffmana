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

def min_heapify(A, n, i):
    smallest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and A[l]['freq'] < A[smallest]['freq']:
        smallest = l

    if r < n and A[r]['freq'] < A[smallest]['freq']:
        smallest = r

    if smallest != i:
        A[i], A[smallest] = A[smallest], A[i]
        min_heapify(A, n, smallest)

def build_min_heap(A):
    n = len(A)
    for i in range(n // 2 - 1, -1, -1):
        min_heapify(A, n, i)

def insert_into_queue(Q, node):
    # dodanie na koniec kolejki
    Q.append(node)
    # naprawienie kolejki
    build_min_heap(Q)

    # if node['label'] is None:
    #     label = f"'{node['left']['label']}{node['right']['label']}'"
    # else:
    #     label = f"'{node['label']}'"
    # print(f"Insert(Q, {label}:{node['freq']})")

def delete_from_queue(Q):
    n = len(Q)
    # jeśli kopiec jest pusty
    if n == 0:
        return None
    # root - najmniejszy element
    root = Q[0]
    if n > 1:
        # zamienia pierwszy z ostatnim elementem
        Q[0] = Q.pop()
        # naprawia kopiec
        min_heapify(Q, len(Q), 0)
    else:
        Q.pop(0)
    return root

def build_priority_queue(frequencies):
    Q = []
    # tworzenie węzłów
    for char, frequency in frequencies:
        Q.append({
            # etykieta
            'label': char,
            'freq': frequency,
            'left': None,
            'right': None
        })
    build_min_heap(Q)
    return Q

# wyświetlanie kolejki w mniej więcej takim formacie jak na wykładzie
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

        # pobranie węzła o najmniejszej liczbie wystąpień (częstości)
        x = delete_from_queue(Q)

        # print(f"z.left = '{node1['label']}':{node1['freq']}")
        # print_queue(Q)

        # pobranie kolejnego węzła o najmn. licz. wystąpień
        y = delete_from_queue(Q)

        # print(f"z.right = '{node2['label']}':{node2['freq']}")
        # print_queue(Q)

        # połączenie tych węzłów
        new_node = {
            'label': f"{x['label']}{y['label']}",
            'freq': x['freq'] + y['freq'],
            'left': x,
            'right': y
        }

        insert_into_queue(Q, new_node)
        # print()

    # zwraca korzeń
    return Q[0]

# generowanie kodów Huffmana
# codes - pary: (znak, kod Huffmana)
def generate_codes(node, current_code, codes):
    # jeśli węzeł jest liściem
    if node['left'] is None and node['right'] is None:
        # current_code - kod tworzony podczas przechodzenia od korzenia do węzła
        if current_code:
            codes.append((node['label'], current_code))
        else:
            # drzewo z jednym węzłem
            codes.append((node['label'], 0))
    else:
        # przechodzi rekurencyjnie przez lewe i prawe poddrzewo
        if node['left']:
            generate_codes(node['left'], current_code + '0', codes)
        if node['right']:
            generate_codes(node['right'], current_code + '1', codes)

    return dict(codes)

# koduje tekst na podstawie kodów Huffmana
def encoding(text, codes):
    encoded = ""
    for char in text:
        encoded += codes[char]
    # zwraca ciąg zer i jedynek
    return encoded

# dekoduje na podstawie drzewa
def decoding(encoded_text, root):
    decoded = ""
    current_node = root

    for bit in encoded_text:
        if bit == '0':
            # przechodzi do lewego dziecka
            current_node = current_node['left']
        else:
            # przechodzi do prawego dziecka
            current_node = current_node['right']

        # dotarcie do liścia
        if current_node['left'] is None and current_node['right'] is None:
            # zapisuje znak
            decoded += current_node['label']
            # wraca do korzenia
            current_node = root

    return decoded

# zbudowanie drzewa na podstawie kodów Huffmana
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
                # przejście do lewego dziecka
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
        # ustawienie label w liściu na odpowiedni znak
        current['label'] = char
    return root

def read_encoded_file(filename):
    # otworzenie pliku w trybie binarnym
    encoded_file = open(filename, 'rb')

    # odczytanie nagłówka z kodami
    header_bytes = b""
    while not header_bytes.endswith(b"\n\n"):
        header_bytes += encoded_file.read(1)
    # dekoduje z postaci binarnej na tekst
    header_text = header_bytes.decode('utf-8').strip()

    # stworzenie słownika z kodami
    codes = {}
    for line in header_text.split():
        char, code = line.split(":")
        # zamienia reprezentację znaku na rzeczywisty znak
        if char == "\\s":
            char = ' '
        else:
            char = eval("'" + char + "'")
        codes[char] = code

    # odczytanie ile dodatkowych zer dodano na końcu zakodowanego tekstu
    extra_zeros = encoded_file.read(1)[0]
    # odczytanie zakodowanego tekstu
    encoded_bytes = encoded_file.read()

    # formatuje bajty do ciągu 0 i 1 oraz łączy te ciągi
    encoded_bits = ''
    for byte in encoded_bytes:
        # zamiana bajtu na 8 bitowy ciąg binarny
        bits = format(byte, '08b')
        encoded_bits += bits

    # usunięcie dodatkowych zer
    if extra_zeros == 0:
        encoded_string = encoded_bits
    else:
        encoded_string = encoded_bits[:-extra_zeros]

    return codes, encoded_string

def save_encoded_file(filename, codes, encoded_text):
    output_filename = f"szyfr-{filename}"

    # stworzenie nagłówka z kodami
    header = ""
    for char, code in codes.items():
        if char == ' ':
            char = "\\s"
        else:
            char = repr(char)[1:-1]
        header += f"{char}:{code} "
    header += "\n\n"

    # obliczenie ile zer trzeba dodać na koniec pliku do wyrównania do pełnych bajtów
    extra_zeros = 8 - (len(encoded_text) % 8)
    if extra_zeros == 8:
        extra_zeros = 0
    encoded_text += "0" * extra_zeros

    # zamiana ciągu 0 i 1 na tablicę bajtów
    encoded_bytes = bytearray()
    for i in range(0, len(encoded_text), 8):
        # wycina 8 bitów
        byte = encoded_text[i:i + 8]
        # zamienia na liczbę całkowitą i dodaje do tablicy
        encoded_bytes.append(int(byte, 2))

    # zapisanie do pliku
    try:
        file = open(output_filename, 'wb')
        # nagłowek zakodowany w utf-8, aby przy dekodowaniu były poprawne polskie znaki
        file.write(header.encode('utf-8'))
        # zapisanie liczby dodatkowych zer
        file.write(bytes([extra_zeros]))
        # nieczytelna reszta - zakodowane dane
        file.write(encoded_bytes)
        file.close()
    except Exception as e:
        print(f"Nie udało się zapisać pliku {output_filename}. Błąd: {e}")
        return None

    return output_filename

def save_decoded_file(decoded_text, filename):
    # zamiana "szyfr-" na początku pliku na "deszyfr-"
    output_filename = f"de{filename}"
    # zamiana \n na \r\n windowsowe lub \n linuxowe
    decoded_text = decoded_text.replace("\n", os.linesep)

    try:
        file = open(output_filename, 'w', encoding='utf-8')
        file.write(decoded_text)
        file.close()
    except Exception as e:
        print(f"Nie udało się zapisać pliku {output_filename}. Błąd: {e}")
        return None

    return output_filename

def process_file(filename, mode):
    # szyfrowanie
    if mode == 'encrypt':
        try:
            # musi otwierać w utf-8 przez polskie znaki
            file = open(filename, 'r', encoding='utf-8')
            text = file.read()
            # zamiana windowsowego \r\n na linuxowe \n
            text = text.replace("\r\n", "\n")
            file.close()
        except Exception as e:
            print(f"Nie udało się otworzyć pliku {filename}. Błąd: {e}")
            return

        frequencies = calculate_frequencies(text)
        queue = build_priority_queue(frequencies)
        root = build_tree(queue)
        codes = []
        codes = generate_codes(root, "", codes)
        encoded_text = encoding(text, codes)
        output_filename = save_encoded_file(filename, codes, encoded_text)
        if output_filename is not None:
            print(f"Zapisano zaszyfrowany plik jako: {output_filename}")

    # deszyfrowanie
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
