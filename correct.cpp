#include<bits/stdc++.h>

using namespace std;

int main() {
	int N;
	cin >> N;
	vector<int> v(N);
	for (int &x : v) {
		cin >> x;
	}
	sort(v.begin(), v.end());
	for (int i = 0; i < N; i++) { 
		cout << v[i] << " \n"[i == N - 1];
	}
}
