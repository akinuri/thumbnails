from PIL import Image

def float_to_duration(seconds = 0):
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = int(seconds % 60)
    duration = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    return duration

def merge_frames_into_grid(frame_paths, grid_size, img_width=None, img_height=None):
    images = [Image.open(path) for path in frame_paths]
    width, height = images[0].size
    grid_width = grid_size[0]
    grid_height = grid_size[1]
    grid = Image.new("RGB", (width * grid_width, height * grid_height))
    for index, image in enumerate(images):
        x = index % grid_width
        y = index // grid_width
        grid.paste(image, (x * width, y * height))
    if img_width or img_height:
        fitted = fit(grid.width, grid.height, img_width, img_height, round_values=True)
        if fitted["width"] != grid.width or fitted["height"] != grid.height:
            grid = grid.resize((fitted["width"], fitted["height"]))
    return grid

def fit(width, height, maxWidth=None, maxHeight=None, alignment="center center", round_values=False):
    valid_alignment_values = [
        "left top", "left center", "left bottom",
        "center", "center top", "center center", "center bottom",
        "right top", "right center", "right bottom"
    ]
    if alignment not in valid_alignment_values:
        raise ValueError("Invalid alignment value.")
    if alignment == "center":
        alignment = "center center"
    horizontal_align, vertical_align = alignment.split()
    result = {
        "width": 0,
        "height": 0,
        "top": None,
        "left": None,
        "right": None,
        "bottom": None,
        "alignment": alignment,
        "container": {
            "maxWidth": maxWidth,
            "maxHeight": maxHeight,
        },
    }
    if maxWidth is not None and maxHeight is None:
        if width <= maxWidth:
            result["width"] = width
            result["height"] = height
        else:
            ratio = maxWidth / width
            result["width"] = maxWidth
            result["height"] = height * ratio
    elif maxHeight is not None and maxWidth is None:
        if height <= maxHeight:
            result["width"] = width
            result["height"] = height
            result["left"] = 0
            result["top"] = (maxHeight - height) / 2
        else:
            ratio = maxHeight / height
            result["width"] = width * ratio
            result["height"] = maxHeight
    else:
        if width <= maxWidth and height <= maxHeight:
            result["width"] = width
            result["height"] = height
        else:
            ratio_width = maxWidth / width
            ratio_height = maxHeight / height
            ratio = min(ratio_width, ratio_height)
            result["width"] = width * ratio
            result["height"] = height * ratio
    if horizontal_align == "left":
        result["left"] = 0
    elif horizontal_align == "center":
        result["left"] = (maxWidth - result["width"]) / 2
        result["right"] = result["left"]
    elif horizontal_align == "right":
        result["right"] = 0
    if vertical_align == "top":
        result["top"] = 0
    elif vertical_align == "center":
        result["top"] = (maxHeight - result["height"]) / 2
        result["bottom"] = result["top"]
    elif vertical_align == "bottom":
        result["bottom"] = 0
    if round_values:
        result["width"] = round(result["width"])
        result["height"] = round(result["height"])
        result["top"] = round(result["top"])
        result["left"] = round(result["left"])
        result["right"] = round(result["right"])
        result["bottom"] = round(result["bottom"])
    return result

