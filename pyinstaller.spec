# -*- mode: python -*-

import pkg_resources
import site

block_cipher = None


def Entrypoint(dist, group, name, **kwargs):

    # get toplevel packages of distribution from metadata
    def get_toplevel(dist):
        distribution = pkg_resources.get_distribution(dist)
        if distribution.has_metadata('top_level.txt'):
            return list(distribution.get_metadata('top_level.txt').split())
        else:
            return []

    kwargs.setdefault('binaries', [])
    kwargs.setdefault('datas', [])
    kwargs.setdefault('hiddenimports', [])
    packages = []
    for distribution in kwargs['hiddenimports']:
        packages += get_toplevel(distribution)

    kwargs.setdefault('hookspath', ['.'])
    kwargs.setdefault('hooksconfig', {})
    kwargs.setdefault('runtime_hooks', [])
    kwargs.setdefault('excludes', [])
    kwargs.setdefault('win_no_prefer_redirects', False)
    kwargs.setdefault('win_private_assemblies', False)
    kwargs.setdefault('noarchive', False)

    spdir = site.getsitepackages()[-1]
    label_studio_dir = os.path.join(spdir, 'label_studio')
    kwargs.setdefault('pathex', [label_studio_dir])
    # get the entry point
    ep = pkg_resources.get_entry_info(dist, group, name)
    # insert path of the egg at the verify front of the search path
    kwargs['pathex'] = [ep.dist.location] + kwargs['pathex']
    # script name must not be a valid module name to avoid name clashes on import
    script_path = os.path.join(workpath, name + '-script.py')
    print ("creating script for entry point", dist, group, name)
    with open(script_path, 'w') as fh:
        print("import", ep.module_name, file=fh)
        print("%s.%s()" % (ep.module_name, '.'.join(ep.attrs)), file=fh)
        for package in packages:
            print ("import", package, file=fh)

    return Analysis([script_path], **kwargs)


a = Entrypoint(
    'label-studio',
    'console_scripts',
    'label-studio',
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='label-studio',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
