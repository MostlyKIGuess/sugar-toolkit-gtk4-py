"""Tests for Style module."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

try:
    import gi
    gi.require_version("Gtk", "4.0")
    from gi.repository import Gtk, Gdk
    GTK_AVAILABLE = True
except (ImportError, ValueError):
    GTK_AVAILABLE = False

from sugar.graphics import style


class TestColor(unittest.TestCase):
    """Test cases for Color class."""

    def test_color_creation(self):
        """Test basic Color creation."""
        color = style.Color("#FF0000")
        self.assertEqual(color.get_html(), "#ff0000")

        color_with_alpha = style.Color("#00FF00", 0.5)
        rgba = color_with_alpha.get_rgba()
        self.assertEqual(rgba[3], 0.5)

    def test_color_rgba(self):
        """Test RGBA values."""
        color = style.Color("#FF8000")
        rgba = color.get_rgba()
        self.assertAlmostEqual(rgba[0], 1.0, places=2)  # Red
        self.assertAlmostEqual(rgba[1], 0.5, places=2)  # Green
        self.assertAlmostEqual(rgba[2], 0.0, places=2)  # Blue
        self.assertEqual(rgba[3], 1.0)  # Alpha

    def test_color_html(self):
        """Test HTML color conversion."""
        color = style.Color("#ABCDEF")
        self.assertEqual(color.get_html(), "#abcdef")

    def test_color_css_rgba(self):
        """Test CSS RGBA format."""
        color = style.Color("#FF0000", 0.8)
        css_rgba = color.get_css_rgba()
        self.assertEqual(css_rgba, "rgba(255, 0, 0, 0.8)")

    def test_color_svg(self):
        """Test SVG color format."""
        color = style.Color("#FF0000")
        self.assertEqual(color.get_svg(), "#ff0000")

        transparent_color = style.Color("#FF0000", 0.0)
        self.assertEqual(transparent_color.get_svg(), "none")

    def test_color_with_alpha(self):
        """Test creating color with different alpha."""
        color = style.Color("#FF0000")
        new_color = color.with_alpha(0.5)
        self.assertEqual(new_color.get_rgba()[3], 0.5)
        self.assertEqual(new_color.get_html(), "#ff0000")

    def test_color_int(self):
        """Test integer color representation."""
        color = style.Color("#FF0000")
        int_color = color.get_int()
        self.assertIsInstance(int_color, int)

    @unittest.skipUnless(GTK_AVAILABLE, "GTK4 not available")
    def test_gdk_rgba(self):
        """Test GDK RGBA conversion."""
        color = style.Color("#FF8000", 0.75)
        gdk_rgba = color.get_gdk_rgba()
        self.assertIsInstance(gdk_rgba, Gdk.RGBA)
        self.assertAlmostEqual(gdk_rgba.red, 1.0, places=2)
        self.assertAlmostEqual(gdk_rgba.green, 0.5, places=2)
        self.assertAlmostEqual(gdk_rgba.blue, 0.0, places=2)
        self.assertAlmostEqual(gdk_rgba.alpha, 0.75, places=2)

    def test_invalid_color(self):
        """Test invalid color input."""
        with self.assertRaises(ValueError):
            style.Color("#GGGGGG")  # Invalid hex

        with self.assertRaises(ValueError):
            style.Color("#FF")  # Too short

    def test_alpha_clamping(self):
        """Test alpha value clamping."""
        color_high = style.Color("#FF0000", 2.0)
        self.assertEqual(color_high.get_rgba()[3], 1.0)

        color_low = style.Color("#FF0000", -0.5)
        self.assertEqual(color_low.get_rgba()[3], 0.0)


class TestFont(unittest.TestCase):
    """Test cases for Font class."""

    def test_font_creation(self):
        """Test basic Font creation."""
        font = style.Font("Sans 12")
        self.assertEqual(str(font), "Sans 12")

    def test_font_css_string(self):
        """Test CSS string generation."""
        font = style.Font("Sans bold 14")
        css = font.get_css_string()
        self.assertIn("font-family: Sans", css)
        self.assertIn("font-size: 14pt", css)
        self.assertIn("font-weight: bold", css)

    def test_font_css_italic(self):
        """Test CSS generation for italic fonts."""
        font = style.Font("Arial italic 12")
        css = font.get_css_string()
        self.assertIn("font-style: italic", css)

    @unittest.skipUnless(GTK_AVAILABLE, "GTK4 not available")
    def test_pango_desc(self):
        """Test Pango font description."""
        font = style.Font("Sans 12")
        pango_desc = font.get_pango_desc()
        self.assertIsNotNone(pango_desc)


class TestStyleConstants(unittest.TestCase):
    """Test cases for style constants."""

    def test_zoom_factor(self):
        """Test zoom factor calculation."""
        self.assertIsInstance(style.ZOOM_FACTOR, float)
        self.assertGreater(style.ZOOM_FACTOR, 0)

    def test_zoom_function(self):
        """Test zoom function."""
        result = style.zoom(100)
        self.assertIsInstance(result, int)
        self.assertEqual(result, int(100 * style.ZOOM_FACTOR))

    def test_spacing_constants(self):
        """Test spacing constants are properly zoomed."""
        self.assertIsInstance(style.DEFAULT_SPACING, int)
        self.assertIsInstance(style.DEFAULT_PADDING, int)
        self.assertGreater(style.DEFAULT_SPACING, 0)
        self.assertGreater(style.DEFAULT_PADDING, 0)

    def test_icon_size_constants(self):
        """Test icon size constants."""
        sizes = [
            style.SMALL_ICON_SIZE,
            style.STANDARD_ICON_SIZE,
            style.MEDIUM_ICON_SIZE,
            style.LARGE_ICON_SIZE,
            style.XLARGE_ICON_SIZE,
        ]

        for size in sizes:
            self.assertIsInstance(size, int)
            self.assertGreater(size, 0)

        # Check size ordering
        self.assertLess(style.SMALL_ICON_SIZE, style.STANDARD_ICON_SIZE)
        self.assertLess(style.STANDARD_ICON_SIZE, style.MEDIUM_ICON_SIZE)
        self.assertLess(style.MEDIUM_ICON_SIZE, style.LARGE_ICON_SIZE)
        self.assertLess(style.LARGE_ICON_SIZE, style.XLARGE_ICON_SIZE)

    def test_color_constants(self):
        """Test predefined color constants."""
        colors = [
            style.COLOR_BLACK,
            style.COLOR_WHITE,
            style.COLOR_PRIMARY,
            style.COLOR_SUCCESS,
            style.COLOR_WARNING,
            style.COLOR_ERROR,
        ]

        for color in colors:
            self.assertIsInstance(color, style.Color)
            rgba = color.get_rgba()
            self.assertEqual(len(rgba), 4)

    def test_font_constants(self):
        """Test predefined font constants."""
        fonts = [
            style.FONT_NORMAL,
            style.FONT_BOLD,
            style.FONT_ITALIC,
        ]

        for font in fonts:
            self.assertIsInstance(font, style.Font)
            self.assertIsInstance(str(font), str)


@unittest.skipUnless(GTK_AVAILABLE, "GTK4 not available")
class TestStyleGTKIntegration(unittest.TestCase):
    """Test cases for GTK4 integration."""

    def setUp(self):
        """Set up test fixtures."""
        if not Gtk.is_initialized():
            Gtk.init()

    def test_apply_css_to_widget(self):
        """Test CSS application to widgets."""
        button = Gtk.Button(label="Test")
        css = "button { background-color: red; }"

        # Should not raise an exception
        style.apply_css_to_widget(button, css)

    def test_css_integration_with_colors(self):
        """Test CSS integration with Color objects."""
        color = style.COLOR_PRIMARY
        css_color = color.get_css_rgba()

        button = Gtk.Button(label="Test")
        css = f"button {{ background-color: {css_color}; }}"

        # Should not raise an exception
        style.apply_css_to_widget(button, css)

    def test_css_integration_with_fonts(self):
        """Test CSS integration with Font objects."""
        font = style.FONT_BOLD
        css_font = font.get_css_string()

        label = Gtk.Label(label="Test")
        css = f"label {{ {css_font}; }}"

        # Should not raise an exception
        style.apply_css_to_widget(label, css)


class TestStyleWithoutGTK(unittest.TestCase):
    """Test cases that work without GTK."""

    def test_zoom_factor_environment(self):
        """Test zoom factor with environment variable."""
        original_scaling = os.environ.get('SUGAR_SCALING')

        try:
            os.environ['SUGAR_SCALING'] = '150'
            # Need to reload the module to test environment variable
            import importlib
            importlib.reload(style)
            # This is approximate since ZOOM_FACTOR is calculated at import

        finally:
            if original_scaling is not None:
                os.environ['SUGAR_SCALING'] = original_scaling
            elif 'SUGAR_SCALING' in os.environ:
                del os.environ['SUGAR_SCALING']

    def test_color_edge_cases(self):
        """Test Color edge cases."""
        # Test with different cases
        color = style.Color("#ffFFff")
        self.assertEqual(color.get_html(), "#ffffff")

        # Test with spaces
        color = style.Color("  #123456  ")
        self.assertEqual(color.get_html(), "#123456")


if __name__ == "__main__":
    unittest.main()
