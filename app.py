from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

lista = []

# --- Algoritmos ---
def bubble_sort(lista):
    inicio_tempo = time.time()
    n = len(lista)
    for i in range(n):
        for j in range(0, n-i-1):
            if lista[j] > lista[j+1]:
                lista[j], lista[j+1] = lista[j+1], lista[j]
    fim_tempo = time.time()
    return lista, (fim_tempo - inicio_tempo)

def busca_linear(lista, valor):
    inicio_tempo = time.time()
    for i in range(len(lista)):
        if lista[i] == valor:
            fim_tempo = time.time()
            return i, (fim_tempo - inicio_tempo)
    fim_tempo = time.time()
    return -1, (fim_tempo - inicio_tempo)

def busca_binaria(lista, valor):
    inicio_tempo = time.time()
    inicio, fim = 0, len(lista)-1
    while inicio <= fim:
        meio = (inicio + fim) // 2
        if lista[meio] == valor:
            fim_tempo = time.time()
            return meio, (fim_tempo - inicio_tempo)
        elif lista[meio] < valor:
            inicio = meio + 1
        else:
            fim = meio - 1
    fim_tempo = time.time()
    return -1, (fim_tempo - inicio_tempo)

# --- Rotas ---
@app.route("/")
def home():
    return render_template("index.html")   # Flask procura dentro da pasta templates/

@app.route("/listar", methods=["GET"])
def listar():
    return jsonify(lista)

@app.route("/adicionar", methods=["POST"])
def adicionar():
    data = request.json
    item = data.get("item")
    if item:
        lista.append(item)
    return jsonify({"message": "Item adicionado", "lista": lista})

@app.route("/ordenar", methods=["POST"])
def ordenar():
    global lista
    lista, tempo_sort = bubble_sort(lista)
    return jsonify({"message": "Lista ordenada", "tempo": tempo_sort})

@app.route("/buscar", methods=["POST"])
def buscar():
    data = request.json
    item = data.get("item")

    # busca linear
    pos_linear, tempo_linear = busca_linear(lista, item)

    # busca binária
    lista_ordenada, _ = bubble_sort(lista.copy())
    pos_binaria, tempo_binaria = busca_binaria(lista_ordenada, item)

    return jsonify({
        "linear": {"pos": pos_linear, "tempo": tempo_linear},
        "binaria": {"pos": pos_binaria, "tempo": tempo_binaria}
    })

if __name__ == "__main__":
    app.run(debug=True)
