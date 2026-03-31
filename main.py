import sys
import random
import time
def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <makespan>")
        return
    makespan_objetivo = int(sys.argv[1])
    print("Makespan objetivo:", makespan_objetivo)


    tareas = leer_tareas("tareas.txt")
    recursos = leer_recursos("recursos.txt")
    inicio=time.time()

    cronograma = planificar(tareas, recursos)
    fin=time.time()

   
    escribir_output(cronograma)

    makespan_real = calcular_makespan(cronograma)
    print("Makespan obtenido:", makespan_real)
    print("Tiempo de ejecución:", round(fin - inicio, 2), "segundos")

    if makespan_real <= makespan_objetivo:
        print("Cumple el makespan objetivo")
    else:
        print("No cumple el makespan objetivo")

    print("\nPrimeras 10 tareas del cronograma:")
    for t in cronograma[:10]:
        print(t)

    print("\nCronograma generado en output.txt")



# LECTURA

def leer_tareas(path):
    tareas = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            partes = [x.strip() for x in line.split(",")]

            if len(partes) != 3:
                continue

            tareas.append({
                "id": partes[0],
                "duracion": int(partes[1]),
                "categoria": partes[2]
            })
    return tareas


def leer_recursos(path):
    recursos = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            partes = [x.strip() for x in line.split(",")]

            if len(partes) < 2:
                continue

            recursos.append({
                "id": partes[0],
                "categorias": partes[1:],
                "tiempo_disponible": 0
            })
    return recursos



# OPTIMIZACIÓN 

def crear_mapa_recursos(recursos):
    mapa = {}
    for r in recursos:
        for cat in r["categorias"]:
            if cat not in mapa:
                mapa[cat] = []
            mapa[cat].append(r)
    return mapa



# PLANIFICACIÓN
def planificar(tareas, recursos):
    # mapa rápido
    mapa = crear_mapa_recursos(recursos)

    # precálculo compatibilidad
    compat_count = {
        t["id"]: len(mapa.get(t["categoria"], []))
        for t in tareas
    }

    # ordenar una sola vez
    tareas_ordenadas = sorted(
        tareas,
        key=lambda x: (
            compat_count[x["id"]],
            -x["duracion"]
        )
    )

    # copiar recursos
    recursos_copia = [
        {"id": r["id"], "categorias": r["categorias"], "tiempo_disponible": 0}
        for r in recursos
    ]

    mapa = crear_mapa_recursos(recursos_copia)

    cronograma = []

    for tarea in tareas_ordenadas:
        if tarea["categoria"] not in mapa:
            raise Exception(f"No hay recurso compatible para {tarea['id']}")

        compatibles = mapa[tarea["categoria"]]

        recurso = min(
            compatibles,
            key=lambda r: r["tiempo_disponible"]
        )

        inicio = recurso["tiempo_disponible"]
        fin = inicio + tarea["duracion"]

        cronograma.append((tarea["id"], recurso["id"], inicio, fin))

        recurso["tiempo_disponible"] = fin

    return cronograma



def calcular_makespan(cronograma):
    return max(fin for _, _, _, fin in cronograma)


def cantidad_recursos_compatibles(tarea, recursos):
    return sum(1 for r in recursos if tarea["categoria"] in r["categorias"])


def escribir_output(cronograma):
    with open("output.txt", "w") as f:
        for t in cronograma:
            f.write(f"{t[0]},{t[1]},{t[2]},{t[3]}\n")


if __name__ == "__main__":
    main()