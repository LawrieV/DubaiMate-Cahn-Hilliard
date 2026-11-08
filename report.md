Group report 

# Cahn-Hilliard model

Describe the task in your own words, and/or link to the task description. 

The Cahn-Hilliard model is a model, which describes the process of phase separation in binary mixtures.
Its main idea is that a material will not separate instantly, but small composition fluctuations will grow that produce domains which grow larger. This idea is important in material science as it can influence microstructure, mechanical properties as well as phase stability.

All in all this model was divided into four tasks with the first one simulating phase separation and then in the second checking if the simulation obeys mass conservation and free energy disipation.
In the third task the domain growth was measured by quantifying how the characteristic size of the separated domoains increase over time. Lastly in the fourth task five different energy models were investigated to see how free energy functions influence phase separation and its resulting structure.

## Layout of the algorithm, functions to be created

Name the most important functions and mention their functionality, i.e., input and output.

In the first task as well in the tasks that follow one of the most important function was the "advance" function. As this was always used to calculate the concentration field in tasks 1 and 4. It calculates the chemical potential by the given formula and  given concentration and returns the concentration + delta t times mobility and times the laplacian of the chemical potential.

def advance(concentration):
    """Calculate the concentration field one time step later."""
    chemical_potential = (
        concentration**3 - concentration
        - kappa * laplacian(concentration)
    )
    return concentration + deltat * mobility * laplacian(chemical_potential)

## How to run the code

Each task can be run in the following files by using the run button in vs code:

- Task 1:
    - *plotConcSnapshots.py*
- Task 2:
    - *task2.py*
- Task 3:
    - *task3.py*
- Task 4:
    - Asymmetric double well: *AsymmDoubleWell.py*
    - Flory-Huggins free energy for polymers: *FloryHuggins.py*
    - Triple-well potential: *TripleWellPotential.py*
    - Non-convex + external field: *NonConvex.py*
    - Periodic free energy: *PeriodicFreeEnergy.py*

In each file the parameters for the creation of the concentration field can be changed seperately



## Resulting files

Mention any resulting files and their format and meaning. 

## Successful tests

Summarize, which tests have been successfully passed to test your code. 

## Problems

The first problem we ran into, was that our code was very slow going through all 10000 time steps in *Task1\calculateConc.py*. We identified the main source of slowing the code down was the *laplacian()* function. Since for each step it checks all neighbours in a easy, but sadly rather time-consuming way. So the *laplacian()* function was rewritten with the np.roll(a, shift, axis). Here, a is the input array, shift is the amount by which the element is shifted, and axis is the axis along which the element should be shifted. This helped reduce the time it took to calculate the concentration changes by a huge amount.

In task 2 we ran into no problems.

When writing the code for task 3, our first challenge was actually understanding how to implement what is asked of us. For this, we first tried to understand every aspect of the theory behind the task, i.e. understanding how we can go from the fourier transformed concentration field to the *k~MAX~*. This took quite a while to figure out, but eventually we did. Then it was much easier to also implement the task into python code. The next problem we had was that it took too long to compute the charcteristic lengthscale for t>100. Here we managed to cut down the time slightly by removing unnecessary calls of certain functions that we overlooked. A third problem was finding the values for *A* and *alpha*. This was becasue our *L(t)*  function just consited mostly of plateaus, making it hard to fit a linear plot to them. Increasing the size of the grid to $N=256$ din't halp either.

For task four the different subtasks were divided in the group, where first a general code was created for the Asymmetric double well, which was then used for the other codes and slightly altered. Most of the subtasks went smoothly and there was no bigger problem except with the triple well potential. Here one of the main problems that arose were the results themselves. The graph that was created after 10000 steps always turned out to be completely white and never either red or blue, which suggested that some of the code might be faulty. After checking the math and the code with the professor it was tested if a different concentration distribution would change the graphs colors. This turned out to be true as changing the parameter to smaller distributions resulted in the graph after 10000 steps being mostly red or blue depending on the concentration region.

## Results (speed tests etc.)

### Task 1:

Following the steps in the task and using the double-well free energy function

$$f(c)=(c^2-1)^2/4$$

The simulations use $N=128$, $mobility=1$, $\kappa=1$, $\Delta t=0.01$, and the same reproducible random initial field uniformly distributed between $-1$ and $1$. We simulated the change of the concentration profile, here at timestep 0, 2500, 5000, 7500 and 10000:

