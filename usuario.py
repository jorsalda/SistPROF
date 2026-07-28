import time

t0 = time.time()
from app.models import usuario
print(f'usuario: {time.time()-t0:.2f}s')

t0 = time.time()
from app.models import docente
print(f'docente: {time.time()-t0:.2f}s')

t0 = time.time()
from app.models import estudiante
print(f'estudiante: {time.time()-t0:.2f}s')
