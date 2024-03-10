import time
import looping
import looping_cy


start_py = time.time()
looping.marching(600, 600, 512)
end_py = time.time()
print(end_py - start_py)

start_c = time.time()
looping_cy.marching(600, 600, 512)
end_c = time.time()
print(end_c - start_c)