![Concentration at timestep 0](Task1/Snapshots/conc_snapshot_0.png)
![Concentration at timestep 2500](Task1/Snapshots/conc_snapshot_2500.png)
![Concentration at timestep 5000](Task1/Snapshots/conc_snapshot_5000.png)
![Concentration at timestep 7500](Task1/Snapshots/conc_snapshot_7500.png)
![Concentration at timestep 10000](Task1/Snapshots/conc_snapshot_10000.png)

This makes sense, since the function $f(c)$ has two wells, at $c=-1$ and $c=1$, so the random concentration field separates into these two wells over time.



### Task 2:

For Task we plotted the total mass versus time and also the free energy versus time:

![Mass conservation and Energy dissipation](Task2/images/task2-mass-energy.png)

Here we can show that we have mass conservation, which makes sense, since we only "move concentration/mass around" and shouldn't lose any. Also we see that the total free energy of the system decreases. Again this makes sense, since a system always tries to reduce its free energy and, as seen in task 1, this is done by separating the materials into the two concentration wells.



### Task 3:

In task 3 we calculated the charcteristic length scale $L(t)$ present in the formed pattern. This was done over the calculation of the isotropic structure factor, from which we could extract the maximal wavenumber $k_\textrm{max}(t)$ in the course of time, giving us $L(t)$.

We took all the same parameters as in task 1, except that we chose $N=256$, and that we evaluated the charcteristic length scale at large time scales ($t>>100$). Plotting $L(t)$ against time gave us the following plot:

![Charcteristic length scale vs Time](Task3/Images/characteristic_length_vs_time.png)

In the figure one can also see a fitted curve. This gave us the growth exponent $\alpha=0.317$ and the prefactor $A=3.69$. Its hard to say if these are good results, since the charcteristic length scale constantly plateaus.



### Task 4:

#### Non convex + external field
Starting from random noise in [-1, 1], all simulations undergo spinodal decomposition within 10,000 time steps. The field separates into domains of the two phases c ≈ +1 and c ≈ −1, and the mean concentration is conserved (⟨c⟩ ≈ 0.003). The domains are still coarsening at the final step, so equilibrium has not been reached.

For H = 0, the microstructure is statistically isotropic. For H > 0, the linear term in the chemical potential favors the c = +1 phase on the left (small x) and the c = −1 phase on the right (large x). This bias grows with H. The mean concentration in the leftmost / rightmost 32 columns is 0.09 / −0.07 for H = 0.1, 0.17 / −0.15 for H = 0.25, 0.24 / −0.21 for H = 0.5, and 0.33 / −0.31 for H = 1.0, compared to 0.03 / −0.01 at H = 0. The field extremes also shift beyond ±1 (about ±1.14 for H = 1.0, versus ±1.03 for H = 0).

Overall, a weak linear field does not suppress phase separation but biases it spatially, and the asymmetry increases roughly linearly with H in the range studied.

Falls du die Colorbar vmin=-3.5 nicht bewusst gewählt hast: Die Werte liegen nur in etwa [-1.14, 1.04], die Bilder wirken dadurch kontrastarm.

#### Periodic free energy
With the periodic free-energy derivative f′(c) = sin(c), no phase separation occurs. The free-energy curvature f″(c) = cos(c) is positive for all |c| < π/2. The initial noise in [-1, 1] lies entirely in this stable region, so the dynamics are purely diffusive and the field relaxes toward the uniform state. The mean concentration is conserved (⟨c⟩ = 0.0034), while the standard deviation falls from 0.58 initially to 0.045 after 500 steps and 0.013 after 10,000 steps. At the final step, all values lie within [-0.022, 0.031], so the snapshot is essentially homogeneous. The decay continues without saturating, as the remaining fluctuations are smoothed out. Spinodal decomposition would require initial values with |c| > π/2 ≈ 1.57, where cos(c) < 0.


#### Asymmetric double well

We used the free-energy density

$f(c)=\frac{(c^2-1)^2}{4}+\alpha*c^3 c,$$

whose derivative is $f'(c)=c^3-c+3*\alpha*c^2$. The simulations use $N=128$, $mobility=1$, $\kappa=1$, $\Delta t=0.01$, and the same reproducible random initial field uniformly distributed between $-3.5$ and $1$ for each parameter value. We compared $\alpha=0$, $\alpha=0.1$, $\alpha=0.25$, $\alpha=0.5$, and $\alpha=1$ through 10,000 time steps.

##### $\alpha=0$:

![Initial concentration, alpha=0](Task4/Snapshots/AsymmDoubleWell/alpha_0/conc_snapshot_0.png)
![Final concentration, alpha=0](Task4/Snapshots/AsymmDoubleWell/alpha_0/conc_snapshot_10000.png)

##### $\alpha=0.1$:

