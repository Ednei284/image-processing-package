import numpy as np
from skimage import io, transform
from skimage.util import montage
import matplotlib.pyplot as plt
import argparse


def combine_images(image_paths, output_path=None):
    """
    Combina múltiplas imagens em uma grade e exibe/salva o resultado

    Args:
        image_paths (list): Lista de caminhos para as imagens
        output_path (str): Caminho para salvar a imagem combinada (opcional)
    """
    try:
        # Carrega todas as imagens
        images = [io.imread(img_path) for img_path in image_paths]

        # Verifica se todas as imagens têm as mesmas dimensões
        shapes = np.array([img.shape for img in images])
        if not np.all(shapes == shapes[0]):
            print("Redimensionando imagens para o menor tamanho...")
            min_shape = np.min(shapes, axis=0)
            images = [transform.resize(img, min_shape) for img in images]

        # Cria uma montagem com 2 linhas (ajuste conforme necessidade)
        combined = montage(np.array(images), grid_shape=(2, len(images) // 2))

        # Exibe o resultado
        plt.figure(figsize=(10, 10))
        plt.imshow(combined)
        plt.axis("off")
        plt.title(f"Combinação de {len(images)} imagens")

        # Salva se um caminho for fornecido
        if output_path:
            io.imsave(output_path, combined)
            print(f"Imagem salva em: {output_path}")

        plt.show()

    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Combina múltiplas imagens em uma grade"
    )
    parser.add_argument("images", nargs="+", help="Caminhos das imagens de entrada")
    parser.add_argument("--output", "-o", help="Caminho para salvar a imagem combinada")

    args = parser.parse_args()

    combine_images(args.images, args.output)
