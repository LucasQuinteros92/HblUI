from pathlib import Path


def getRootPath():
    full_path = Path(__file__).parent.resolve()
    path_parts = full_path.parts
    try:
        hbl3_index = path_parts.index('HblUI')
    except ValueError:
        raise Exception("El directorio 'HblUI' no se encuentra en la ruta.")
    new_path = Path(*path_parts[:hbl3_index + 1])
    return new_path.__str__()