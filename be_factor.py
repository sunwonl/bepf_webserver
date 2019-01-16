import math


def line(ix, iy):
    l = lambda x, y: x / ix + y / iy

    return l


def compute_ccei(p1, p2):
    ccei1 = line(p1['ix'], p2['iy'])(p2['x'], p2['y'])
    ccei2 = line(p2['ix'], p2['iy'])(p1['x'], p1['y'])

    if (ccei1 >= 1) or (ccei2 >= 1):
        return 1
    else:
        return max(ccei1, ccei2)


def crra_portfolio_func(x_data, alpha, rho, omega):
    def f(ix, iy):
        v = math.log(iy/ix)
        log_alpha = math.log(alpha)
        log_omega = math.log(omega)
        if v >= (log_alpha - rho*log_omega):
            return log_omega
        elif log_alpha < v < (log_alpha - rho*log_omega):
            return (-1/rho) * (v-log_alpha)
        elif (-1 * log_alpha) <= v < log_alpha:
            return 0
        elif (-1 * log_alpha + rho * log_omega) <= v < (-1 * log_alpha):
            return (-1/rho) * (v-log_alpha)
        else:
            return -1 * log_omega
    ix, iy = x_data
    return f(ix, iy)


def cara_portfolio_func(x_data, alpha, A):
    def f(ix, iy):
        v = math.log(iy/ix)
        log_alpha = math.log(alpha)
        if v >= log_alpha + A * iy:
            return iy
        elif log_alpha < v < (log_alpha + A * iy):
            return (1/A) * (v - log_alpha)
        elif (-1 * log_alpha) <= v <= log_alpha:
            return 0
        elif (-1 * log_alpha + A * ix) < v < (-1 * log_alpha):
            return (1/A) * (v + log_alpha)
        else:
            return -1 * ix

    ix, iy = x_data
    return f(ix, iy)


def objective_crra(portfolio, budgets, alpha, rho, omega):
    sse = 0
    f = crra_portfolio_func(alpha=alpha, rho=rho, omega=omega)
    for i in range(len(portfolio)):
        x, y = portfolio[i]
        ix, iy = budgets[i]
        sse += (math.log(x/y) - f(ix, iy)) ** 2

    return sse


def objective_cara(portfolio, budgets, alpha, A):
    sse = 0
    f = cara_portfolio_func(alpha=alpha, A=A)
    for i in range(len(portfolio)):
        x, y = portfolio[i]
        ix, iy = budgets[i]
        sse += ((y-x) - f(ix=ix, iy=iy)) ** 2
    return sse


def gradient_crra_portfolio_func(alpha, rho, omega):
    def f_prime(ix, iy):
        v = math.log(iy / ix)
        log_alpha = math.log(alpha)
        log_omega = math.log(omega)
        if v >= (log_alpha - rho * log_omega):
            return 0, 0, 1/omega
        elif log_alpha < v < (log_alpha - rho * log_omega):
            return 1 / (alpha * rho), 1 / (rho**2) * v, 0
        elif (-1 * log_alpha) <= v < log_alpha:
            return 0, 0, 0
        elif (-1 * log_alpha + rho * log_omega) <= v < (-1 * log_alpha):
            return -1 / (alpha * rho), 1 / (rho**2) * v, 0
        else:
            return 0, 0, -1/omega

    return f_prime


def get_be_profile(portfolio, budgets, utility='crra'):
    from scipy import optimize
    if utility == 'crra':
        func = crra_portfolio_func
    elif utility == 'cara':
        func = cara_portfolio_func
    else:
        print('invliad utility function')
        return None

    params, params_covariance = optimize.curve_fit(f=func,
                                                   xdata=budgets,
                                                   ydata=portfolio)

    print(params)

    return params
