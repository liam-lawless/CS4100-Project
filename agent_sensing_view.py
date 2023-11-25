"""
File name: agent_sensing_view.py
Author(s): Liam Lawless
Date created: November 24, 2023
Last modified: November 24, 2023

Description:
    This file contains the AgentSensingView class, which handles the graphical representations of the agents vision and direction.

Dependencies:
    - PIL (Pillow): Provides ability to create an image with transparency
"""

from PIL import Image, ImageTk, ImageDraw

class AgentSensingView:
    def __init__(self, canvas):
        self.canvas = canvas
        self.images = []  # Keep references to prevent garbage collection

    def create_transparent_oval(self, x, y, a, b, **options):
        alpha = options.pop('alpha', 1) * 255
        fill = options.pop('fill', '')
        fill_rgb = self.canvas.winfo_rgb(fill) + (int(alpha),)
        image = Image.new('RGBA', (a - x, b - y), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.ellipse((0, 0, a - x, b - y), fill=fill_rgb)
        self.images.append(ImageTk.PhotoImage(image))
        self.canvas.create_image(x, y, image=self.images[-1], anchor='nw')
        outline_option = options.pop('outline', '')
        if outline_option:
            self.canvas.create_oval(x, y, a, b, outline=outline_option, **options)

    def create_sensing_radius(self, x, y, width, height, heading_angle, body_fill, heading_fill, body_alpha=1.0, heading_alpha=1.0, start_angle=0):
        # Determine the bottom-right coordinates of the bounding box based on the width and height
        a = x + width
        b = y + height
        
        # Draw the sensing circle
        self.create_transparent_oval(x, y, a, b, 
            fill=body_fill, 
            alpha=body_alpha,
            outline='')

        # Adjust start angle
        start_angle = start_angle
        
        # Calculate the start and end angles for the heading
        half_heading_angle = heading_angle / 2
        start_heading_angle = start_angle - half_heading_angle
        end_heading_angle = start_angle + half_heading_angle

        # Create an overlay image for the heading with a wedge shape
        heading_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(heading_image)
        
        # Draw the heading cut-out as a filled pie slice with the fill color and alpha
        mouth_fill_with_alpha = self.canvas.winfo_rgb(heading_fill) + (int(heading_alpha * 255),)
        draw.pieslice([(0, 0), (width, height)], start=start_heading_angle, end=end_heading_angle, fill=mouth_fill_with_alpha)
        
        # Overlay the heading image onto the body
        self.images.append(ImageTk.PhotoImage(heading_image))
        self.canvas.create_image(x, y, image=self.images[-1], anchor='nw')

    def clear_sensing_radii(self):
        for image in self.images:
            self.canvas.delete(image)
        self.images.clear()  # Clear the references to the images