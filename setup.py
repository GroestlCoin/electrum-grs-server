from setuptools import setup

setup(
    name="electrum-grs-server",
    version="1.0",
    scripts=['run_electrum_grs_server.py','electrum-grs-server'],
    install_requires=['plyvel','jsonrpclib', 'irc==13.3.1', 'groestlcoin_hash'],
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
    ],
    description="Bitcoin Electrum Server",
    author="Thomas Voegtlin",
    author_email="thomasv@electrum.org",
    license="MIT Licence",
    url="https://github.com/spesmilo/electrum-server/",
    long_description="""Server for the Electrum Lightweight Bitcoin Wallet"""
)
