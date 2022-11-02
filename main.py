from pettingzoo.test import api_test 
from app.domains.shipping_fo import raw_env as shipping_fo

env = shipping_fo(10)
api_test(env, num_cycles=100, verbose_progress=False)