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

    if node['label'] is None:
        label = f"'{node['left']['label']}{node['right']['label']}'"
    else:
        label = f"'{node['label']}'"
    print(f"Insert(Q, {label}:{node['freq']})")

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
        print_queue(Q)
        node1 = pop_from_queue(Q)
        print(f"z.left = '{node1['label']}':{node1['freq']}")
        print_queue(Q)
        node2 = pop_from_queue(Q)
        print(f"z.right = '{node2['label']}':{node2['freq']}")
        print_queue(Q)

        new_node = {
            'label': f"{node1['label']}{node2['label']}",
            'freq': node1['freq'] + node2['freq'],
            'left': node1,
            'right': node2
        }

        insert_into_queue(Q, new_node)
        print()

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
    wynik = ""
    codes = dict(codes)
    for char in text:
        wynik += codes[char]
    return wynik

def decoding(encoded_text, tree):
    wynik = ""
    current_node = tree

    for bit in encoded_text:
        if bit == '0':
            current_node = current_node['left']
        else:
            current_node = current_node['right']

        # dotarliśmy do liścia, zapisujemy znak i wracamy do korzenia
        if current_node['left'] is None and current_node['right'] is None:
            wynik += current_node['label']
            current_node = tree

    return wynik

text = "KEBAB BARBARY"
print("text:", text)

frequencies = calculate_frequencies(text)
print("frequencies:", frequencies)
print()

queue = build_priority_queue(frequencies)
tree = build_tree(queue)

codes = generate_codes(tree)
print("generated codes:", codes)

encoded_text = encoding(text, codes)
print("\nencoded text:", encoded_text)

decoded_text = decoding(encoded_text, tree)
print("decoded text:", decoded_text)
