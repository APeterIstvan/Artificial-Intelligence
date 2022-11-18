import random
from cooling_strategies import *

def probability(t_star, f_st, temp):
  expon = (t_star - f_st) / temp
  return math.exp(-expon)


def object_function(jobs, order, jobs_num, machines_num):
  job_begin = [[0 for x in range(jobs_num)] for y in range(machines_num)]  # stores the starting points of the jobs
  job_end = [[0 for x in range(jobs_num)] for y in range(machines_num)]  # stores the end points of the jobs
  cost = [0 for i in range(jobs_num)]  #
  for i in range(0, machines_num):
    for j in range(0, jobs_num):
      c_max = cost[j]
      if j > 0:
        c_max = max(cost[j - 1], cost[j])
      cost[j] = c_max + jobs[order[j] - 1][i]
      job_end[i][j] = cost[j]
      job_begin[i][j] = job_end[i][j] - jobs[order[j] - 1][i]
      c_max = job_end[i][j]

  return {"c_max": c_max, "job_begin": job_begin, "job_end": job_end}


def simulated_annealing(jobs, s, object_f, iterations, neighbors, t0, jobs_num, machines_num, cooling_strategy):
  try:
    s_best = list(s)  # stores the best order of jobs
    f_best = object_f(jobs, s_best, jobs_num, machines_num)['c_max']  # stores the best Cmax
    s_base = list(s_best)
    f_base = f_best
    t = 0  # represents time
    alpha = 0.8  # alpha (should be between 0.8 - 0.9)
    for i in range(iterations):
      s_best_neighbor = list(s_base)
      f_best_neighbor = f_base
      for j in range(neighbors):
        t += 1
        s_neighbor = list(s_base)
        a = random.randint(0, len(s) - 1)
        b = random.randint(0, len(s) - 1)
        s_neighbor[a], s_neighbor[b] = s_neighbor[b], s_neighbor[a]
        f_neighbor = object_f(jobs, s_neighbor, jobs_num, machines_num)['c_max']

        # -- START SIMULATED ANNEALING --
        if f_neighbor < f_best_neighbor:
          f_best_neighbor = f_neighbor
          s_best_neighbor = s_neighbor
        else:
          temp = choose_cooling_strategy(cooling_strategy, f_best_neighbor, f_neighbor, t0, alpha, t)
          prob = probability(f_best_neighbor, f_neighbor, temp)
          randProb = random.randint(0, 98)
          if randProb < prob * 100:
            f_best_neighbor = f_neighbor
            s_best_neighbor = s_neighbor
        # -- END SIMULATED ANNEALING --
      s_base = s_best_neighbor
      f_base = f_best_neighbor
      if f_base < f_best:
        f_best = f_base
        s_best = s_base
  except(OverflowError):
    print(f"\n!!! Overflow Error - Exited at: {t}/{iterations * neighbors} !!!")
  return s_best
