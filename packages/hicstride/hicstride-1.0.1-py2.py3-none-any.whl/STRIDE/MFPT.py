import os, sys
import numpy as np
from numpy import matlib, linalg
from collections import Counter
from scipy import optimize
import pandas as pd
import importlib

__config__ = {
    "min_coverage": 0.02,
    "KR_tol": 1e-12,
    "device": "cpu",
    "norm": "fro"
}


def mask_low_coverage(M, min_coverage=0.02):
    M = M - np.diag(np.diag(M))
    s = M.sum(axis=0)
    q = np.quantile(s[s > 0], min_coverage)
    flag = s > q
    return flag


def get_largest_compnoent(cm: np.array,
                          pre_masked=None,
                          return_indicator=False) -> list:
    cm = cm - np.diag(np.diag(cm))
    ligal = np.ones(cm.shape[0], dtype=bool)
    if pre_masked is None:
        pre_masked = np.ones(cm.shape[0], dtype=bool)
    ligal = ligal & pre_masked

    def get_components(root):
        visited = set()
        to_be_continue = [root]
        while to_be_continue:
            visited.update(to_be_continue)
            next_layer = set()
            for l in map(lambda i: (np.where((cm[i, :] > 0) & ligal)[0]),
                         to_be_continue):
                next_layer.update(l)
            to_be_continue = [i for i in next_layer if not i in visited]
        return list(visited)

    un_used = -np.ones(cm.shape[0], dtype=np.int64)
    un_used[ligal] = 0
    ix = 1
    while any(un_used == 0):
        v = get_components(np.where(un_used == 0)[0][0])
        un_used[v] = ix
        ix += 1
    vmax = max(list(Counter(un_used[un_used > 0]).items()),
               key=lambda v: v[1])[0]
    if return_indicator:
        return un_used == vmax
    else:
        flag = (un_used == vmax)
        return cm[flag, :][:, flag], flag


def KRNorm(A, tol=1e-8, f1=False):
    A = A - np.diag(np.diag(A))
    n = A.shape[0]
    e = np.ones((n, 1), dtype=np.float64)
    res = []
    Delta = 3
    delta = 0.1
    x0 = np.copy(e)
    g = 0.9
    etamax = eta = 0.1
    stop_tol = tol * 0.5
    x = np.copy(x0)
    rt = tol**2.0
    v = x * (A.dot(x))
    rk = 1.0 - v
    rho_km1 = ((rk.transpose()).dot(rk))[0, 0]
    rho_km2 = rho_km1
    rout = rold = rho_km1
    MVP = 0
    i = 0
    while rout > rt:
        i += 1
        if i > 30000:
            break
        k = 0
        y = np.copy(e)
        innertol = max(eta**2.0 * rout, rt)
        while rho_km1 > innertol:
            k += 1
            if k == 1:
                Z = rk / v
                p = np.copy(Z)
                rho_km1 = (rk.transpose()).dot(Z)
            else:
                beta = rho_km1 / rho_km2
                p = Z + beta * p
            if k > 10:
                break
            w = x * A.dot(x * p) + v * p
            alpha = rho_km1 / (((p.transpose()).dot(w))[0, 0])
            ap = alpha * p
            ynew = y + ap
            if np.amin(ynew) <= delta:
                if delta == 0:
                    break
                ind = np.where(ap < 0.0)[0]
                gamma = np.amin((delta - y[ind]) / ap[ind])
                y += gamma * ap
                break
            if np.amax(ynew) >= Delta:
                ind = np.where(ynew > Delta)[0]
                gamma = np.amin((Delta - y[ind]) / ap[ind])
                y += gamma * ap
                break
            y = np.copy(ynew)
            rk -= alpha * w
            rho_km2 = rho_km1
            Z = rk / v
            rho_km1 = ((rk.transpose()).dot(Z))[0, 0]
        x *= y
        v = x * (A.dot(x))
        rk = 1.0 - v
        rho_km1 = ((rk.transpose()).dot(rk))[0, 0]
        rout = rho_km1
        MVP += k + 1
        rat = rout / rold
        rold = rout
        res_norm = rout**0.5
        eta_o = eta
        eta = g * rat
        if g * eta_o**2.0 > 0.1:
            eta = max(eta, g * eta_o**2.0)
        eta = max(min(eta, etamax), stop_tol / res_norm)
        if f1:
            res.append(res_norm)
    Y = A * (x * x.T)
    m = Y.sum(axis=0).max()
    Y = Y / m
    d = 1 - Y.sum(axis=0)
    N = Y.shape[0]
    Y = Y.flatten()
    Y[0:N**2:N + 1] = d
    return Y.reshape((N, N))


try:
    torch = importlib.import_module("torch")

    def get_mfpt(P):
        if not isinstance(P, torch.Tensor):
            P = torch.tensor(P,
                             dtype=torch.float64,
                             device=__config__["device"])
        m = P.shape[0]
        I = torch.eye(m, dtype=torch.float64, device=__config__["device"])
        K = torch.eye(m, dtype=torch.float64, device=__config__["device"])
        for i in range(m):
            pit = P[[i], :]
            bit = pit - torch.ones(
                [1, m], dtype=torch.float64, device=__config__["device"]) / m
            ki = 1 - bit.mm(K[:, [i]])
            CI = bit.mm(K) / ki
            K = K + K[:, [i]] * (CI)
            pct = int(i / m * 100)
            p_bar = "+" * pct + "-" * (100 - pct)
        M = (I - K + torch.diag(K).repeat(m, 1))
        return M.cpu().numpy()

    def get_mfpt_large_mem(P):
        P = torch.tensor(P, dtype=torch.float64, device=__config__["device"])
        Z = torch.eye(P.shape[0],
                      device=__config__["device"]) - P + torch.ones(
                          P.shape, device=__config__["device"]) / P.shape[0]
        Z = torch.linalg.inv(Z)
        M = torch.eye(Z.shape[0],
                      device=__config__["device"]) - Z + torch.diag(Z).repeat(
                          Z.shape[0], 1)
        return M.numpy()
