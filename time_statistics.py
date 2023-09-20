import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def time_statistics(T: list, config):
    
    T: np.ndarray = np.array(T)
    time = np.cumsum(T)
    minutes = time / 60.0
    Q_L = np.quantile(T, 0.05)
    Q_U = np.quantile(T, 1-0.05)
    T_Q = T[np.logical_and((Q_L < T), (T < Q_U))]

    _min = T.min()
    _max = T.max()
    _min_Q = T_Q.min()
    _max_Q = T_Q.max()
    mu = T.mean()
    std = T.std()
    mu_Q = T_Q.mean()
    std_Q = T_Q.std()


    # Running average 
    plt.subplot(2, 1, 1)
    moving_mean = np.array(pd.DataFrame(T).rolling(config.window_size).mean())
    plt.plot(minutes, moving_mean)
    plt.grid()
    plt.xlabel("time t [min]")
    plt.ylabel("Delta $\Delta T$ [s]")
    plt.title("Moving mean")

    # Raw histogram
    plt.subplot(2, 2, 3)
    plt.hist(T, density=True)
    plt.title(f"$\mu$ = {mu:.3f}, $\sigma$ = {std:.3f}")
        
    # Quantile histogram
    plt.subplot(2, 2, 4)
    plt.hist(T_Q, density=True)
    plt.title(f"$\mu$ = {mu_Q:.3f}, $\sigma$ = {std_Q:.3f}")
        





    plt.show()


if __name__ == "__main__":

    from params import CONST
    config = CONST()
    time_statistics(1.5+np.random.randn(1000), config)
