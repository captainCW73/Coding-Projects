#include <iostream>
using namespace std;

int main() {
  int firstint;
  int secondint;
  char arithchoice;

  cout << "Enter first int: ";
  cin >> firstint;

  cout << "Enter second int: ";
  cin >> secondint;

  cout << "Enter operator (+, -, *, /): ";
  cin >> arithchoice;

  if (arithchoice == '+') {
    firstint += secondint;
  } else if (arithchoice == '-') {
    firstint -= secondint;
  } else if (arithchoice == '*') {
    firstint *= secondint;
  } else if (arithchoice == '/') {
    if (secondint == 0) {
      cout << "Error: division by zero.\n";
      return 1;
    }
    firstint /= secondint;
  } else {
    cout << "Invalid choice. No operation performed.\n";
    return 1;
  }

  cout << "Result: " << firstint << "\n";
  return 0;
}
