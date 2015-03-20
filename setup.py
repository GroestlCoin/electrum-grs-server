from setuptools import setup

setup(
    name="electrum-grs-server",
    version="0.9",
    scripts=['run_electrum_server','electrum-server'],
    install_requires=['plyvel','jsonrpclib', 'irc>=11', 'groestlcoin_hash'],
    dependency_links=['git+https://github.com/groestlcoin/groestlcoin-hash-python#egg=groestlcoin_hash'],
    package_dir={
        'electrumgrsserver':'src'
        },
    py_modules=[
        'electrumgrsserver.__init__',
        'electrumgrsserver.utils',
        'electrumgrsserver.storage',
        'electrumgrsserver.deserialize',
        'electrumgrsserver.networks',
        'electrumgrsserver.blockchain_processor',
        'electrumgrsserver.server_processor',
        'electrumgrsserver.processor',
        'electrumgrsserver.version',
        'electrumgrsserver.ircthread',
        'electrumgrsserver.stratum_tcp',
        'electrumgrsserver.stratum_http'
    ],
    description="Bitcoin Electrum Server",
    author="Thomas Voegtlin",
    author_email="thomasv1@gmx.de",
    license="GNU Affero GPLv3",
    url="https://github.com/spesmilo/electrum-server/",
    long_description="""Server for the Electrum Lightweight Bitcoin Wallet"""
)


