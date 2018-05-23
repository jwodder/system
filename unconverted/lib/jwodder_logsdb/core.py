from   pathlib import Path
import sqlalchemy as S

JWODDER_ROOT = Path(__file__).parents[2]

def connect() -> 'Engine':
    dbpass = (JWODDER_ROOT/'etc'/'logger').read_text().strip()
    return S.create_engine(S.engine.url.URL(
        drivername = 'postgresql',
        host       = 'localhost',
        database   = 'logs',
        username   = 'logger',
        password   = dbpass,
    ))

def longint(n):
    n = str(n)
    nl = len(n)
    triples = [n[i:i+3] for i in range(nl % 3, nl, 3)]
    if nl % 3:
        triples = [n[:nl%3]] + triples
    return ' '.join(triples)
