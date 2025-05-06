import numpy as np
from skimage import io, transform, color, filters, exposure
import matplotlib.pyplot as plt
import argparse


def apply_transformations(image, operations):
    """
    Aplica transformações sequenciais a uma imagem

    Args:
        image (ndarray): Imagem de entrada
        operations (list): Lista de operações a serem aplicadas

    Returns:
        ndarray: Imagem transformada
    """
    transformed = image.copy()

    for op in operations:
        if op["type"] == "resize":
            transformed = transform.resize(transformed, (op["height"], op["width"]))

        elif op["type"] == "rotate":
            transformed = transform.rotate(transformed, op["angle"])

        elif op["type"] == "flip":
            if op["direction"] == "horizontal":
                transformed = transformed[:, ::-1]
            else:
                transformed = transformed[::-1, :]

        elif op["type"] == "grayscale":
            transformed = color.rgb2gray(transformed)

        elif op["type"] == "blur":
            transformed = filters.gaussian(transformed, sigma=op["sigma"])

        elif op["type"] == "sharpen":
            transformed = filters.unsharp_mask(
                transformed, radius=op["radius"], amount=op["amount"]
            )

        elif op["type"] == "adjust_brightness":
            transformed = exposure.adjust_gamma(transformed, gamma=op["gamma"])

        elif op["type"] == "edge_detect":
            transformed = filters.sobel(transformed)

    return transformed


def main():
    parser = argparse.ArgumentParser(
        description="Transformação de imagens com scikit-image"
    )
    parser.add_argument("input", help="Caminho da imagem de entrada")
    parser.add_argument(
        "--output", "-o", help="Caminho para salvar a imagem transformada"
    )

    # Operações disponíveis
    parser.add_argument(
        "--resize",
        nargs=2,
        metavar=("WIDTH", "HEIGHT"),
        type=int,
        help="Redimensiona a imagem",
    )
    parser.add_argument("--rotate", type=float, help="Rotaciona a imagem (graus)")
    parser.add_argument(
        "--flip", choices=["horizontal", "vertical"], help="Inverte a imagem"
    )
    parser.add_argument(
        "--grayscale", action="store_true", help="Converte para escala de cinza"
    )
    parser.add_argument("--blur", type=float, help="Aplica desfoque gaussiano (sigma)")
    parser.add_argument(
        "--sharpen",
        nargs=2,
        metavar=("RADIUS", "AMOUNT"),
        type=float,
        help="Aplica sharpening",
    )
    parser.add_argument(
        "--brightness",
        type=float,
        dest="gamma",
        help="Ajusta brilho (gamma <1 clareia, >1 escurece)",
    )
    parser.add_argument("--edge-detect", action="store_true", help="Detecção de bordas")

    args = parser.parse_args()

    # Carrega a imagem
    try:
        image = io.imread(args.input)
    except Exception as e:
        print(f"Erro ao carregar imagem: {e}")
        return

    # Prepara lista de operações
    operations = []

    if args.resize:
        operations.append(
            {"type": "resize", "width": args.resize[0], "height": args.resize[1]}
        )
    if args.rotate:
        operations.append({"type": "rotate", "angle": args.rotate})
    if args.flip:
        operations.append({"type": "flip", "direction": args.flip})
    if args.grayscale:
        operations.append({"type": "grayscale"})
    if args.blur:
        operations.append({"type": "blur", "sigma": args.blur})
    if args.sharpen:
        operations.append(
            {"type": "sharpen", "radius": args.sharpen[0], "amount": args.sharpen[1]}
        )
    if args.gamma:
        operations.append({"type": "adjust_brightness", "gamma": args.gamma})
    if args.edge_detect:
        operations.append({"type": "edge_detect"})

    # Aplica transformações
    if operations:
        transformed = apply_transformations(image, operations)
    else:
        print("Nenhuma operação especificada. Use --help para ver as opções.")
        return

    # Exibe resultados
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(image)
    plt.title("Original")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(transformed)
    plt.title("Transformada")
    plt.axis("off")

    plt.tight_layout()

    # Salva se especificado
    if args.output:
        io.imsave(args.output, transformed)
        print(f"Imagem transformada salva em: {args.output}")

    plt.show()


if __name__ == "__main__":
    main()
