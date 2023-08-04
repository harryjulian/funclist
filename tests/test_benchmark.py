from funclist.src import funclist


def test_benchmark_list_comp_project_euler_1(benchmark):

    def _inner():
        n = [i for i in range(1000)]
        print(n)
        n = [i for i in n if i % 3 == 0 or i % 5 == 0]
        return sum(n)
    
    ans = benchmark(_inner)

    assert ans == 233168

def test_benchmark_funclist_project_euler_1(benchmark):

    def _f(x):
        return x % 3 == 0 or x % 5 == 0

    def _inner():
        ans = sum(funclist([i for i in range(1000)]).filter(_f))
        return ans
    
    ans = benchmark(_inner)
    
    assert ans == 233168