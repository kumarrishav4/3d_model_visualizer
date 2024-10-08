import streamlit as st
import plotly.graph_objects as go
import trimesh
import io

# Web App Title
st.title("3D STL File Viewer")

# Upload the STL file
uploaded_file = st.file_uploader("Upload an STL file", type="stl")

# Check if a file has been uploaded
if uploaded_file is not None:
    # Convert the uploaded file to a file-like object
    stl_data = uploaded_file.read()
    file_like_object = io.BytesIO(stl_data)
    
    # Load the mesh using trimesh
    mesh = trimesh.load_mesh(file_like_object, file_type='stl')
    st.write(f"Uploaded: {uploaded_file.name}")
    st.write(f"Mesh loaded with {len(mesh.vertices)} vertices and {len(mesh.faces)} faces")
    
    # Extract vertices and faces from the mesh
    x, y, z = mesh.vertices.T
    faces = mesh.faces

    # Create solid mesh (faces)
    solid_mesh = go.Mesh3d(x=x, y=y, z=z, i=faces[:, 0], j=faces[:, 1], k=faces[:, 2], color='lightblue', opacity=1, name="Faces")

    # Create edges for wireframe visualization (edges)
    edges = mesh.edges
    wireframe_x = []
    wireframe_y = []
    wireframe_z = []

    for edge in edges:
        wireframe_x.extend([mesh.vertices[edge[0]][0], mesh.vertices[edge[1]][0], None])  # None to break the line
        wireframe_y.extend([mesh.vertices[edge[0]][1], mesh.vertices[edge[1]][1], None])
        wireframe_z.extend([mesh.vertices[edge[0]][2], mesh.vertices[edge[1]][2], None])

    # Create wireframe mesh (edges)
    wireframe_mesh = go.Scatter3d(x=wireframe_x, y=wireframe_y, z=wireframe_z, mode='lines', line=dict(color='black', width=2), name="Edges")

    # Create a scatter plot for the vertices
    vertex_mesh = go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(color='red', size=3), name="Vertices")

    # Create semi-transparent face mesh for "Point View"
    face_with_opacity = go.Mesh3d(x=x, y=y, z=z, i=faces[:, 0], j=faces[:, 1], k=faces[:, 2], color='lightblue', opacity=0.5, name="Faces with 50% Opacity")

    # Create a figure with nothing shown initially
    fig = go.Figure()

    # Add traces for solid (faces), wireframe (edges), and vertices (initially hidden)
    fig.add_trace(solid_mesh)
    fig.add_trace(wireframe_mesh)
    fig.add_trace(vertex_mesh)
    fig.add_trace(face_with_opacity)

    # Set all traces as invisible by default
    solid_mesh.visible = False
    wireframe_mesh.visible = False
    vertex_mesh.visible = False
    face_with_opacity.visible = False

    # Add buttons to switch between views and toggle components (vertices, edges, faces)
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                showactive=True,
                buttons=[
                    dict(label="Show Faces",
                         method="update",
                         args=[{"visible": [True, False, False, False]},
                               {"title": "3D View - Show Faces"}]),

                    dict(label="Show Edges",
                         method="update",
                         args=[{"visible": [False, True, False, False]},
                               {"title": "3D View - Show Edges"}]),

                    dict(label="Show Vertices",
                         method="update",
                         args=[{"visible": [False, False, True, False]},
                               {"title": "3D View - Show Vertices"}]),

                    dict(label="Solid",
                         method="update",
                         args=[{"visible": [True, True, False, False]},
                               {"title": "3D View - Solid Mode (Faces + Edges)"}]),

                    dict(label="Wireframe",
                         method="update",
                         args=[{"visible": [False, True, True, False]},
                               {"title": "3D View - Wireframe Mode (Edges + Vertices)"}]),

                    dict(label="Point View",
                         method="update",
                         args=[{"visible": [False, False, True, True]},
                               {"title": "3D View - Point View (Faces with 50% Opacity + Vertices)"}])
                ],
            )
        ]
    )

    # Show the plot using Streamlit's Plotly component
    st.plotly_chart(fig)

else:
    st.write("Please upload an STL file.")
