# Label Studio PyInstaller

This repository contains hooks and `.spec` files to support building
[Label Studio](https://labelstud.io/) as a standalone executable.

## Bundling

It's pretty simple. First, set up the environment using `conda`:

```sh
conda env create --file environment.yml
```

Once the environment is created, simply run:

```sh
python build_label_studio.py
```

The bundled executable will be available as `dist/label-studio.exe`.

## Details

1. The environment includes a few things to support either Label Studio
   itself, or analysis of Label Studio by PyInstaller:

    * This is tested and intended for Windows only.
    * `pathex` includes the `label_studio` root directory because many of the
      Django applications that are part of Label Studio are self-contained.
      For example, modules within the `label_studio.core` package do not
      import from `label_studio.core`, they import from `core` as top-level.
    * `coverage` is included because of a `label_studio` `site_customize.py`
      file that is exposed by adding the `label_studio` root directory to the
      set of paths searched by PyInstaller.
    * `gdal` is included because of a Django dependency. It is pinned at
      3.1 despite versions up to 3.4 being available because, at time of this
      writing, it will not locate `gdalXXX.dll` files beyond `gdal301`.
    * Two files are patched as part of bundling:
        * `label_studio.core.templatetags` has an `__init__.py` added by
          patching, to help PyInstaller's `collect_submodules` hook locate
          and bundle its filters correctly.
        * `label_studio.core.version` does not have logic to support
          correct discovery of version information when bundled. This patch
          ensures good behavior of its `get_git_commit_info()` function.
          Note: it is hardcoded to provide information given the 1.4
          release right now. This could be improved in the future, but may
          not be necessary.
    * The hidden imports and datas collected by `hook-label_studio.py` are
      based on two sources of information:
        * The `label_studio` 1.4 tag `MANIFEST.in` file.
        * Extensive trial and error bundling and testing the executable at
          runtime.
    * The `pyinstaller.spec` is written with arguments to support "onefile"
      executable bundling.
    * The `build_label_studio.py` script assumes Git for Windows will be
      installed for use of its bundled `patch.exe`.
