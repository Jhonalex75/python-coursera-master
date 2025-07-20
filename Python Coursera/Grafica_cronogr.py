from proyecto_montaje_molino import crear_cronograma, plot_gantt

df = crear_cronograma()
plot_gantt(df, save_path="gantt_molino.png")
print("Gráfica Gantt guardada como gantt_molino.png")