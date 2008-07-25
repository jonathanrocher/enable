#------------------------------------------------------------------------------
# Copyright (c) 2005-2007 by Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
#------------------------------------------------------------------------------
""" Trait definition for an RGBA-based color, which is either:

* A tuple of the form (*red*,*green*,*blue*,*alpha*), where each component is
  in the range from 0.0 to 1.0
* An integer which in hexadecimal is of the form 0xAARRGGBB, where AA is alpha,
  RR is red, GG is green, and BB is blue.
"""


from enthought.traits.api import Trait, TraitError, TraitFactory
from enthought.traits.trait_base import SequenceTypes

from enthought.etsconfig.api import ETSConfig

if ETSConfig.toolkit == 'wx':
    from enthought.traits.ui.wx.color_trait import standard_colors
elif ETSConfig.toolkit == 'qt4':
    # FIXME
    #from enthought.traits.ui.qt4.color_trait import standard_colors
    standard_colors = {}
else:
    standard_colors = {}


#-------------------------------------------------------------------------------
#  Convert a value into an Enable/Kiva color:
#-------------------------------------------------------------------------------

def convert_to_color ( object, name, value ):
    """ Converts a value to an Enable or Kiva color.
    """
    if ((type( value ) in SequenceTypes) and
        (len( value ) == 4) and
        (0.0 <= value[0] <= 1.0) and
        (0.0 <= value[1] <= 1.0) and
        (0.0 <= value[2] <= 1.0) and
        (0.0 <= value[3] <= 1.0)):
        return value
    if type( value ) is int:
        result = ( ((value >> 24) & 0xFF) / 255.0,
                   ((value >> 16) & 0xFF) / 255.0,
                   ((value >>  8) & 0xFF) / 255.0,
                    (value & 0xFF)        / 255.0 )
        return result
    raise TraitError

convert_to_color.info = ('a tuple of the form (red,green,blue,alpha), where '
                         'each component is in the range from 0.0 to 1.0, or '
                         'an integer which in hex is of the form 0xAARRGGBB, '
                         'where AA is alpha, RR is red, GG is green, and BB is '
                         'blue')

#-------------------------------------------------------------------------------
#  Standard colors:
#-------------------------------------------------------------------------------

# RGBA versions of standard colors
rgba_standard_colors = {}
for name, color in standard_colors.items():
    rgba_standard_colors[ name ] = ( color.Red()   / 255.0,
                                     color.Green() / 255.0,
                                     color.Blue()  / 255.0,
                                     1.0 )
rgba_standard_colors[ 'clear' ] = ( 0, 0, 0, 0 )


#-------------------------------------------------------------------------------
#  Define Enable/Kiva specific color traits:
#-------------------------------------------------------------------------------

def RGBAColorFunc(*args, **metadata):
    """
    Returns a trait whose value must be a GUI toolkit-specific RGBA-based color.

    Description
    -----------
    For wxPython, the returned trait accepts any of the following values:

    * A tuple of the form (*r*, *g*, *b*, *a*), in which *r*, *g*, *b*, and *a*
      represent red, green, blue, and alpha values, respectively, and are floats
      in the range from 0.0 to 1.0
    * An integer whose hexadecimal form is 0x*AARRGGBB*, where *AA* is the alpha
      (transparency) value, *RR* is the red value, *GG* is the green value, and
      *BB* is the blue value

    Default Value
    -------------
    For wxPython, (1.0, 1.0, 1.0, 1.0) (that is, opaque white)
    """
    # The editor is commented out for now to avoid a circular import.
    if ETSConfig.toolkit == 'wx':
        from enthought.enable.traits.ui.wx.rgba_color_editor import RGBAColorEditor
    elif ETSConfig.toolkit == 'qt4':
        # FIXME
        #from enthought.enable.traits.ui.qt4.rgba_color_editor import RGBAColorEditor
        RGBAColorEditor = None
    else:
        RGBAColorEditor = None
    
    tmp_trait = Trait( 'white', convert_to_color, rgba_standard_colors, 
           editor = RGBAColorEditor )
    return tmp_trait(*args, **metadata)


RGBAColorTrait = TraitFactory( RGBAColorFunc )
RGBAColor = RGBAColorTrait

