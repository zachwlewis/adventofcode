import sys, math

if len(sys.argv) > 1:
  times = int(sys.argv[1])
  for x in range(times):
    u = (math.cos(2 * math.pi / times * x) + 1) * 0.5
    v = (math.sin(2 * math.pi / times * x) + 1) * 0.5
    print(f"{u},\n{v},")