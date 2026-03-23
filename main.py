import sys
def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <makespan>")
        return

    makespan_objetivo = int(sys.argv[1])
    print("Makespan objetivo:", makespan_objetivo)

    tareas= leer_tareas()
    recursos= leer_recursos()
    cronograma= planificar(tareas, recursos)
    escribir_output(cronograma)
    makespan_real=calcular_makespan(cronograma)
    print("Makespan obtenido:", makespan_real)

    if makespan_real <= makespan_objetivo:
        print("Cumple el makespan objetivo")
    else:
        print("No cumple el makespan objetivo")
    print("\nCronograma:")
    for t in cronograma:
        print(t)
    print("\nCronograma generado en output.txt")
   


def leer_tareas():
    tareas = []
    with open("tareas_EP.txt") as f:
        for line in f:
            id_t,dur,cat = line.strip().split(",")
            tareas.append({
                "id":id_t,
                "duracion":int(dur),
                "categoria":cat })
    return tareas

def leer_recursos():
    recursos=[]
    with open("recursos_EP.txt") as f:
        for line in f:
            partes = line.strip().split(",")
            id_r = partes[0]
            categorias = partes[1:]
            recursos.append({
                "id": id_r,
                "categorias": categorias,
                "tiempo_disponible": 0})
    return recursos   
        
def planificar(tareas, recursos):
    tareas.sort(key=lambda x: -x["duracion"])
    cronograma = []
    for tarea in tareas:
        compatibles = [
            r for r in recursos
            if tarea["categoria"] in r["categorias"]
        ]
        if not compatibles:
            raise Exception(f"No hay recurso compatible para {tarea['id']}")
        recurso = min(compatibles, key=lambda r: r["tiempo_disponible"])
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


if __name__ == "__main__": main() 
