import cv2
import numpy as np
import os

def extract_patches(image_path, output_dir, patch_size=1024, stride=100):
    # Crear el directorio de salida si no existe
    os.makedirs(output_dir, exist_ok=True)

    # Leer la imagen con OpenCV
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    if img is None:
        raise ValueError(f"No se pudo cargar la imagen: {image_path}")

    # Obtener dimensiones de la imagen
    height, width = img.shape[:2]
    print(f"Dimensiones de la imagen: {img.shape}")

    # Contador para nombrar las imágenes
    counter = 0

    # Iterar sobre la imagen con la ventana deslizante
    for y in range(0, height - patch_size + 1, stride):
        for x in range(0, width - patch_size + 1, stride):
            # Extraer el parche
            patch = img[y:y + patch_size, x:x + patch_size]

            # Guardar el parche
            output_path = os.path.join(output_dir, f'patch_{counter:04d}.png')
            cv2.imwrite(output_path, patch)

            counter += 1

            if counter % 100 == 0:
                print(f"Procesados {counter} patches...")

    return counter

def process_all_images(nir_path, rgb_path, mask_path, patch_size=1024, stride=100):
    # Directorios de salida
    output_dirs = {
        'nir': 'patches_NIR',
        'rgb': 'patches_RGB',
        'mask': 'patches_mask'
    }

    # Procesar cada imagen
    image_paths = {
        'nir': nir_path,
        'rgb': rgb_path,
        'mask': mask_path
    }

    results = {}

    for img_type, path in image_paths.items():
        print(f"\nProcesando imagen {img_type.upper()}...")
        try:
            patches_count = extract_patches(
                path,
                output_dirs[img_type],
                patch_size,
                stride
            )
            results[img_type] = patches_count
            print(f"Completado {img_type.upper()}: {patches_count} patches generados")
        except Exception as e:
            print(f"Error procesando {img_type}: {str(e)}")
            results[img_type] = 0

    return results

# Ejemplo de uso
if __name__ == "__main__":    
    # Rutas de las imágenes de entrada
    nir_path = 'C:/Respaldo/Henry/Proyecto Camuflaje/Datasets/WeedBanana/RGB-NIR/NIR.png'
    rgb_path = 'C:/Respaldo/Henry/Proyecto Camuflaje/Datasets/WeedBanana/RGB-NIR/RGB.png'
    mask_path = 'C:/Respaldo/Henry/Proyecto Camuflaje/Datasets/WeedBanana/RGB-NIR/mask.png'


    # Parámetros
    patch_size = 1024
    stride = 300

    # Procesar todas las imágenes
    results = process_all_images(
        nir_path,
        rgb_path,
        mask_path,
        patch_size,
        stride
    )

    # Mostrar resumen final
    print("\nResumen del proceso:")
    print(f"Patches NIR generados: {results['nir']}")
    print(f"Patches RGB generados: {results['rgb']}")
    print(f"Patches máscara generados: {results['mask']}")

    # Created/Modified files during execution:
    print("\nDirectorios creados:")
    print("- patches_NIR/")
    print("- patches_RGB/")
    print("- patches_mask/")
    print("\nArchivos generados (por cada directorio):")
    print("patch_0000.tif hasta patch_XXXX.tif")