![Initial concentration, alpha=0](Task4/Snapshots/AsymmDoubleWell/alpha_0.1/conc_snapshot_0.png)
![Final concentration, alpha=0](Task4/Snapshots/AsymmDoubleWell/alpha_0.1/conc_snapshot_10000.png)

##### $\alpha=0.25$:

![Initial concentration, alpha=0](Task4/Snapshots/AsymmDoubleWell/alpha_0.25/conc_snapshot_0.png)
![Final concentration, alpha=0](Task4/Snapshots/AsymmDoubleWell/alpha_0.25/conc_snapshot_10000.png)

##### $\alpha=0.5$:

![Initial concentration, alpha=0.5](Task4/Snapshots/AsymmDoubleWell/alpha_0.5/conc_snapshot_0.png)
![Final concentration, alpha=0.5](Task4/Snapshots/AsymmDoubleWell/alpha_0.5/conc_snapshot_10000.png)

##### $\alpha=1$:

![Initial concentration, alpha=1](Task4/Snapshots/AsymmDoubleWell/alpha_1/conc_snapshot_0.png)
![Final concentration, alpha=1](Task4/Snapshots/AsymmDoubleWell/alpha_1/conc_snapshot_10000.png)

When comparing the concentration patterns for different $\alpha$ with the functions as seen in the following figure, one can see that the concentration splits into two wells, that are given by the minima of the functions.

![Plots of function of all alpha](Task4/Snapshots/AsymmDoubleWell/plots.png)

The only result where we arent too sure what is happening is the one for $\alpha=1$. Since in the concentration snapshot after 10000 timesteps it looks like that a lot of the concentration is at $c=1$, which wouldnt be correct, since the function has non minima there.

#### Flory Huggins free energy for polymers

For this task we used the function: 

$$f(c) = c \ln(c) + (1-c)\ln(1-c) + \chi c(1-c)$$

which has $\chi=2.5$ as a parameter. The derivative of this function turned out to be: $f'(c)=\log(c) - \log(1 - c) + \chi*(1 - 2*c)$. The simulations were done with 0 and 10000 steps. The random concentration distribution to initiate the simulation was set between $0.45$ to $0.55$. This is due to the fact that we didn't want the concentration value to leave the range of $0$ to $1$, otherwise the logarithms would be undefined. The resulting initial and final concentration was:

![Initial concentration, chi=2.5](Task4/Snapshots/FloryHuggins/alpha_2.5/conc_snapshot_0.png)
![Final concentration, chi=2.5](Task4/Snapshots/FloryHuggins/alpha_2.5/conc_snapshot_10000.png)

This fits, as the function has a double well structure with minima at a relative concentration of around $0.14$ and $0.86$


#### Triple well potential

For this task we used the function: 

$$f(c)=(c+1)^2 c^2(c-1)^2$$

which does not have a parameter. The derivative of this function turned out to be: $f'(c)=6c^5 - 8c^3 + 2c $. The simulations were done with 0 and 10000 steps. In total three simulations were done. The first one keeping the random concentration distribution in the range of $-1.5$ to $1.5$ as used in other examples. The second simulation uses a distribution between $-0.55$ to $-0.45$ and the last simulation was between $0.45$ to $0.55$.

##### Distribution between -1.5 to 1.5:

![Distribution between -1.5 to 1.5, for 0 steps](Task4/Snapshots/TripleWellPotential/conc_snapshot_0.png)
![Distribution between -1.5 to 1.5, for 10000 steps](Task4/Snapshots/TripleWellPotential/conc_snapshot_10000.png)

##### Distribution between -0.55 to -0.45:

![Distribution between -0.55 to -0.45, for 0 steps](Task4/Snapshots/TripleWellPotential/conc_snapshot_between-0.55to-0.450.png)
![Distribution between -1.5 to 1.5, for 10000 steps](Task4/Snapshots/TripleWellPotential/conc_snapshot_between-0.55to-0.4510000.png)

##### Distribution between 0.45 to 0.55:

![Distribution between 0.45 to 0.55, for 0 steps](Task4/Snapshots/TripleWellPotential/conc_snapshot_between0.55to0.450.png)
![Distribution between 0.45 to 0.55, for 10000 steps](Task4/Snapshots/TripleWellPotential/conc_snapshot_between0.55to0.4510000.png)


It is visible that for the smaller concentrations in either the positive or negative regime it concentrates into either only red and white or only blue and white. This makes it evident that there should be three wells within the system but also with the example of the distribution from -1.5 to 1.5 we see that the well of the white distribution has to be the global minimum as it always turns white with a bigger distribution.


#### Non-convex + external field




#### Periodic free energy


