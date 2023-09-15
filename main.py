import numpy as np
import ast
from PIL import Image 

KEY_TO_RGB = {
    "b": "(50, 50, 255)",
    "v": "(209, 95, 238)",
    "p": "(255, 52, 179)",
    "y": "(255, 255, 0)",
    "o": "(255, 128, 0)", 
    "g": "(0, 205, 0)",
    "w": "(255, 255, 255)"
}
KEY_TO_COLOR = {
    "b": "BLUE",
    "v": "VIOLET",
    "p": "PINK",
    "y": "YELLOW",
    "o": "ORANGE", 
    "g": "GREEN",
    "w": "WHITE"
}
KEY_TO_PATTERN = {
    "h": "HORIZONTAL",
    "v": "VERTICAL", 
    "s": "SPLATTER"
}

class TieDyeDesigner: 
    """
    A class to represent tye-dye design generator. 

    ...
    
    Attributes 
    ----------
    transition_matrix: dict
        probabilities that one color will follow another used by Markov chain
    colors: list 
        list of non-background colors (or dyes) used in design
    background: str
        background color for design
    pattern: str
        type of pattern (splatter, vertical, or horizontal)

    Methods 
    -------
    compose_image(image_width=100, image_height=100)
        Returns an image generated with the TieDyeDesigner attributes in the given
        width and height.  

    """

    def __init__(self, colors, background, pattern): 
        self.transition_matrix = self.__generate_transition_matrix_from_inputs(colors, background)
        self.colors = colors
        self.colors.append(background)
        self.background = background
        self.pattern = pattern

    def __get_background_probabilities(self, colors, background): 
        """Generate probabilities for which colors should border the background."""
        background_prob = {}
        sum = 1
        background_prob[background] = 0.7 
        sum -= 0.7
        other_prob = 0.3 / len(colors)
        for color in colors: 
            sum -= other_prob
            background_prob[color] = other_prob
        background_prob[background] += sum
        return background_prob
    
    def __generate_transition_matrix_from_inputs(self, colors, background): 
        """Generate probabilities for the colors and backgrounds in TieDyeDesigner."""
        transition_matrix = {}
        for color in colors: 
            color_prob = {}
            for next_color in colors: 
                if color is next_color: 
                    color_prob[next_color] = 0.9
                else: 
                    color_prob[next_color] = 0
            color_prob[background] = 0.1
            transition_matrix[color] = color_prob
        background_prob = self.__get_background_probabilities(colors, background)
        transition_matrix[background] = background_prob
        return transition_matrix
    
    def __get_pixel_color_splatter(self, color, second_color=None):
        """Return random pixel color for splatter pattern using weights 
        from transition matrix (takes average of two probabilities).
        """
        if second_color is None: 
            choice = np.random.choice(
                self.colors, 
                p=[self.transition_matrix[color][next_color] for next_color in self.colors]
            )
        else: 
            choice = np.random.choice(
                self.colors, 
                p=[(self.transition_matrix[color][next_color]+self.transition_matrix[second_color][next_color])/2 for next_color in self.colors]
            )
        return choice

    def __get_pixel_color_h_or_v(self, color):
        """Return random pixel color for horizontal or vertical patterns
        using weights from transition matrix.
        """        
        choice = np.random.choice(
            self.colors, 
            p=[self.transition_matrix[color][next_color] for next_color in self.colors]
        )
        return choice

    def compose_image(self, image_width=100, image_height=100):
        """Return Image object (using PIL) with pixels generated according
        to pattern type and transition matrix of colors and probabilities.
        """
        image = Image.new(mode="RGB", size=(image_width, image_height), color="white")
        color = np.random.choice(self.colors)
        current_x = 0
        current_y = 0

        if self.pattern == 'h': 
            # pixels filled in across then down 
            while current_y < image_height:
                while current_x < image_width: 
                    pixel_string = self.__get_pixel_color_h_or_v(color=color)
                    next_pixel_color = ast.literal_eval(pixel_string)
                    color = pixel_string
                    image.putpixel(
                        [current_x, current_y], 
                        next_pixel_color)
                    current_x += 1
                current_y += 1
                current_x = 0
        elif self.pattern == 'v': 
            # pixels filled in down then across 
            while current_x < image_width:
                while current_y < image_height: 
                    pixel_string = self.__get_pixel_color_h_or_v(color=color)
                    next_pixel_color = ast.literal_eval(pixel_string)
                    color = pixel_string
                    image.putpixel(
                        [current_x, current_y], 
                        next_pixel_color)
                    current_y += 1
                current_x += 1
                current_y = 0
        else: 
            # pixels filled in across then down 
            while current_y < image_height:
                border = current_y == 0
                while current_x < image_width: 
                    if border is False: 
                        second_color = str(image.getpixel((current_x, current_y-1)))
                    else: 
                        second_color = None
                    pixel_string = self.__get_pixel_color_splatter(color=color, second_color=second_color)
                    next_pixel_color = ast.literal_eval(pixel_string)
                    color = pixel_string
                    image.putpixel(
                        [current_x, current_y], 
                        next_pixel_color)
                    current_x += 1
                current_y += 1
                current_x = 0

        return image

def main(): 
    print("Welcome to the Tie-Dye Designer! Please choose which colors you want to use to dye your pattern.\n")
    print("Key: \nblue - b\nviolet - v\npink - p\norange - o\nyellow - y\ngreen - g\n")

    color_input = input("Choose a color using the key\n")
    colors = []
    while (color_input != "q") and len(colors) < 6: 
        if color_input in KEY_TO_COLOR.keys():
            colors.append(KEY_TO_RGB[color_input])
            print("You chose " + KEY_TO_COLOR[color_input] + ".")
            color_input = input("Choose another color or type 'q' to quit.\n")
        else: 
            color_input = input("Please type a value in the key or 'q'.\n")
    
    pattern_input = input("Choose a pattern using the key.\nsplatter - s\nvertical - v\nhorizontal - h\n")
    while pattern_input not in {"s", "v", "h"}: 
        pattern_input = input("Please a pattern using the key (s, v, or h).\n")
    print("The pattern will be " + KEY_TO_PATTERN[pattern_input] + ".")

    background_input = input("The background is currently white. To keep it white, type 'w', or change it with the color key.\n")
    if background_input in KEY_TO_COLOR.keys(): 
        print("The background will be " + KEY_TO_COLOR[background_input] + ". Generating image now.")
        background = KEY_TO_RGB[background_input]
    else: 
        while background_input not in KEY_TO_COLOR.keys():
            background_input = input("Please type a value in the key or 'w' to choose the background.\n")
        print("The background will be " + KEY_TO_COLOR[background_input] + ". Generating image now.")
        background = KEY_TO_RGB[background_input]

    designer = TieDyeDesigner(colors, background, pattern=pattern_input)

    generate = True

    while generate is True: 
        designer.compose_image().show()
        generate = input(
            "Generate another image with the same inputs? Type 'y' for yes and anything else for no.\n"
            ) == 'y'
    
if __name__ == "__main__": 
    main()