import typing

from PIL import Image
import tempfile
import os

def frame(input_img_path: str, 
        frame_dimensions: typing.Tuple[typing.Union[int, float], typing.Union[int, float]] = (1080, 1350),
        *, 
        border_sides: typing.Union[int, float] = 60, 
        border_top: typing.Union[int, float] = 60, 
        border_bottom: typing.Union[int, float] = 60, 
        img_x_off: typing.Union[int, float] = 0, 
        img_y_off: typing.Union[int, float] = 0,
        scale:int = 1):
    
    frame_width, frame_height = frame_dimensions
    
    frame_width = int(round(frame_width*scale))
    frame_height = int(round(frame_height*scale))
    
    border_sides = int(round(border_sides*scale))
    border_top = int(round(border_top*scale))
    border_bottom = int(round(border_bottom*scale))
    
    landscape = False
    
    img = Image.open(input_img_path)
    img_w, img_h = img.size
    
    # if img_w > img_h:
    #     landscape = True
    #     frame_width, frame_height = frame_height, frame_width

    inner_width = frame_width - (2 * border_sides)
    inner_height = frame_height - border_top - border_bottom

    cover_scale = max(inner_width / img_w, inner_height / img_h)
    resized_width = int(round(img_w * cover_scale))
    resized_height = int(round(img_h * cover_scale))
    img = img.resize((resized_width, resized_height), Image.Resampling.LANCZOS)

    max_x_crop = max(0, img.width - inner_width)
    max_y_crop = max(0, (img.height - inner_height)/2)
    
    print(f"Image size: {img.size}, Inner size: ({inner_width}, {inner_height})")
    print(f"Max x crop: {max_x_crop}, Max y crop: {max_y_crop}")

    if abs(img_y_off) > max_y_crop / 2:
        print(f"Warning: Image y offset is greater than half the crop range. \nThis may result in unexpected cropping.\n[{img_y_off} > {max_y_crop / 2}]")

    left = (img.width - inner_width) / 2 + img_x_off
    top = (img.height - inner_height) / 2 + img_y_off

    img = img.crop((left, top, left + inner_width, top + inner_height))
    
    x_off = int(round(border_sides))
    y_off = int(round(border_top))
    
    framed = Image.new("RGB", (frame_width, frame_height), (255, 255, 255))
    
    framed.paste(img, (x_off, y_off))
    
    output_img = "framed_" + input_img_path.split('/')[-1]
    
    if not os.path.exists("output"):
        os.makedirs("output")
    
    output_path = os.path.join("output", output_img)
    
    framed =framed.resize((framed.width, framed.height), Image.Resampling.LANCZOS)
    
    framed.save(output_path, dpi=(300, 300), quality=95)
    print(f"Framed image saved as {output_path}")


if __name__ == "__main__":
    import time
    
    if not os.path.exists("input"):
        os.makedirs("input")
        print("Input folder created. Please add images to the 'input' folder and rerun the script.")
    
    for file in os.listdir("input"):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            start_time = time.time()
            
            # INSTAX MINI
            # border_sides=47.2, 
            # border_top=71.4, 
            # border_bottom=212, 
            # frame_width=637.8, 
            # frame_height=1015.7
            # frame(f"input/{file}", (637.8, 1015.7), scale=1, border_sides=47.2, border_top=71.4, border_bottom=212)
            
            # INSTAX SQUARE
            # border_sides=59.1, 
            # border_top=71,  
            # border_bottom=212.5, 
            # frame_width=850.4, 
            # frame_height=1015.7
            # frame(f"input/{file}", (850.4, 1015.7), scale=1, border_sides=59.1, border_top=71.4, border_bottom=212)
            
            # INSTAX WIDE
            # border_sides=53.2, 
            # border_top=71.1, 
            # border_bottom=212.4, 
            # frame_width=1275.6, 
            # frame_height=1015.7
            # frame(f"input/{file}", (1275.6, 1015.7), scale=1, border_sides=53.2, border_top=71.4, border_bottom=212)
            
            # POLAROID GO
            # border_sides=46.7, 
            # border_top=59.1, 
            # border_bottom=172.4, 
            # frame_width=636.6, 
            # frame_height=786.6
            # frame(f"input/{file}", (636.6, 786.6), scale=1, border_sides=46.7, border_top=59.1, border_bottom=172.4)
            frame(f"input/{file}", (1080, 1350), scale=3, border_sides=60, border_top=60, border_bottom=60)
            print(f"Execution time: {(time.time() - start_time):.2f} seconds")
        