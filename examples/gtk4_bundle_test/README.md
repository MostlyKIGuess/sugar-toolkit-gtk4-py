# GTK4 Bundle Test Example

This example demonstrates how to bundle a minimal GTK4 Sugar activity using Flatpak.

## Files

- `main.py`: Minimal GTK4 Sugar activity (must start with `#!/usr/bin/env python3` and be executable).
- `org.sugarlabs.Gtk4BundleTest.json`: Flatpak manifest for building and running the bundle.

## How to Build and Run with Flatpak

1. Install Flatpak and the GNOME SDK:

   ```sh
   flatpak install flathub org.gnome.Platform//45 org.gnome.Sdk//45
   ```

2. Build the Flatpak bundle (from this directory(_the gtk4_bundle_test directory_ )):

   ```sh
   flatpak-builder --force-clean build-dir org.sugarlabs.Gtk4BundleTest.json
   ```

3. (Recommended) Install and run the app as a real Flatpak:

   ```sh
   flatpak-builder --user --install --force-clean build-dir org.sugarlabs.Gtk4BundleTest.json
   flatpak run org.sugarlabs.Gtk4BundleTest
   ```

   Or, for quick dev testing (may not set up the full GUI environment):

   ```sh
   flatpak-builder --run build-dir org.sugarlabs.Gtk4BundleTest.json org.sugarlabs.Gtk4BundleTest
   ```

## How to Create and Share a Flatpak Bundle

To generate a single-file Flatpak bundle you can send to others:

1. Build a Flatpak repository (from this directory):

   ```sh
   flatpak-builder --repo=repo --force-clean build-dir org.sugarlabs.Gtk4BundleTest.json
   ```

2. Create the bundle file:

   ```sh
   flatpak build-bundle repo Gtk4BundleTest.flatpak org.sugarlabs.Gtk4BundleTest
   ```

3. Send `Gtk4BundleTest.flatpak` to others. They can install it with:

   ```sh
   flatpak install --user Gtk4BundleTest.flatpak
   flatpak run org.sugarlabs.Gtk4BundleTest
   ```

This produces a portable `.flatpak` file that can be installed on any Flatpak-enabled system.

## Notes

- `main.py` must start with `#!/usr/bin/env python3` and be executable (`chmod +x main.py`).
- The manifest installs `main.py` as `/app/bin/org.sugarlabs.Gtk4BundleTest` and sets that as the Flatpak command.
- The manifest includes finish-args for GUI support (Wayland/X11, DRI, network, host fs).
- This example assumes you have the sugar-toolkit-gtk4-py source available two directories up from this example folder.
- You can adapt the manifest for your own app/bundle as needed.
