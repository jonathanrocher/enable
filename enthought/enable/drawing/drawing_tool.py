
from enthought.traits.api import Enum
from enthought.enable.api import Component


class DrawingTool(Component):
    """
    A drawing tool is just a component that also defines a certain drawing mode
    so that its container knows how to render it and pass control to it.
    
    The DrawingTool base class also defines a draw() dispatch, so that 
    different draw methods are called depending on the event state of the tool.
    """

    # The mode in which this tool draws:
    #   "normal": the tool draws like a normal component, alongside other
    #             components in the container
    #   "overlay": the tool draws on top of over components in the container
    #   "exclusive": the tool gets total control of how the container should
    #                be rendered
    draw_mode = Enum("normal", "overlay", "exclusive")

    def reset(self):
        """
        Causes the tool to reset any saved state and revert its event_state
        back to the initial value (usually "normal").
        """
        pass
    
    def complete_left_down(self, event):
        """
        Default function that causes the tool to reset if the user starts
        drawing again.
        """
        self.reset()
        self.request_redraw()
        self.normal_left_down(event)
        return
    
    def _draw_mainlayer(self, gc, view_bounds, mode="default"):
        draw_func = getattr(self, self.event_state + "_draw", None)
        if draw_func:
            draw_func(gc)
        return
    
    def request_redraw(self):
        if self.container is not None:
            self.container.request_redraw()
        elif hasattr(self, "canvas") and self.canvas is not None:
            self.canvas.request_redraw()
        else:
            pass
        return
    

# EOF
