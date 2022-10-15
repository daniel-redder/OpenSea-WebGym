from pettingzoo.test import performance_benchmark
from pettingzoo.butterfly import pistonball_v6
env = pistonball_v6.env()
performance_benchmark(env)