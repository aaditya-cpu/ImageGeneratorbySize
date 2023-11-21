import io

import numpy as np
from PIL import Image


def generate_dummy_image(file_size_mb, filename="dummy_image.jpg"):
        file_size = file_size_mb * 1024 * 1024
        target_size_tolerance = 1024  # Tolerance of 1 KB

        # Estimate initial dimensions based on a rough file size to pixel ratio
        # This ratio can be adjusted based on empirical observations
        ratio = 0.0005  # This is an estimated ratio and might need adjustment
        initial_dimension = int((file_size * ratio)**0.5)
        width, height = initial_dimension, initial_dimension

        max_iterations = 100
        iterations = 0

        while iterations < max_iterations:
                img_array = random_noise_array(width, height)
                img = Image.fromarray(img_array, 'RGB')

                img_bytes = io.BytesIO()
                quality = 85  # Start with a default quality
                img.save(img_bytes, format='JPEG', quality=quality)
                img_size = img_bytes.tell()

                if abs(img_size - file_size) <= target_size_tolerance:
                        break

                # Adjust dimensions based on the difference between current and target size
                size_diff_ratio = (file_size - img_size) / file_size
                adjustment_factor = 1 + (size_diff_ratio / 2
                                         )  # Adjust this factor as needed
                width, height = int(width * adjustment_factor), int(
                    height * adjustment_factor)

                iterations += 1

        img.save(filename)
        return filename


def random_noise_array(width, height):
        return (np.random.rand(height, width, 3) * 255).astype(np.uint8)


# Example usage
try:
        filename = generate_dummy_image(
            4.00)  # Specify desired file size in MB
        print(f"Generated image saved as {filename}")
except ValueError as e:
        print(f"Error: {e}")
