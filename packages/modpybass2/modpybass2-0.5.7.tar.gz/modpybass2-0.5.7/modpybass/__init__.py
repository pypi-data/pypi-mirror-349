__version__ = '0.5.6'
__author__ = 'Johann M. Kammiste'
__email__ = 'peppy0510@hotmail.com'
__license__ = 'BSD'
__doc__ = '''
bass_module, func_type = bass.load(__file__)
'''


TRIAL_MODULES = [
    'pybass',
    'pybass_vst',
    'pybass_aac',
    'pybass_ac3',
    'pybass_adx',
    'pybass_aix',
    'pybass_alac',
    'pybass_ape',
    'pybass_mpc',
    'pybass_ofr',
    'pybass_sfx',
    'pybass_spx',
    'pybass_tta',
    'pybass_vst',
    'pybassasio',
    'pybassflac',
    'pybassmidi',
    'pybassmix',
    'pybasswasapi',
    'pybasswma',
    'pyogginfo',
    'pytags',
]


IMPORTED_MODULES = []


for name in TRIAL_MODULES:
    try:
        try:
            exec('from %s import *' % (name))
        except ImportError:
            exec('from .%s import *' % (name))
        IMPORTED_MODULES += [name]
    except Exception:
        pass


if __name__ == '__main__':
    print(IMPORTED_MODULES)
    # print(list(globals()))
