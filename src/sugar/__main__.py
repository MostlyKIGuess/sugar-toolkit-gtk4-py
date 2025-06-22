"""Main entry point for sugar-toolkit-gtk4-py."""

import sys


def main():
    # NOTE: Following is subject to change in future versions
    """Main entry point for testing the toolkit."""
    print("Sugar Toolkit GTK4 Python")
    print("=" * 25)
    print()

    try:
        from sugar.graphics.xocolor import XoColor

        print("XoColor import successful")

        # Test XoColor
        color = XoColor()
        print(f" XoColor creation successful: {color.to_string()}")

    except Exception as e:
        print(f" XoColor test failed: {e}")
        return 1

    try:
        # Only test Activity if GTK is available
        import gi

        gi.require_version("Gtk", "4.0")

        from sugar.activity.activity import Activity

        print(" Activity import successful")

        # basic Activity creation (without showing)
        activity = Activity()
        print(f" Activity creation successful: {activity.get_id()[:8]}...")

    except Exception as e:
        print(f" Activity test failed: {e}")
        print("  (This is expected if GTK4 is not available)")

    print()
    print("Basic toolkit test completed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
