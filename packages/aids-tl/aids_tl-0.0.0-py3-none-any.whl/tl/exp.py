def exp(n):
    if not 1 <= n <= 10:
        raise ValueError("Only exp(1) to exp(10) are supported")

    module = __import__(f"tl.experiments.exp{n}", fromlist=["run"])
    module.run()