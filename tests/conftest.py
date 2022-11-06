import betamax
import os

if not os.path.exists('tests/cassettes'):
    os.makedirs('tests/cassettes')

with betamax.Betamax.configure() as config:
    config.cassette_library_dir = 'tests/cassettes/'