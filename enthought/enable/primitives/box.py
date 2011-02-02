""" Define a simple filled box component.
"""

# Parent package imports
from enthought.enable.api import border_size_trait, Component, transparent_color
from enthought.enable.colors import ColorTrait
from enthought.kiva.constants import FILL, STROKE

class Box(Component):

    color        = ColorTrait("white")
    border_color = ColorTrait("black")
    border_size  = border_size_trait

    def _draw_mainlayer(self, gc, view_bounds=None, mode="default"):
        "Draw the box background in a specified graphics context"

        gc.save_state()

        # Set up all the control variables for quick access:
        bs  = self.border_size
        bsd = bs + bs
        bsh = bs / 2.0
        x, y = self.position
        dx, dy = self.bounds

        # Fill the background region (if required);
        color = self.color_
        if color is not transparent_color:
            gc.set_fill_color(color)
            gc.draw_rect((x + bs, y + bs, dx - bsd, dy - bsd), FILL)

        # Draw the border (if required):
        if bs > 0:
            border_color = self.border_color_
            if border_color is not transparent_color:
                gc.set_stroke_color(border_color)
                gc.set_line_width(bs)
                gc.draw_rect((x + bsh, y + bsh, dx - bs, dy - bs), STROKE)

        gc.restore_state()
        return

# EOF
