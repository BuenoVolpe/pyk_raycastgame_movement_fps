from engine.utils.json import json_reader


class ColorMapLoader:
    """
    Loads palette swap maps from a PNG + JSON definition.

    PNG rows represent different palettes.
    JSON provides palette names.
    """
    def __init__(self, image_loader):
        self.image_loader = image_loader

    def load(self, png_path: str, json_path: str) -> dict:
        """
        Loads all palettes from a color map image.
        """
        # Load the PNG palette texture
        image = self.image_loader.load(png_path)

        # Load palette names from JSON
        names = json_reader(json_path)

        width, height = image.get_size()

        # First row contains the base colors
        base_colors = [image.get_at((x, 0)) for x in range(width)]

        palettes = {}

        # Each row after the first is a new palette
        for y in range(1, height):
            cmap = {}

            for x, base in enumerate(base_colors):
                new = image.get_at((x, y))

                # Map base RGB -> new RGB
                key = (base.r, base.g, base.b)
                cmap[key] = (new.r, new.g, new.b)

            # Palette name from JSON or fallback
            name = names[y - 1] if y - 1 < len(names) else f"palette_{y}"
            palettes[name] = cmap

        return palettes
    