def wrap_text(text, font, max_width):
    lines = []

    for paragraph in text.split("\n"):

        words = paragraph.split(" ")
        current = ""

        for word in words:
            test = word if current == "" else current + " " + word

            if font.size(test)[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word

        lines.append(current)

    return lines


