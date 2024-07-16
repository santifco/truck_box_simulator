import streamlit as st
import plotly.graph_objects as go




with st.expander("Caja del vehículo", expanded=True):
    large_rect_width = st.number_input("Ancho del rectángulo grande (mm)", value=2300)
    large_rect_height = st.number_input("Profundidad del rectángulo grande (mm)", value=5400)
    altura = st.number_input("Altura del rectángulo grande (mm)", value=2100)

with st.expander("Unidad Contenedora", expanded=True):
    # Crear entradas para las dimensiones de los rectángulos pequeños
    small_rect_width = st.number_input("Ancho del rectángulo pequeño (mm)", value=1000)
    small_rect_height = st.number_input("Profundidad del rectángulo pequeño (mm)", value=1200)
    altura_small_rect = st.number_input("Altura del rectángulo pequeño (mm)", value=1600)

# Calcular cuántos rectángulos pequeños caben en el rectángulo grande
num_small_rects_x = large_rect_width // small_rect_width
num_small_rects_y = large_rect_height // small_rect_height
num_small_rects_z = altura // altura_small_rect
total_small_rects = num_small_rects_x * num_small_rects_y * num_small_rects_z

# Crear el objeto de la figura en 3D
fig = go.Figure()

# Coordenadas de los vértices de la caja
x = [0, large_rect_width, large_rect_width, 0, 0, large_rect_width, large_rect_width, 0]
y = [0, 0, large_rect_height, large_rect_height, 0, 0, large_rect_height, large_rect_height]
z = [0, 0, 0, 0, altura, altura, altura, altura]

# Definir las líneas que forman los bordes de la caja
edges = [
    [0, 1], [1, 2], [2, 3], [3, 0],  # Base inferior
    [4, 5], [5, 6], [6, 7], [7, 4],  # Base superior
    [0, 4], [1, 5], [2, 6], [3, 7]   # Verticales
]

# Añadir las líneas al gráfico
for edge in edges:
    fig.add_trace(go.Scatter3d(
        x=[x[edge[0]], x[edge[1]]],
        y=[y[edge[0]], y[edge[1]]],
        z=[z[edge[0]], z[edge[1]]],
        mode='lines',
        line=dict(color='blue', width=5)
    ))

# Añadir los rectángulos pequeños dentro de la caja
for i in range(num_small_rects_x):
    for j in range(num_small_rects_y):
        for k in range(num_small_rects_z):
            x0 = i * small_rect_width
            y0 = j * small_rect_height
            z0 = k * altura_small_rect
            x1 = x0 + small_rect_width
            y1 = y0 + small_rect_height
            z1 = z0 + altura_small_rect

            # Coordenadas de los vértices del rectángulo pequeño
            small_x = [x0, x1, x1, x0, x0, x1, x1, x0]
            small_y = [y0, y0, y1, y1, y0, y0, y1, y1]
            small_z = [z0, z0, z0, z0, z1, z1, z1, z1]

            # Definir las líneas que forman los bordes del rectángulo pequeño
            small_edges = [
                [0, 1], [1, 2], [2, 3], [3, 0],  # Base inferior
                [4, 5], [5, 6], [6, 7], [7, 4],  # Base superior
                [0, 4], [1, 5], [2, 6], [3, 7]   # Verticales
            ]

            # Añadir las líneas del rectángulo pequeño al gráfico
            for edge in small_edges:
                fig.add_trace(go.Scatter3d(
                    x=[small_x[edge[0]], small_x[edge[1]]],
                    y=[small_y[edge[0]], small_y[edge[1]]],
                    z=[small_z[edge[0]], small_z[edge[1]]],
                    mode='lines',
                    line=dict(color='lightseagreen', width=2)
                ))

# Añadir la anotación de la cantidad de rectángulos pequeños que caben
fig.add_trace(go.Scatter3d(
    x=[large_rect_width / 2],
    y=[large_rect_height / 2],
    z=[altura + 200],
    mode='text',
    text=[f"Cantidad de rectángulos pequeños: {total_small_rects}"],
    textposition='middle center',
    showlegend=False
))

# Ajustar el layout
fig.update_layout(
    scene=dict(
        xaxis_title='Ancho (mm)',
        yaxis_title='Profundidad (mm)',
        zaxis_title='Altura (mm)',
        aspectratio=dict(x=large_rect_width/altura, y=large_rect_height/altura, z=altura/altura)
    ),
    margin=dict(l=0, r=0, t=0, b=0)
)

# Mostrar la figura con Streamlit
st.plotly_chart(fig)


# Mostrar el número total de rectángulos pequeños
st.write(f"Total de rectángulos pequeños que caben: {total_small_rects}")
st.write(f"Volumen del contenedor (pallet): {(small_rect_width*small_rect_height*altura_small_rect)*1e-9:.2f} m3")
st.write(f"Volumen total de la caja (m3): {(large_rect_width*large_rect_height*altura)*1e-9:.2f}")
st.write(f"Volumen total utilizado (m3): {(altura_small_rect*small_rect_width*small_rect_height*total_small_rects)*1e-9:.2f}")
st.write(f"Volumen en altura vacante (m3): {((altura-altura_small_rect)*small_rect_width*small_rect_height*total_small_rects)*1e-9:.2f}")
st.write(f"Volumen en piso vacante (m3): {round((((large_rect_width*large_rect_height)-(small_rect_width*small_rect_height*total_small_rects)))*altura*1e-9,2):.2f}")
