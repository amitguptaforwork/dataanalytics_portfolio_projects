import numpy as np
import matplotlib.pyplot as plt

# Constraint lines
x = np.linspace(0, 6, 400)
y1 = 10 - 2*x        # Machine
y2 = (12 - x) / 3   # Labor

# Feasible region
y = np.minimum(y1, y2)
y[y < 0] = 0


# Optimal point (from solver)
x_opt, y_opt = 3.6, 2.8

plt.figure()
plt.plot(x, y1, label="2x + y ≤ 10")
plt.plot(x, y2, label="x + 3y ≤ 12")
plt.fill_between(x, 0, y, alpha=0.3)

plt.scatter(x_opt, y_opt)
plt.text(x_opt + 0.1, y_opt, "Optimal Solution")

plt.xlabel("Product A")
plt.ylabel("Product B")
plt.legend()
plt.title("Feasible Region and Optimal Solution")
plt.show()