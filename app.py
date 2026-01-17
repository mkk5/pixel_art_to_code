import streamlit as st
from PIL import Image


def generate_pixel_art_data(image):
    # Convert uploaded file to an image object
    img = Image.open(image).convert("RGB")
    pixels = list(img.getdata())
    width, height = img.size

    # 1. Extract unique colors
    unique_colors = sorted(list(set(pixels)))

    # 2. Build colors_map (Hex)
    colors_map = ['#{:02x}{:02x}{:02x}'.format(*color) for color in unique_colors]
    color_to_index = {color: str(i) for i, color in enumerate(unique_colors)}

    # Check for limit
    if len(unique_colors) > 10:
        return None, None, f"Error: Image has {len(unique_colors)} colors. Max allowed is 10 for this format."

    # 3. Build pic_map
    pic_map = []
    for y in range(height):
        row_string = ""
        for x in range(width):
            pixel = pixels[y * width + x]
            row_string += color_to_index[pixel]
        pic_map.append(row_string)

    return colors_map, pic_map, None


# --- UI Layout ---
st.title("Pixel Art to Python Converter")
st.write("Upload a pixel art image to generate the data structure.")

uploaded_file = st.file_uploader("Choose a PNG or JPG file", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    colors, picture, error = generate_pixel_art_data(uploaded_file)

    if error:
        st.error(error)
    else:
        st.success("Done! Copy your code below:")

        # Format the output string
        output_code = "colors_map = [\n" + ", ".join([f'"{c}"' for c in colors]) + "\n]\n\n"
        output_code += "pic_map = [\n"
        for row in picture:
            output_code += f'    "{row}",\n'
        output_code += "]"

        # Display as copyable code block
        st.code(output_code, language='python')
