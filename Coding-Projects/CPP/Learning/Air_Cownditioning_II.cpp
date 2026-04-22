#include <iostream>
using namespace std;

int main() {
  int n, m_limit;
  cin >> n >> m_limit;

  for (int i = 0; i < n; i++) {
    int s, t, c;
    cin >> s >> t >> c;
    cout << t << "\n";
  }

  for (int i = 0; i < m_limit; i++) {
    int a, b, p, m;
    cin >> a >> b >> p >> m;
  }

  return 0;
}