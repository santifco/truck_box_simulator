import streamlit as st
import plotly.graph_objects as go

# Expander for the vehicle box
with st.expander("Caja del vehículo", expanded=True):
    large_rect_width = st.number_input("Ancho del rectángulo grande (mm)", value=2300)
    large_rect_height = st.number_input("Profundidad del rectángulo grande (mm)", value=5400)
    altura = st.number_input("Altura del rectángulo grande (mm)", value=2100)

# Expander for the first container unit
with st.expander("Unidad Contenedora 1", expanded=True):
    small_rect_width_1 = st.number_input("Ancho del rectángulo pequeño 1 (mm)", value=1000)
    small_rect_height_1 = st.number_input("Profundidad del rectángulo pequeño 1 (mm)", value=1200)
    altura_small_rect_1 = st.number_input("Altura del rectángulo pequeño 1 (mm)", value=1600)

# Expander for the second container unit
with st.expander("Unidad Contenedora 2", expanded=True):
    small_rect_width_2 = st.number_input("Ancho del rectángulo pequeño 2 (mm)", value=800)
    small_rect_height_2 = st.number_input("Profundidad del rectángulo pequeño 2 (mm)", value=1000)
    altura_small_rect_2 = st.number_input("Altura del rectángulo pequeño 2 (mm)", value=1400)

# Expander for the percentage of container units
with st.expander("Porcentaje de Unidades Contenedoras", expanded=True):
    porcentaje_1 = st.slider("Porcentaje de Unidad Contenedora 1 (%)", 0, 100, 50)
    porcentaje_2 = 100 - porcentaje_1

# Calculate total number of small rectangles
total_volume = large_rect_width * large_rect_height * altura
volume_1 = small_rect_width_1 * small_rect_height_1 * altura_small_rect_1
volume_2 = small_rect_width_2 * small_rect_height_2 * altura_small_rect_2

# Effective volumes
volume_1_effective = total_volume * (porcentaje_1 / 100)
volume_2_effective = total_volume * (porcentaje_2 / 100)

