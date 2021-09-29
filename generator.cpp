#include<bits/stdc++.h>

using namespace std;

mt19937_64 my_rand;
int rand(int l, int r) {
	return l + my_rand() % (r - l + 1);
}

//Only 1 parameter , the seed
int main(int argc, char **argv) {
	int seed = atoi(argv[1]);
	my_rand.seed(seed);
	int N = rand(10, 10000);
	cout << N << endl;
	for (int i = 0; i < N; i++) {
		cout << rand(1, 1000);
	}
	cout << endl;
}
