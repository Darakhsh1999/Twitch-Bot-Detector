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
    SBR = (30.0/20.0)*(len(T)/time[-1]) # Shadow Ban Ratio (20 msg per 30s)

    _min = T.min()
    _max = T.max()
    mu = T.mean()
    std = T.std()
    mu_Q = T_Q.mean()
    std_Q = T_Q.std()
    
    print(f"SBR = {SBR:.3f}")

    # Running average 
    plt.subplot(2, 1, 1)
    moving_mean = np.array(pd.DataFrame(T).rolling(config.window_size).mean())
    plt.plot(minutes, moving_mean, label=f"Moving mean (W={config.window_size})")
    plt.fill_between(minutes, mu-std, mu+std, alpha=0.3, label=f"$\sigma = {std:.3f}$")
    plt.hlines(mu, xmin=minutes[0], xmax=minutes[-1], colors="black", linestyles="dashed", label=f"$\mu = {mu:.3f}$")
    plt.grid()
    plt.legend(loc="upper left", frameon=True)
    plt.xlabel("time t [min]")
    plt.ylabel("Delta $\Delta T$ [s]")
    plt.title(f'Moving mean (N={len(T)}), $\Delta_1$ = {_min:.2f}, $\Delta_2$ = {_max:.2f}')

    # Raw histogram
    plt.subplot(2, 2, 3)
    plt.hist(T, bins=50, density=True)
    plt.vlines(mu_Q*np.arange(1,5), ymin=0, ymax=1, colors="black", linestyles="dashed", label=f"$\mu_Q$")
    plt.title(f"$\mu$ = {mu:.3f}, $\sigma$ = {std:.3f}")
        
    # Quantile histogram
    plt.subplot(2, 2, 4)
    plt.hist(T_Q, bins=50, density=True)
    plt.title(f"$\mu_Q$ = {mu_Q:.3f}, $\sigma_Q$ = {std_Q:.3f}")
        

    plt.show()


if __name__ == "__main__":

    from params import CONST
    config = CONST()
    time_statistics(1.5+np.random.randn(1000), config)
