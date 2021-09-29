#include<bits/stdc++.h>

using namespace std;

int main(int argc, char **argv) {
	ifstream correct_in(argv[1]), wrong_in(argv[2]);
	vector<string> c, w;
	string tmp;
	while (correct_in >> tmp) {
		c.push_back(tmp);
	}
	while (wrong_in >> tmp) {
		w.push_back(tmp);
	}
	if (c.size() != w.size()) {
		return 1;
	}
	for (int i = 0; i < (int)c.size(); i++) {
		if (c[i] != w[i]) {
			return 1;
		}
	}
	return 0;
}
