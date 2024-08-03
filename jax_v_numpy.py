import jax.numpy as jnp
import numpy as np
import jax

case = 'JAX'
def my_dot(x,y):

    if case == 'JAX':
        val = jnp.dot(x, y)
    else:
        val = np.dot(x, y)

    return val

jmd = jax.jit(my_dot)

print(jmd(np.array([1, 2, 3]), np.array([4,])))
