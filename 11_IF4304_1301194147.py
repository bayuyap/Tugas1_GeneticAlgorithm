import random as rnd
from math import *

NPOP = 50
LKROM = 10
PM = 0.05
PC = 0.8
NGEN = 50
nTitikPotong = 2

class cromosome :
  def __init__(self, bit):
    self.geno = bit
    x, y = self.getFeno()
    self.fit = self.fitness(x, y)


  def getFeno(self):
    n = LKROM // 2
    x = self.decode(self.geno[:n], -1, 2)
    y = self.decode(self.geno[n:], -1, 1)
    return x, y


  def decode(self, gen, rb, ra):
    down = sum([2**-(i+1) for i in range(len(gen))])
    up = sum([gen[i]*(2**-(i+1)) for i in range(len(gen))])
    return rb + ((ra -rb)*up/down)


  def h(self, x, y):
    return cos(x*x) * sin(y*y) + (x + y)

  def fitness(self, x, y):
    return self.h(x, y)

def GeneratePopulation():
  pop = []
  while len(pop) < NGEN:
    p = rnd.choices([0,1], k=LKROM)
    if p not in pop:
      pop.append(p)

  population = []
  for p in pop:
    population.append(cromosome(p))
  return population


def popToFitPop(pop):
  fPop = []
  for p in pop:
    fPop.append(p.fit)
  return fPop

def seleksiOrtu(population):
  #mengambil semua nilai fitness
  popFit = popToFitPop(population)
  all = sum(popFit)
  fit = [(sum(popFit[:i+1])/all) * 10 for i in range(len(popFit))]

  # Metode seleksi roullete wheel
  parentIdx = []
  n = NGEN // 2
  while len(parentIdx) < n:

    x = rnd.uniform(0, 10)
    idx = -1

    for i in range(len(fit)):
      if x <= fit[i]:
        idx = i
        break

    if not (idx in parentIdx):
      parentIdx.append(idx)

  parent = []
  for pi in parentIdx:
    parent.append(population[pi].geno)
  return parent


def binerDoublePoint(kromosom1, kromosom2):
  if rnd.uniform(0, 1) > PC :
    return [list(kromosom1), list(kromosom2)]
  # Ambil sembarang titik sebanyak 2 titik potong
  points = []
  while(len(points) < nTitikPotong):
    x = rnd.randint(1, len(kromosom1)-1)
    if not (x in points):
      points.append(x)
  points.sort()

  child1 = []
  child2 = []
  last = 0
  for i in range(nTitikPotong):
    p = points[i]
    if i % 2 == 0:
      child1.extend(kromosom2[last:p])
      child2.extend(kromosom1[last:p])
    else:
      child1.extend(kromosom1[last:p])
      child2.extend(kromosom2[last:p])
    last = p
  if nTitikPotong % 2 == 0:
    child1.extend(kromosom2[last:])
    child2.extend(kromosom1[last:])
  else:
    child1.extend(kromosom1[last:])
    child2.extend(kromosom2[last:])
  return child1, child2

def rekombinasi(parentBit):
  childBit = []
  for i in range(len(parentBit)-1):
    # Pencarian pasangan untuk orang tua secara acak
    cp = i
    while cp == i:
      cp = rnd.randint(0, len(parentBit) - 1)
    # rekombinasi dan generate generasi baru
    childBit.extend(binerDoublePoint(parentBit[i], parentBit[cp]))

  return childBit


def mutasi(k):
  for i in range(len(k)):
    if(rnd.uniform(0,1) < PM):
      k[i] = (k[i] + 1) % 2
  return k


def mutasiChild(childBits):
  child = []
  for cb in childBits:
    child.append(cromosome(mutasi(cb)))
  return child

# Seleksi Survivor
def selection(population, child):
  population.extend(child)
  population.sort(key=lambda cromosome : cromosome.fit, reverse=True)
  for i in range(len(child)):
    population.pop()
  return population


population = GeneratePopulation()
for i in range(NGEN):
  parentBit = seleksiOrtu(population)
  childBit = rekombinasi(parentBit)
  child = mutasiChild(childBit)
  population = selection(population, child)
  x, y = population[0].getFeno()
  print('Generasi ke - {} , Best x : {} Best y : {}, Kromosom Terbaik: {}'.format(i+1, x, y, population[0].fit))

#Mengambil kromosom terbaik dari generasi terakhir
#output berupa Best individu x, Best Individu y dan Kromosom Terbaik
x, y = population[0].getFeno()
print('Best x : {} Best y : {}'.format(x, y))
print('Kromosom Terbaik : {}'.format(population[0].h(x, y)))