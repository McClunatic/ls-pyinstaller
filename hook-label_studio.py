import os
import pathlib
import site

from typing import Iterator, Union

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Make sure label_studio settings are visible for the django hook
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'label_studio.core.settings.label_studio',
)

# Load datas based on the MANIFEST.in for label_studio
datas = []
for dirname in ('lsf', 'react-app', 'dm'):
    frontends = collect_data_files(
        'label_studio',
        subdir=os.path.join('frontend', 'dist', dirname)
    )
    datas += [
        (src, dst.replace('label_studio' + os.sep, ''))
        for src, dst in frontends
    ]

datas += collect_data_files(
    'label_studio',
    subdir='annotation_templates',
)

for dirname in ('static'):
    datas += collect_data_files(
        'label_studio',
        subdir=os.path.join('core', dirname),
    )

datas += collect_data_files(
    'label_studio',
    subdir=os.path.join('core', 'utils', 'schema'),
    includes=['*.json'],
)

datas += collect_data_files(
    'label_studio',
    subdir=os.path.join('core', 'utils', 'schema'),
    includes=['*.json'],
)

datas += collect_data_files(
    'label_studio',
    subdir='io_storages',
    includes=['*.yml'],
)

datas += collect_data_files(
    'label_studio',
    subdir='io_storages',
    includes=['*.yml'],
)

datas += collect_data_files(
    'label_studio',
    subdir='tests',
    includes=['*.sh'],
)

datas += collect_data_files(
    'label_studio',
    subdir=os.path.join('tests', 'loadtests'),
    includes=['*.txt'],
)

datas += collect_data_files(
    'label_studio',
    subdir=os.path.join('tests', 'test_data'),
    includes=['*.yml'],
)

datas += collect_data_files(
    'label_studio',
    subdir=os.path.join('tests', 'test_suites', 'samples'),
)

datas += collect_data_files(
    'label_studio',
    subdir=os.path.join('tests', 'test_suites'),
    includes=['*.yml'],
)

datas += collect_data_files(
    'label_studio',
    includes=['*.ini'],
)

# Collect hidden imports encountered in testing
hiddenimports = collect_submodules('label_studio.core.settings')
hiddenimports += collect_submodules('corsheaders')
hiddenimports += collect_submodules('django_extensions')
hiddenimports += collect_submodules('django_rq')
hiddenimports += collect_submodules('rules')
hiddenimports += collect_submodules('annoying')
hiddenimports += collect_submodules('rest_framework_swagger')
hiddenimports += collect_submodules('drf_generators')
hiddenimports += collect_submodules('django_user_agents')
hiddenimports += collect_submodules('drf_yasg')

# Load embedded django applications as top-level modules
for mod in (
    'core',
    'users',
    'organizations',
    'data_import',
    'data_export',
    'projects',
    'tasks',
    'data_manager',
    'io_storages',
    'ml',
    'webhooks',
    'core.middleware',
):
    ls_submodules = collect_submodules(mod)
    hiddenimports += ls_submodules

# Add further data encountered as part of testing
datas += collect_data_files('coreschema', include_py_files=True)
datas += collect_data_files('rest_framework', include_py_files=True)
datas += collect_data_files('label_studio.core', include_py_files=True)
datas += collect_data_files('boxing', includes=['*.json'])

# ...including fake top-level inside label_studio
datas += collect_data_files('data_manager.actions', include_py_files=True)

# Finally, get templates for django from main and label_studio-embedded apps
sp = pathlib.Path(site.getsitepackages()[-1])
ls = sp.joinpath('label_studio')

ls_templates = ls.joinpath('templates').rglob('*.html')
datas += [(str(tpl), str(tpl.relative_to(ls).parent)) for tpl in ls_templates]

templates = []
for mod in (
    'data_manager',
    'organizations',
    'projects',
    'users',
):
    path = ls.joinpath(mod)
    app_tpls = [tpl for tpl in path.rglob('*.html')]
    rel_tpls = [tpl.relative_to(path).parent for tpl in app_tpls]
    templates += list(zip(app_tpls, rel_tpls))

datas += [(str(a), str(r)) for a, r in templates]

# Try to get templatetags available for import as datas
datas += collect_data_files('projects.templatetags', include_py_files=True)

# For some reason the below finds .git/ files?'
# UPDATE: patch for __init__.py
datas += collect_data_files('core.templatetags', include_py_files=True)

# Make sure static_build ends up at /static
statics = collect_data_files('core', subdir='static_build')
datas += statics

# TODO:
#  - EDITOR_ROOT
#  - DM_ROOT
#  - REACT_APP_ROOT
#  - MEDIA_ROOT