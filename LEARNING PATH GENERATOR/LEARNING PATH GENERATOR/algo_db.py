# --- MULTILINGUAL EXPERT ENGINE ---
# Supports high-fidelity code generation for Python, Java, C++, C, JavaScript, Go, Rust
ALGORITHM_DATABASE = {
    "find_max": {
        "keywords": ["max", "maximum", "largest", "find_max", "max_num", "list_of_numbers", "greatest"],
        "python": "def find_max(numbers):\n    if not numbers: return None\n    max_val = numbers[0]\n    for num in numbers:\n        if num > max_val: max_val = num\n    return max_val\n\n# Test\nprint(find_max([3, 7, 2, 9, 1]))  # Output: 9",
        "java": "public class Main {\n    public static int findMax(int[] arr) {\n        int max = arr[0];\n        for(int n : arr) if(n > max) max = n;\n        return max;\n    }\n    public static void main(String[] args) {\n        int[] arr = {3, 7, 2, 9, 1};\n        System.out.println(\"Max: \" + findMax(arr));\n    }\n}",
        "cpp": "#include <iostream>\n#include <vector>\nusing namespace std;\nint findMax(vector<int>& arr) {\n    int maxVal = arr[0];\n    for(int n : arr) if(n > maxVal) maxVal = n;\n    return maxVal;\n}\nint main() {\n    vector<int> arr = {3, 7, 2, 9, 1};\n    cout << \"Max: \" << findMax(arr) << endl;\n    return 0;\n}",
        "c": "#include <stdio.h>\nint findMax(int arr[], int n) {\n    int max = arr[0];\n    for(int i=1; i<n; i++) if(arr[i] > max) max = arr[i];\n    return max;\n}\nint main() {\n    int arr[] = {3, 7, 2, 9, 1};\n    printf(\"Max: %d\\n\", findMax(arr, 5));\n    return 0;\n}",
        "javascript": "function findMax(arr) {\n    return Math.max(...arr);\n}\nconsole.log('Max:', findMax([3, 7, 2, 9, 1]));",
        "go": "package main\nimport \"fmt\"\nfunc findMax(arr []int) int {\n    max := arr[0]\n    for _, n := range arr { if n > max { max = n } }\n    return max\n}\nfunc main() {\n    fmt.Println(\"Max:\", findMax([]int{3, 7, 2, 9, 1}))\n}",
        "rust": "fn find_max(arr: &[i32]) -> i32 {\n    *arr.iter().max().unwrap()\n}\nfn main() {\n    println!(\"Max: {}\", find_max(&[3, 7, 2, 9, 1]));\n}"
    },
    "find_min": {
        "keywords": ["min", "minimum", "smallest", "find_min", "min_num"],
        "python": "def find_min(numbers):\n    if not numbers: return None\n    min_val = numbers[0]\n    for num in numbers:\n        if num < min_val: min_val = num\n    return min_val\n\nprint(find_min([3, 7, 2, 9, 1]))  # Output: 1",
        "java": "public class Main {\n    public static int findMin(int[] arr) {\n        int min = arr[0];\n        for(int n : arr) if(n < min) min = n;\n        return min;\n    }\n    public static void main(String[] args) {\n        int[] arr = {3, 7, 2, 9, 1};\n        System.out.println(\"Min: \" + findMin(arr));\n    }\n}",
        "cpp": "#include <iostream>\n#include <vector>\nusing namespace std;\nint findMin(vector<int>& arr) {\n    int minVal = arr[0];\n    for(int n : arr) if(n < minVal) minVal = n;\n    return minVal;\n}\nint main() {\n    vector<int> arr = {3, 7, 2, 9, 1};\n    cout << \"Min: \" << findMin(arr) << endl;\n}",
        "c": "#include <stdio.h>\nint findMin(int arr[], int n) {\n    int min = arr[0];\n    for(int i=1; i<n; i++) if(arr[i] < min) min = arr[i];\n    return min;\n}\nint main() {\n    int arr[] = {3, 7, 2, 9, 1};\n    printf(\"Min: %d\\n\", findMin(arr, 5));\n}",
        "javascript": "function findMin(arr) {\n    return Math.min(...arr);\n}\nconsole.log('Min:', findMin([3, 7, 2, 9, 1]));"
    },
    "sum_n": {
        "keywords": ["sum", "total", "summation", "add all", "n numbers"],
        "python": "def calculate_sum(n):\n    total_sum = 0\n    for i in range(1, n + 1):\n        total_sum += i\n    return total_sum\n\nn = 10\nprint(f'Sum of 1 to {n}: {calculate_sum(n)}')",
        "java": "public class Main {\n    public static void main(String[] args) {\n        int n = 10, sum = 0;\n        for(int i=1; i<=n; i++) sum += i;\n        System.out.println(\"Sum: \" + sum);\n    }\n}",
        "cpp": "#include <iostream>\nusing namespace std;\nint main() {\n    int n = 10, sum = 0;\n    for(int i=1; i<=n; i++) sum += i;\n    cout << \"Sum: \" << sum << endl;\n    return 0;\n}",
        "c": "#include <stdio.h>\nint main() {\n    int n = 10, sum = 0;\n    for(int i=1; i<=n; i++) sum += i;\n    printf(\"Sum: %d\\n\", sum);\n    return 0;\n}",
        "javascript": "function sumToN(n) {\n    let sum = 0;\n    for(let i=1; i<=n; i++) sum += i;\n    return sum;\n}\nconsole.log('Sum:', sumToN(10));",
        "go": "package main\nimport \"fmt\"\nfunc sumToN(n int) int {\n    return n * (n + 1) / 2\n}\nfunc main() {\n    fmt.Println(\"Sum:\", sumToN(10))\n}",
        "rust": "fn sum_to_n(n: i32) -> i32 {\n    (1..=n).sum()\n}\nfn main() {\n    println!(\"Sum: {}\", sum_to_n(10));\n}"
    },
    "reverse_item": {
        "keywords": ["reverse", "reversal", "backward", "reverse string", "reverse array"],
        "python": "def reverse_data(x):\n    return x[::-1]\n\nprint(reverse_data('hello'))   # olleh\nprint(reverse_data([1,2,3]))   # [3, 2, 1]",
        "java": "public class Main {\n    public static String reverse(String s) {\n        return new StringBuilder(s).reverse().toString();\n    }\n    public static void main(String[] args) {\n        System.out.println(reverse(\"hello\"));\n    }\n}",
        "cpp": "#include <iostream>\n#include <algorithm>\nusing namespace std;\nint main() {\n    string s = \"hello\";\n    reverse(s.begin(), s.end());\n    cout << s << endl;\n}",
        "c": "#include <stdio.h>\n#include <string.h>\nvoid reverse(char* s) {\n    int n = strlen(s);\n    for (int i = 0; i < n / 2; i++) {\n        char t = s[i];\n        s[i] = s[n - i - 1];\n        s[n - i - 1] = t;\n    }\n}\nint main() {\n    char s[] = \"hello\";\n    reverse(s);\n    printf(\"%s\\n\", s);\n}",
        "javascript": "function reverse(s) {\n    return s.split('').reverse().join('');\n}\nconsole.log(reverse('hello'));"
    },
    "bubble_sort": {
        "keywords": ["bubble", "bubble sort", "sorting", "ascending", "sort array"],
        "python": "def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr\n\ndata = [64, 34, 25, 12, 22, 11, 90]\nprint('Sorted:', bubble_sort(data))",
        "java": "import java.util.Arrays;\npublic class Main {\n    static void bubbleSort(int[] arr) {\n        int n = arr.length;\n        for (int i = 0; i < n-1; i++)\n            for (int j = 0; j < n-i-1; j++)\n                if (arr[j] > arr[j+1]) {\n                    int temp = arr[j];\n                    arr[j] = arr[j+1];\n                    arr[j+1] = temp;\n                }\n    }\n    public static void main(String[] args) {\n        int[] arr = {64, 34, 25, 12, 22, 11, 90};\n        bubbleSort(arr);\n        System.out.println(\"Sorted: \" + Arrays.toString(arr));\n    }\n}",
        "cpp": "#include <iostream>\nusing namespace std;\nvoid bubbleSort(int arr[], int n) {\n    for (int i = 0; i < n-1; i++)\n        for (int j = 0; j < n-i-1; j++)\n            if (arr[j] > arr[j+1])\n                swap(arr[j], arr[j+1]);\n}\nint main() {\n    int arr[] = {64, 34, 25, 12, 22, 11, 90};\n    int n = 7;\n    bubbleSort(arr, n);\n    for(int i=0; i<n; i++) cout << arr[i] << \" \";\n}",
        "c": "#include <stdio.h>\nvoid bubbleSort(int arr[], int n) {\n    for (int i = 0; i < n-1; i++)\n        for (int j = 0; j < n-i-1; j++)\n            if (arr[j] > arr[j+1]) {\n                int temp = arr[j];\n                arr[j] = arr[j+1];\n                arr[j+1] = temp;\n            }\n}\nint main() {\n    int arr[] = {64, 34, 25, 12, 22, 11, 90};\n    int n = 7;\n    bubbleSort(arr, n);\n    for(int i=0; i<n; i++) printf(\"%d \", arr[i]);\n}",
        "javascript": "function bubbleSort(arr) {\n    let n = arr.length;\n    for (let i = 0; i < n-1; i++)\n        for (let j = 0; j < n-i-1; j++)\n            if (arr[j] > arr[j+1])\n                [arr[j], arr[j+1]] = [arr[j+1], arr[j]];\n    return arr;\n}\nconsole.log('Sorted:', bubbleSort([64, 34, 25, 12, 22, 11, 90]));"
    },
    "selection_sort": {
        "keywords": ["selection sort", "selection", "select min"],
        "python": "def selection_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        min_idx = i\n        for j in range(i+1, n):\n            if arr[j] < arr[min_idx]:\n                min_idx = j\n        arr[i], arr[min_idx] = arr[min_idx], arr[i]\n    return arr\n\nprint('Sorted:', selection_sort([64, 25, 12, 22, 11]))",
        "java": "import java.util.Arrays;\npublic class Main {\n    static void selectionSort(int[] arr) {\n        int n = arr.length;\n        for(int i = 0; i < n-1; i++) {\n            int minIdx = i;\n            for(int j = i+1; j < n; j++)\n                if(arr[j] < arr[minIdx]) minIdx = j;\n            int temp = arr[minIdx];\n            arr[minIdx] = arr[i];\n            arr[i] = temp;\n        }\n    }\n    public static void main(String[] args) {\n        int[] arr = {64, 25, 12, 22, 11};\n        selectionSort(arr);\n        System.out.println(Arrays.toString(arr));\n    }\n}",
        "cpp": "#include <iostream>\nusing namespace std;\nvoid selectionSort(int arr[], int n) {\n    for(int i = 0; i < n-1; i++) {\n        int minIdx = i;\n        for(int j = i+1; j < n; j++)\n            if(arr[j] < arr[minIdx]) minIdx = j;\n        swap(arr[i], arr[minIdx]);\n    }\n}\nint main() {\n    int arr[] = {64, 25, 12, 22, 11};\n    selectionSort(arr, 5);\n    for(int i=0; i<5; i++) cout << arr[i] << \" \";\n}",
        "c": "#include <stdio.h>\nvoid selectionSort(int arr[], int n) {\n    for(int i = 0; i < n-1; i++) {\n        int minIdx = i;\n        for(int j = i+1; j < n; j++)\n            if(arr[j] < arr[minIdx]) minIdx = j;\n        int temp = arr[minIdx];\n        arr[minIdx] = arr[i];\n        arr[i] = temp;\n    }\n}\nint main() {\n    int arr[] = {64, 25, 12, 22, 11};\n    selectionSort(arr, 5);\n    for(int i=0; i<5; i++) printf(\"%d \", arr[i]);\n}"
    },
    "insertion_sort": {
        "keywords": ["insertion sort", "insertion", "insert sort"],
        "python": "def insertion_sort(arr):\n    for i in range(1, len(arr)):\n        key = arr[i]\n        j = i - 1\n        while j >= 0 and key < arr[j]:\n            arr[j + 1] = arr[j]\n            j -= 1\n        arr[j + 1] = key\n    return arr\n\nprint('Sorted:', insertion_sort([12, 11, 13, 5, 6]))",
        "java": "import java.util.Arrays;\npublic class Main {\n    static void insertionSort(int[] arr) {\n        for(int i = 1; i < arr.length; i++) {\n            int key = arr[i], j = i - 1;\n            while(j >= 0 && arr[j] > key) {\n                arr[j+1] = arr[j]; j--;\n            }\n            arr[j+1] = key;\n        }\n    }\n    public static void main(String[] args) {\n        int[] arr = {12, 11, 13, 5, 6};\n        insertionSort(arr);\n        System.out.println(Arrays.toString(arr));\n    }\n}",
        "cpp": "#include <iostream>\nusing namespace std;\nvoid insertionSort(int arr[], int n) {\n    for(int i = 1; i < n; i++) {\n        int key = arr[i], j = i - 1;\n        while(j >= 0 && arr[j] > key) {\n            arr[j+1] = arr[j]; j--;\n        }\n        arr[j+1] = key;\n    }\n}\nint main() {\n    int arr[] = {12, 11, 13, 5, 6};\n    insertionSort(arr, 5);\n    for(int i=0; i<5; i++) cout << arr[i] << \" \";\n}"
    },
    "merge_sort": {
        "keywords": ["merge sort", "merge", "divide and conquer sort"],
        "python": "def merge_sort(arr):\n    if len(arr) <= 1: return arr\n    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    return merge(left, right)\n\ndef merge(left, right):\n    result = []\n    i = j = 0\n    while i < len(left) and j < len(right):\n        if left[i] <= right[j]:\n            result.append(left[i]); i += 1\n        else:\n            result.append(right[j]); j += 1\n    result.extend(left[i:])\n    result.extend(right[j:])\n    return result\n\nprint('Sorted:', merge_sort([38, 27, 43, 3, 9, 82, 10]))"
    },
    "quick_sort": {
        "keywords": ["quick sort", "quicksort", "partition sort"],
        "python": "def quick_sort(arr):\n    if len(arr) <= 1: return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quick_sort(left) + middle + quick_sort(right)\n\nprint('Sorted:', quick_sort([3, 6, 8, 10, 1, 2, 1]))"
    },
    "binary_search": {
        "keywords": ["binary search", "binary_search", "search target", "logarithmic search"],
        "python": "def binary_search(arr, target):\n    low, high = 0, len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target: return mid\n        elif arr[mid] < target: low = mid + 1\n        else: high = mid - 1\n    return -1\n\narr = [2, 3, 4, 10, 40]\nprint(f'Found at index: {binary_search(arr, 10)}')",
        "java": "public class Main {\n    static int binarySearch(int[] arr, int target) {\n        int l = 0, r = arr.length - 1;\n        while (l <= r) {\n            int m = l + (r - l) / 2;\n            if (arr[m] == target) return m;\n            if (arr[m] < target) l = m + 1;\n            else r = m - 1;\n        }\n        return -1;\n    }\n    public static void main(String[] args) {\n        int[] arr = {2, 3, 4, 10, 40};\n        System.out.println(\"Found at: \" + binarySearch(arr, 10));\n    }\n}",
        "cpp": "#include <iostream>\nusing namespace std;\nint binarySearch(int arr[], int n, int x) {\n    int l = 0, r = n - 1;\n    while (l <= r) {\n        int m = l + (r - l) / 2;\n        if (arr[m] == x) return m;\n        if (arr[m] < x) l = m + 1;\n        else r = m - 1;\n    }\n    return -1;\n}\nint main() {\n    int arr[] = {2, 3, 4, 10, 40};\n    cout << \"Found at: \" << binarySearch(arr, 5, 10) << endl;\n}",
        "c": "#include <stdio.h>\nint binarySearch(int arr[], int l, int r, int x) {\n    while (l <= r) {\n        int m = l + (r - l) / 2;\n        if (arr[m] == x) return m;\n        if (arr[m] < x) l = m + 1;\n        else r = m - 1;\n    }\n    return -1;\n}\nint main() {\n    int arr[] = {2, 3, 4, 10, 40};\n    printf(\"Found at: %d\\n\", binarySearch(arr, 0, 4, 10));\n}",
        "javascript": "function binarySearch(arr, target) {\n    let low = 0, high = arr.length - 1;\n    while (low <= high) {\n        let mid = Math.floor((low + high) / 2);\n        if (arr[mid] === target) return mid;\n        if (arr[mid] < target) low = mid + 1;\n        else high = mid - 1;\n    }\n    return -1;\n}\nconsole.log('Found at:', binarySearch([2,3,4,10,40], 10));"
    },
    "linear_search": {
        "keywords": ["linear search", "sequential search", "search element"],
        "python": "def linear_search(arr, target):\n    for i in range(len(arr)):\n        if arr[i] == target:\n            return i\n    return -1\n\narr = [10, 23, 45, 70, 11, 15]\nprint(f'Found at index: {linear_search(arr, 70)}')"
    },
    "prime_check": {
        "keywords": ["prime", "is_prime", "check prime", "prime number"],
        "python": "def is_prime(n):\n    if n < 2: return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0: return False\n    return True\n\nfor num in [2, 3, 4, 17, 20, 29]:\n    print(f'{num}: {\"Prime\" if is_prime(num) else \"Not Prime\"}')",
        "java": "public class Main {\n    static boolean isPrime(int n) {\n        if (n < 2) return false;\n        for (int i = 2; i <= Math.sqrt(n); i++) if (n % i == 0) return false;\n        return true;\n    }\n    public static void main(String[] args) {\n        int[] nums = {2, 3, 4, 17, 20, 29};\n        for(int n : nums) System.out.println(n + \": \" + (isPrime(n) ? \"Prime\" : \"Not Prime\"));\n    }\n}",
        "cpp": "#include <iostream>\n#include <cmath>\nusing namespace std;\nbool isPrime(int n) {\n    if (n < 2) return false;\n    for (int i = 2; i * i <= n; i++) if (n % i == 0) return false;\n    return true;\n}\nint main() {\n    int nums[] = {2, 3, 4, 17, 20, 29};\n    for(int n : nums) cout << n << \": \" << (isPrime(n) ? \"Prime\" : \"Not Prime\") << endl;\n}",
        "c": "#include <stdio.h>\nint isPrime(int n) {\n    if (n < 2) return 0;\n    for (int i = 2; i * i <= n; i++) if (n % i == 0) return 0;\n    return 1;\n}\nint main() {\n    int nums[] = {2, 3, 4, 17, 20, 29};\n    for(int i=0; i<6; i++) printf(\"%d: %s\\n\", nums[i], isPrime(nums[i]) ? \"Prime\" : \"Not Prime\");\n}"
    },
    "factorial": {
        "keywords": ["factorial", "n!", "product of n"],
        "python": "def factorial(n):\n    if n == 0: return 1\n    return n * factorial(n - 1)\n\nfor i in range(8):\n    print(f'{i}! = {factorial(i)}')",
        "java": "public class Main {\n    static long factorial(int n) {\n        return (n == 0) ? 1 : n * factorial(n - 1);\n    }\n    public static void main(String[] args) {\n        for(int i=0; i<8; i++) System.out.println(i + \"! = \" + factorial(i));\n    }\n}",
        "cpp": "#include <iostream>\nusing namespace std;\nlong long factorial(int n) {\n    return (n == 0) ? 1 : n * factorial(n - 1);\n}\nint main() {\n    for(int i=0; i<8; i++) cout << i << \"! = \" << factorial(i) << endl;\n}",
        "c": "#include <stdio.h>\nlong long factorial(int n) {\n    if (n == 0) return 1;\n    return n * factorial(n - 1);\n}\nint main() {\n    for(int i=0; i<8; i++) printf(\"%d! = %lld\\n\", i, factorial(i));\n}"
    },
    "fibonacci": {
        "keywords": ["fibonacci", "fib", "series", "fibonacci series", "fibonacci sequence"],
        "python": "def fibonacci(n):\n    a, b = 0, 1\n    result = []\n    for _ in range(n):\n        result.append(a)\n        a, b = b, a + b\n    return result\n\nprint('Fibonacci:', fibonacci(10))",
        "java": "public class Main {\n    public static void main(String[] args) {\n        int n = 10, a = 0, b = 1;\n        System.out.print(\"Fibonacci: \");\n        for(int i = 0; i < n; i++) {\n            System.out.print(a + \" \");\n            int c = a + b; a = b; b = c;\n        }\n    }\n}",
        "cpp": "#include <iostream>\nusing namespace std;\nint main() {\n    int n = 10, a = 0, b = 1;\n    cout << \"Fibonacci: \";\n    for(int i = 0; i < n; i++) {\n        cout << a << \" \";\n        int c = a + b; a = b; b = c;\n    }\n}",
        "c": "#include <stdio.h>\nint main() {\n    int n = 10, a = 0, b = 1;\n    printf(\"Fibonacci: \");\n    for(int i = 0; i < n; i++) {\n        printf(\"%d \", a);\n        int c = a + b; a = b; b = c;\n    }\n}",
        "javascript": "function fibonacci(n) {\n    let a = 0, b = 1, result = [];\n    for(let i = 0; i < n; i++) {\n        result.push(a);\n        [a, b] = [b, a + b];\n    }\n    return result;\n}\nconsole.log('Fibonacci:', fibonacci(10));"
    },
    "palindrome": {
        "keywords": ["palindrome", "palindrome check", "is palindrome"],
        "python": "def is_palindrome(s):\n    s = s.lower().replace(' ', '')\n    return s == s[::-1]\n\nwords = ['racecar', 'hello', 'madam', 'world', 'level']\nfor w in words:\n    print(f'{w}: {\"Palindrome\" if is_palindrome(w) else \"Not Palindrome\"}')",
        "java": "public class Main {\n    static boolean isPalindrome(String s) {\n        s = s.toLowerCase().replaceAll(\" \", \"\");\n        return s.equals(new StringBuilder(s).reverse().toString());\n    }\n    public static void main(String[] args) {\n        String[] words = {\"racecar\", \"hello\", \"madam\"};\n        for(String w : words) System.out.println(w + \": \" + (isPalindrome(w) ? \"Palindrome\" : \"Not\"));\n    }\n}"
    },
    "gcd": {
        "keywords": ["gcd", "greatest common divisor", "hcf", "euclidean"],
        "python": "def gcd(a, b):\n    while b:\n        a, b = b, a % b\n    return a\n\nprint(f'GCD(48, 18) = {gcd(48, 18)}')\nprint(f'GCD(56, 98) = {gcd(56, 98)}')"
    },
    "lcm": {
        "keywords": ["lcm", "least common multiple"],
        "python": "def gcd(a, b):\n    while b:\n        a, b = b, a % b\n    return a\n\ndef lcm(a, b):\n    return abs(a * b) // gcd(a, b)\n\nprint(f'LCM(12, 18) = {lcm(12, 18)}')"
    },
    "tower_of_hanoi": {
        "keywords": ["tower of hanoi", "hanoi", "disks"],
        "python": "def hanoi(n, source, target, auxiliary):\n    if n == 1:\n        print(f'Move disk 1 from {source} to {target}')\n        return\n    hanoi(n-1, source, auxiliary, target)\n    print(f'Move disk {n} from {source} to {target}')\n    hanoi(n-1, auxiliary, target, source)\n\nhanoi(3, 'A', 'C', 'B')"
    },
    "power": {
        "keywords": ["power", "exponent", "pow", "raise to power"],
        "python": "def power(base, exp):\n    if exp == 0: return 1\n    if exp < 0: return 1 / power(base, -exp)\n    result = 1\n    for _ in range(exp):\n        result *= base\n    return result\n\nprint(f'2^10 = {power(2, 10)}')\nprint(f'3^4 = {power(3, 4)}')"
    },
    "linked_list": {
        "keywords": ["linked list", "singly linked", "node", "linked"],
        "python": "class Node:\n    def __init__(self, data):\n        self.data = data\n        self.next = None\n\nclass LinkedList:\n    def __init__(self):\n        self.head = None\n\n    def append(self, data):\n        new_node = Node(data)\n        if not self.head:\n            self.head = new_node\n            return\n        current = self.head\n        while current.next:\n            current = current.next\n        current.next = new_node\n\n    def display(self):\n        elements = []\n        current = self.head\n        while current:\n            elements.append(str(current.data))\n            current = current.next\n        print(' -> '.join(elements))\n\nll = LinkedList()\nfor val in [1, 2, 3, 4, 5]:\n    ll.append(val)\nll.display()"
    },
    "stack": {
        "keywords": ["stack", "push", "pop", "lifo", "last in first out"],
        "python": "class Stack:\n    def __init__(self):\n        self.items = []\n\n    def push(self, item):\n        self.items.append(item)\n\n    def pop(self):\n        if not self.is_empty():\n            return self.items.pop()\n        return None\n\n    def peek(self):\n        if not self.is_empty():\n            return self.items[-1]\n        return None\n\n    def is_empty(self):\n        return len(self.items) == 0\n\n    def size(self):\n        return len(self.items)\n\ns = Stack()\nfor val in [10, 20, 30]:\n    s.push(val)\nprint(f'Top: {s.peek()}')\nprint(f'Pop: {s.pop()}')\nprint(f'Size: {s.size()}')"
    },
    "queue": {
        "keywords": ["queue", "enqueue", "dequeue", "fifo", "first in first out"],
        "python": "from collections import deque\n\nclass Queue:\n    def __init__(self):\n        self.items = deque()\n\n    def enqueue(self, item):\n        self.items.append(item)\n\n    def dequeue(self):\n        if not self.is_empty():\n            return self.items.popleft()\n        return None\n\n    def is_empty(self):\n        return len(self.items) == 0\n\n    def size(self):\n        return len(self.items)\n\nq = Queue()\nfor val in [10, 20, 30]:\n    q.enqueue(val)\nprint(f'Dequeue: {q.dequeue()}')\nprint(f'Size: {q.size()}')"
    },
    "bfs": {
        "keywords": ["bfs", "breadth first search", "breadth first", "level order"],
        "python": "from collections import deque\n\ndef bfs(graph, start):\n    visited = set()\n    queue = deque([start])\n    visited.add(start)\n    result = []\n    while queue:\n        node = queue.popleft()\n        result.append(node)\n        for neighbor in graph.get(node, []):\n            if neighbor not in visited:\n                visited.add(neighbor)\n                queue.append(neighbor)\n    return result\n\ngraph = {\n    'A': ['B', 'C'],\n    'B': ['D', 'E'],\n    'C': ['F'],\n    'D': [], 'E': [], 'F': []\n}\nprint('BFS:', bfs(graph, 'A'))"
    },
    "dfs": {
        "keywords": ["dfs", "depth first search", "depth first"],
        "python": "def dfs(graph, start, visited=None):\n    if visited is None:\n        visited = set()\n    visited.add(start)\n    result = [start]\n    for neighbor in graph.get(start, []):\n        if neighbor not in visited:\n            result.extend(dfs(graph, neighbor, visited))\n    return result\n\ngraph = {\n    'A': ['B', 'C'],\n    'B': ['D', 'E'],\n    'C': ['F'],\n    'D': [], 'E': [], 'F': []\n}\nprint('DFS:', dfs(graph, 'A'))"
    },
    "dijkstra": {
        "keywords": ["dijkstra", "shortest path", "weighted graph"],
        "python": "import heapq\n\ndef dijkstra(graph, start):\n    distances = {node: float('inf') for node in graph}\n    distances[start] = 0\n    pq = [(0, start)]\n    while pq:\n        dist, node = heapq.heappop(pq)\n        if dist > distances[node]: continue\n        for neighbor, weight in graph[node]:\n            new_dist = dist + weight\n            if new_dist < distances[neighbor]:\n                distances[neighbor] = new_dist\n                heapq.heappush(pq, (new_dist, neighbor))\n    return distances\n\ngraph = {\n    'A': [('B', 1), ('C', 4)],\n    'B': [('C', 2), ('D', 6)],\n    'C': [('D', 3)],\n    'D': []\n}\nprint('Shortest distances:', dijkstra(graph, 'A'))"
    },
    "knapsack": {
        "keywords": ["knapsack", "0/1 knapsack", "dynamic programming knapsack"],
        "python": "def knapsack(W, weights, values, n):\n    dp = [[0] * (W + 1) for _ in range(n + 1)]\n    for i in range(1, n + 1):\n        for w in range(W + 1):\n            if weights[i-1] <= w:\n                dp[i][w] = max(dp[i-1][w], dp[i-1][w - weights[i-1]] + values[i-1])\n            else:\n                dp[i][w] = dp[i-1][w]\n    return dp[n][W]\n\nvalues = [60, 100, 120]\nweights = [10, 20, 30]\nW = 50\nprint(f'Max value: {knapsack(W, weights, values, len(values))}')"
    },
    "matrix_multiply": {
        "keywords": ["matrix multiply", "matrix multiplication", "matrix product"],
        "python": "def matrix_multiply(A, B):\n    rows_A, cols_A = len(A), len(A[0])\n    rows_B, cols_B = len(B), len(B[0])\n    if cols_A != rows_B:\n        return None\n    result = [[0] * cols_B for _ in range(rows_A)]\n    for i in range(rows_A):\n        for j in range(cols_B):\n            for k in range(cols_A):\n                result[i][j] += A[i][k] * B[k][j]\n    return result\n\nA = [[1, 2], [3, 4]]\nB = [[5, 6], [7, 8]]\nresult = matrix_multiply(A, B)\nfor row in result:\n    print(row)"
    },
    "swap": {
        "keywords": ["swap", "exchange", "swap two"],
        "python": "def swap(a, b):\n    print(f'Before: a={a}, b={b}')\n    a, b = b, a\n    print(f'After:  a={a}, b={b}')\n    return a, b\n\nswap(5, 10)"
    }
}
