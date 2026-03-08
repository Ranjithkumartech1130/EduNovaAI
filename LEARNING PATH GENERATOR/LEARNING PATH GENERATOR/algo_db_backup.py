# --- MULTILINGUAL EXPERT ENGINE ---
# This engine supports high-fidelity code generation for Python, Java, C++, and C
ALGORITHM_DATABASE = {
    "find_max": {
        "keywords": ["max", "maximum", "largest", "find_max", "max_num", "list_of_numbers"],
        "python": "def find_max(numbers):\n    if not numbers: return None\n    max_val = numbers[0]\n    for num in numbers:\n        if num > max_val: max_val = num\n    return max_val",
        "java": "public static int findMax(int[] arr) {\n    int max = arr[0];\n    for(int n : arr) if(n > max) max = n;\n    return max;\n}",
        "cpp": "int findMax(vector<int>& arr) {\n    int maxVal = arr[0];\n    for(int n : arr) if(n > maxVal) maxVal = n;\n    return maxVal;\n}",
        "c": "int findMax(int arr[], int n) {\n    int max = arr[0];\n    for(int i=1; i<n; i++) if(arr[i] > max) max = arr[i];\n    return max;\n}",
        "javascript": "function findMax(arr) {\n    return Math.max(...arr);\n}",
        "go": "func findMax(arr []int) int {\n    max := arr[0]\n    for _, n := range arr { if n > max { max = n } }\n    return max\n}",
        "rust": "fn find_max(arr: &[i32]) -> i32 {\n    *arr.iter().max().unwrap()\n}"
    },
    "sum_n": {
        "keywords": ["sum", "total", "summation", "add all", "n numbers"],
        "python": "def calculate_sum():\n    n = int(input('Enter a number n: '))\n    total_sum = 0\n    for i in range(1, n + 1):\n        total_sum += i\n    print(f'The sum is: {total_sum}')\n\ncalculate_sum()",
        "java": "import java.util.Scanner;\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        System.out.print(\"Enter n: \");\n        int n = sc.nextInt();\n        int sum = 0;\n        for(int i=1; i<=n; i++) sum += i;\n        System.out.println(\"Sum: \" + sum);\n    }\n}",
        "cpp": "#include <iostream>\nusing namespace std;\nint main() {\n    int n, sum = 0;\n    cout << \"Enter n: \";\n    cin >> n;\n    for(int i=1; i<=n; i++) sum += i;\n    cout << \"Sum: \" << sum << endl;\n    return 0;\n}",
        "c": "#include <stdio.h>\nint main() {\n    int n, sum = 0;\n    printf(\"Enter n: \");\n    scanf(\"%d\", &n);\n    for(int i=1; i<=n; i++) sum += i;\n    printf(\"Sum: %d\\n\", sum);\n    return 0;\n}",
        "javascript": "function sumToN(n) {\n    let sum = 0;\n    for(let i=1; i<=n; i++) sum += i;\n    return sum;\n}",
        "go": "func sumToN(n int) int {\n    return n * (n + 1) / 2\n}",
        "rust": "fn sum_to_n(n: i32) -> i32 {\n    (1..=n).sum()\n}"
    },
    "reverse_item": {
        "keywords": ["reverse", "reversal", "backward"],
        "python": "def reverse_data(x):\n    return x[::-1]",
        "java": "public String reverse(String s) {\n    return new StringBuilder(s).reverse().toString();\n}",
        "cpp": "string reverseStr(string s) {\n    reverse(s.begin(), s.end());\n    return s;\n}",
        "c": "void reverse(char* s) {\n    int n = strlen(s);\n    for (int i = 0; i < n / 2; i++) {\n        char t = s[i];\n        s[i] = s[n - i - 1];\n        s[n - i - 1] = t;\n    }\n}"
    },
    "bubble_sort": {
        "keywords": ["bubble", "sort", "sorting", "ascending"],
        "python": "def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr",
        "java": "void bubbleSort(int[] arr) {\n    int n = arr.length;\n    for (int i = 0; i < n-1; i++)\n        for (int j = 0; j < n-i-1; j++)\n            if (arr[j] > arr[j+1]) {\n                int temp = arr[j];\n                arr[j] = arr[j+1];\n                arr[j+1] = temp;\n            }\n}",
        "cpp": "void bubbleSort(int arr[], int n) {\n    for (int i = 0; i < n-1; i++)\n        for (int j = 0; j < n-i-1; j++)\n            if (arr[j] > arr[j+1])\n                swap(arr[j], arr[j+1]);\n}",
        "c": "void bubbleSort(int arr[], int n) {\n    for (int i = 0; i < n-1; i++)\n        for (int j = 0; j < n-i-1; j++)\n            if (arr[j] > arr[j+1]) {\n                int temp = arr[j];\n                arr[j] = arr[j+1];\n                arr[j+1] = temp;\n            }\n}"
    },
    "binary_search": {
        "keywords": ["binary search", "binary_search", "search target", "logarithmic search"],
        "python": "def binary_search(arr, target):\n    low, high = 0, len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target: return mid\n        elif arr[mid] < target: low = mid + 1\n        else: high = mid - 1\n    return -1",
        "java": "int binarySearch(int[] arr, int target) {\n    int l = 0, r = arr.length - 1;\n    while (l <= r) {\n        int m = l + (r - l) / 2;\n        if (arr[m] == target) return m;\n        if (arr[m] < target) l = m + 1;\n        else r = m - 1;\n    }\n    return -1;\n}",
        "cpp": "int binarySearch(int arr[], int n, int x) {\n    int l = 0, r = n - 1;\n    while (l <= r) {\n        int m = l + (r - l) / 2;\n        if (arr[m] == x) return m;\n        if (arr[m] < x) l = m + 1;\n        else r = m - 1;\n    }\n    return -1;\n}",
        "c": "int binarySearch(int arr[], int l, int r, int x) {\n    while (l <= r) {\n        int m = l + (r - l) / 2;\n        if (arr[m] == x) return m;\n        if (arr[m] < x) l = m + 1;\n        else r = m - 1;\n    }\n    return -1;\n}"
    },
    "prime_check": {
        "keywords": ["prime", "is_prime", "check prime", "prime number"],
        "python": "def is_prime(n):\n    if n < 2: return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0: return False\n    return True",
        "java": "boolean isPrime(int n) {\n    if (n < 2) return false;\n    for (int i = 2; i <= Math.sqrt(n); i++) if (n % i == 0) return false;\n    return true;\n}",
        "cpp": "bool isPrime(int n) {\n    if (n < 2) return false;\n    for (int i = 2; i * i <= n; i++) if (n % i == 0) return false;\n    return true;\n}",
        "c": "int isPrime(int n) {\n    if (n < 2) return 0;\n    for (int i = 2; i * i <= n; i++) if (n % i == 0) return 0;\n    return 1;\n}"
    },
    "factorial": {
        "keywords": ["factorial", "n!", "product of n"],
        "python": "def factorial(n):\n    return 1 if n == 0 else n * factorial(n - 1)",
        "java": "long factorial(int n) {\n    return (n == 0) ? 1 : n * factorial(n - 1);\n}",
        "cpp": "long long factorial(int n) {\n    return (n == 0) ? 1 : n * factorial(n - 1);\n}",
        "c": "long long factorial(int n) {\n    if (n == 0) return 1;\n    return n * factorial(n - 1);\n}"
    },
    "fibonacci": {
        "keywords": ["fibonacci", "fib", "series"],
        "python": "def fibonacci(n):\n    a, b = 0, 1\n    for _ in range(n): a, b = b, a + b\n    return a",
        "java": "int fib(int n) {\n    int a = 0, b = 1, c;\n    if (n == 0) return a;\n    for (int i = 2; i <= n; i++) { c = a + b; a = b; b = c; }\n    return b;\n}",
        "cpp": "int fib(int n) {\n    int a = 0, b = 1, c;\n    if( n == 0) return a;\n    for(int i = 2; i <= n; i++){ c = a + b; a = b; b = c; }\n    return b;\n}",
        "c": "int fib(int n) {\n    int a = 0, b = 1, c;\n    if( n == 0) return a;\n    for(int i = 2; i <= n; i++){ c = a + b; a = b; b = c; }\n    return b;\n}"
    }
}