except ImportError:

    def get_mfpt(P):
        m = P.shape[0]
        I = np.eye(m)
        K = I.copy()
        for i in range(m):
            pit = P[[i], :]
            bit = pit - np.ones([1, m]) / m
            ki = 1 - bit.dot(K[:, [i]])
            CI = bit.dot(K) / ki
            K = K + K[:, [i]].dot(CI)
            pct = int(i / m * 100)
            p_bar = "+" * pct + "-" * (100 - pct)
            sys.stdout.write(f"\r{p_bar}")
            sys.stdout.flush()
        M = (I - K + matlib.repmat(np.diag(K), m, 1))
        return M


def symmetrize(M):
    return (np.array([M, M.T]).min(axis=0))


def rescale_back_and_calc_plr(M, flag, max_dist=None):
    CM = np.zeros(flag.shape[0]**2)
    bp_used = flag.reshape(-1, 1) * flag
    CM[bp_used.flatten()] = M.flatten()
    CM = CM.reshape(flag.shape[0], flag.shape[0])
    if max_dist is None:
        return CM
    plr = []
    for i in range(1, max_dist):
        v = np.diag(CM, k=i)[np.diag(bp_used, k=i)]
        if len(v) > 0:
            plr.append([v.mean(), v.std(), len(v)])
        else:
            plr.append([np.nan, np.nan, np.nan])
    return CM, pd.DataFrame(plr,
                            index=np.arange(1, max_dist),
                            columns=["Mean", "Std", "Num"])


def plr_fit(CM):
    dist = np.arange(CM.shape[0])
    X = (dist.reshape(1, -1) - dist.reshape(-1, 1))[CM > 0]
    y = CM[CM > 0]
    f = (X > 0)
    X = X[f]
    y = y[f]
    # if X.shape[0] > 5000:
    #     r = random.choice(np.arange(X.shape[0]), size=5000, replace=False)
    curve_fun = lambda x, alpha, beta, gamma, delta: alpha - gamma * (x)**(
        -beta)
    para = optimize.curve_fit(curve_fun, X, y, maxfev=5000)
    return lambda x: curve_fun(x, *para[0])


def get_similarity(M1, M2, flag, max_dist=None, min_dist=None, ord=2):
    M1 = np.log2(M1)
    M2 = np.log2(M2)
    if max_dist is None and min_dist is None:
        return linalg.norm(M1 - M2, ord=ord) / linalg.norm(
            (M1 + M2) / 2, ord=ord)
    else:
        max_dist = flag.shape[0] if max_dist is None else max_dist
        min_dist = 0 if min_dist is None else min_dist
        dist = np.arange(flag.shape[0])
        dist = abs(dist.reshape(-1, 1) - dist.reshape(1, -1))
        dist = dist[flag, :][:, flag]
        f = ((dist >= min_dist) & (dist < max_dist)).astype(int)
        N1 = f * M1
        N2 = f * M2
        return linalg.norm(N1 - N2, ord=ord) / linalg.norm(
            (N1 + N2) / 2, ord=ord)


"""def get_similarity(M1, M2, flag, max_dist=None, min_dist=None):
    M1 = np.log2(M1)
    M2 = np.log2(M2)
    if max_dist is None and min_dist is None:
        M1 = np.triu(M1)
        M2 = np.triu(M2)
    else:
        max_dist = flag.shape[0] if max_dist is None else max_dist
        min_dist = 0 if min_dist is None else min_dist
        dist = np.arange(flag.shape[0])
        dist = dist.reshape(1, -1) - dist.reshape(-1, 1)
        dist = dist[flag, :][:, flag]
        f = ((dist >= min_dist) & (dist < max_dist)).astype(int)
        N1 = f * M1
        N2 = f * M2
    M1 = M1 / linalg.norm(M1)
    M2 = M2 / linalg.norm(M2)
    return linalg.norm(M1 - M2)"""


def core(cm1, cm2, max_dist=None, min_dist=None, flag=None, return_flag=False):
    if flag is None:
        f1 = mask_low_coverage(cm1, min_coverage=__config__["min_coverage"])
        f2 = mask_low_coverage(cm2, min_coverage=__config__["min_coverage"])
        flag = get_largest_compnoent(cm1 * cm2,
                                     pre_masked=f1 & f2,
                                     return_indicator=True)

    # print(f"{sum(flag)}, {sum(flag)/cm1.shape[0]*100:.2f}% bins selected.")

    def fun(cm):
        lm = cm - np.diag(np.diag(cm))
        y = KRNorm(lm, tol=__config__["KR_tol"])
        try:
            M = get_mfpt_large_mem(y)
        except:
            M = get_mfpt(y)
        P = symmetrize(M)
        return P

    M2 = fun(cm2[flag, :][:, flag])
    M1 = fun(cm1[flag, :][:, flag])

    # M1, M2 = Parallel(n_jobs=1)(
    #     delayed(fun)(i)
    #     for i in [cm1[flag, :][:, flag], cm2[flag, :][:, flag]])
    s = get_similarity(M1,
                       M2,
                       flag,
                       max_dist=max_dist,
                       min_dist=min_dist,
                       ord=__config__["norm"])
    if return_flag:
        return s, flag
    else:
        return s
