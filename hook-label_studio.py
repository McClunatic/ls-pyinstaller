import os

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

datas = []
for dirname in ('lsf', 'react-app', 'dm'):
    datas += collect_data_files(
        'label_studio',
        subdir=os.path.join('frontend', 'dist', dirname)
    )

datas += collect_data_files(
    'label_studio',
    includes=['*.html'],
)

datas += collect_data_files(
    'label_studio',
    subdir='annotation_templates',
)

datas += collect_data_files(
    'label_studio',
    subdir='annotation_templates',
)

for dirname in ('static', 'static_build'):
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

hiddenimports = collect_submodules('label_studio.core.settings')
hiddenimports += collect_submodules('corsheaders')
hiddenimports += collect_submodules('django_extensions')
hiddenimports += collect_submodules('django_rq')
hiddenimports += collect_submodules('rules')
hiddenimports += collect_submodules('annoying')
hiddenimports += collect_submodules('rest_framework_swagger')
hiddenimports += collect_submodules('drf_generators')

datas += collect_data_files('coreschema', include_py_files=True)
datas += collect_data_files('rest_framework', include_py_files=True)
datas += collect_data_files('label_studio.core', include_py_files=True)
datas += collect_data_files('users', include_py_files=True)
datas += collect_data_files('boxing', includes=['*.json'])