# Calculate the maximum number of containers based on volume and percentage
total_small_rects_1_effective = int(volume_1_effective // volume_1)
total_small_rects_2_effective = int(volume_2_effective // volume_2)

# Create the 3D figure
fig = go.Figure()

# Coordinates of the vertices of the large box
x = [0, large_rect_width, large_rect_width, 0, 0, large_rect_width, large_rect_width, 0]
y = [0, 0, large_rect_height, large_rect_height, 0, 0, large_rect_height, large_rect_height]
z = [0, 0, 0, 0, altura, altura, altura, altura]

# Define the edges of the large box
edges = [
    [0, 1], [1, 2], [2, 3], [3, 0],  # Bottom base
    [4, 5], [5, 6], [6, 7], [7, 4],  # Top base
    [0, 4], [1, 5], [2, 6], [3, 7]   # Verticals
]

# Add the edges of the large box to the plot
for edge in edges:
    fig.add_trace(go.Scatter3d(
        x=[x[edge[0]], x[edge[1]]],
        y=[y[edge[0]], y[edge[1]]],
        z=[z[edge[0]], z[edge[1]]],
        mode='lines',
        line=dict(color='blue', width=5)
    ))

# Function to add small rectangles to the plot
def add_small_rects(fig, num_rects, width, height, rect_height, color, start_index):
    count = 0
    for k in range(int(altura // rect_height)):
        for j in range(int(large_rect_height // height)):
            for i in range(int(large_rect_width // width)):
                if count >= num_rects:
                    return count
                x0 = i * width
                y0 = j * height
                z0 = k * rect_height
                x1 = x0 + width
                y1 = y0 + height
                z1 = z0 + rect_height

                # Ensure the rectangle fits within the large container
                if x1 > large_rect_width or y1 > large_rect_height or z1 > altura:
                    continue

                # Coordinates of the vertices of the small rectangle
                small_x = [x0, x1, x1, x0, x0, x1, x1, x0]
                small_y = [y0, y0, y1, y1, y0, y0, y1, y1]
                small_z = [z0, z0, z0, z0, z1, z1, z1, z1]

                # Define the edges of the small rectangle
                small_edges = [
                    [0, 1], [1, 2], [2, 3], [3, 0],  # Bottom base
                    [4, 5], [5, 6], [6, 7], [7, 4],  # Top base
                    [0, 4], [1, 5], [2, 6], [3, 7]   # Verticals
                ]

                # Add the edges of the small rectangle to the plot
                for edge in small_edges:
                    fig.add_trace(go.Scatter3d(
                        x=[small_x[edge[0]], small_x[edge[1]]],
                        y=[small_y[edge[0]], small_y[edge[1]]],
                        z=[small_z[edge[0]], small_z[edge[1]]],
                        mode='lines',
                        line=dict(color=color, width=2)
                    ))
                count += 1
    return count

# Add small rectangles of Unidad Contenedora 1
num_added_1 = add_small_rects(fig, total_small_rects_1_effective, small_rect_width_1, small_rect_height_1, altura_small_rect_1, 'lightseagreen', 0)

# Add small rectangles of Unidad Contenedora 2
num_added_2 = add_small_rects(fig, total_small_rects_2_effective, small_rect_width_2, small_rect_height_2, altura_small_rect_2, 'lightcoral', 0)

# Add annotation for the number of small rectangles that fit inside the large box
fig.add_trace(go.Scatter3d(
    x=[large_rect_width / 2],
    y=[large_rect_height / 2],
    z=[altura + 200],
    mode='text',
    text=[f"Total de Unidad Contenedora 1: {num_added_1}<br>Total de Unidad Contenedora 2: {num_added_2}"],
    textposition='middle center',
    showlegend=False
))

# Adjust the layout
fig.update_layout(
    scene=dict(
        xaxis_title='Ancho (mm)',
        yaxis_title='Profundidad (mm)',
        zaxis_title='Altura (mm)',
        aspectratio=dict(x=large_rect_width/altura, y=large_rect_height/altura, z=altura/altura)
    ),
    margin=dict(l=0, r=0, t=0, b=0)
)

# Display the figure with Streamlit
st.plotly_chart(fig)

# Display the calculated information
st.write(f"Total de rectángulos pequeños que caben: {num_added_1 + num_added_2}")
st.write(f"Volumen del contenedor (pallet) 1: {(small_rect_width_1 * small_rect_height_1 * altura_small_rect_1) * 1e-9:.2f} m³")
st.write(f"Volumen del contenedor (pallet) 2: {(small_rect_width_2 * small_rect_height_2 * altura_small_rect_2) * 1e-9:.2f} m³")
st.write(f"Volumen total de la caja: {(large_rect_width * large_rect_height * altura) * 1e-9:.2f} m³")
st.write(f"Volumen total utilizado por contenedor 1: {(altura_small_rect_1 * small_rect_width_1 * small_rect_height_1 * num_added_1) * 1e-9:.2f} m³")
st.write(f"Volumen total utilizado por contenedor 2: {(altura_small_rect_2 * small_rect_width_2 * small_rect_height_2 * num_added_2) * 1e-9:.2f} m³")
st.write(f"Volumen en altura vacante (m³): {((altura - altura_small_rect_1) * small_rect_width_1 * small_rect_height_1 * num_added_1 + (altura - altura_small_rect_2) * small_rect_width_2 * small_rect_height_2 * num_added_2) * 1e-9:.2f}")
st.write(f"Volumen en piso vacante (m³): {((large_rect_width * large_rect_height) - ((small_rect_width_1 * small_rect_height_1 * num_added_1) + (small_rect_width_2 * small_rect_height_2 * num_added_2))) * altura * 1e-9:.2f}")
