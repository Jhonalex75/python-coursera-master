# Ordered: List
steps = ["Preheat oven", "Mix ingredients", "Bake"]
print(steps[1])  # "Mix ingredients"

# Unordered: Set
user_ids = {"id1", "id2", "id3"}

# Mutable: List
cart = ["apple", "banana"]
cart.append("orange")

# Immutable: Tuple
days = ("Monday", "Tuesday", "Wednesday")
# days[0] = "Sunday"  # Error!
print(days)

playlist = []
playlist.append("Song 1")
playlist.append("Song 2")
print(playlist)
playlist.pop(0)  # Remove the song that just finished
print(playlist)

user_profiles = {
    "user123": {"name": "Alice", "age": 30},
    "user456": {"name": "Bob", "age": 25}
}
username = "user123"
print(user_profiles[username])  # Fast lookup

emails = ["a@example.com", "b@example.com", "a@example.com", "c@example.com"]
unique_emails = set(emails)
print(unique_emails)  # {'a@example.com', 'b@example.com', 'c@example.com'}

coordinates = (51.5074, -0.1278, 35)  # London: lat, lon, altitude
print(coordinates)
# coordinates[0] = 52.0  # Error! Tuples are immutable

import timeit

# List lookup
list_data = list(range(100000))
lookup_value = 99999
list_time = timeit.timeit(lambda: lookup_value in list_data, number=1000)

# Dictionary lookup
dict_data = {i: i for i in range(100000)}
dict_time = timeit.timeit(lambda: lookup_value in dict_data, number=1000)

print("List lookup time:", list_time)
print("Dictionary lookup time:", dict_time)

from collections import deque

queue = deque()
queue.append("task1")
queue.append("task2")
print(queue.popleft())  # Output: task1
queue.appendleft("urgent_task")
print(queue)

import heapq

tasks = []
heapq.heappush(tasks, (2, "low priority"))
heapq.heappush(tasks, (1, "high priority"))
heapq.heappush(tasks, (3, "very low priority"))
print(heapq.heappop(tasks))  # (1, 'high priority')

from collections import Counter

words = "apple banana apple orange banana apple".split()
word_counts = Counter(words)
print(word_counts)
print(word_counts.most_common(1))  # [('apple', 3)]

## **Common Types of Exceptions with Examples**

### 1. **ZeroDivisionError**
#Raised when trying to divide by zero.

#```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Error: Cannot divide by zero!")
    result = None
print(f"Result: {result}")


### 2. **FileNotFoundError**
#Raised when trying to access a file that doesn't exist.

#```python
try:
    with open("nonexistent_file.txt", "r") as file:
        content = file.read()
except FileNotFoundError:
    print("Error: File not found. Please check the file path.")
    # Suggest alternative or create file
    print("Creating a new file...")
    with open("new_file.txt", "w") as new_file:
        new_file.write("Hello, World!")


### 3. **TypeError**
#Raised when performing operations on incompatible types.

#```python
try:
    result = "Hello" + 123
except TypeError:
    print("Error: Cannot add string and integer.")
    result = "Hello" + str(123)  # Convert to string first
print(f"Result: {result}")


### 4. **ValueError**
#Raised when passing correct type but inappropriate value.


try:
    age = int("abc")  # Trying to convert non-numeric string to int
except ValueError:
    print("Error: Please enter a valid number for age.")
    age = 0
print(f"Age: {age}")



### 5. **IndexError**
#Raised when accessing list element with out-of-bounds index.

#```python
fruits = ["apple", "banana", "orange"]
try:
    print(fruits[5])  # Index 5 doesn't exist
except IndexError:
    print("Error: Index out of range.")
    print(f"List has {len(fruits)} items (indices 0-{len(fruits)-1})")

### 6. **KeyError**
#Raised when dictionary key is not found.

user_info = {"name": "Alice", "age": 30}
try:
    print(user_info["email"])  # Key doesn't exist
except KeyError:
    print("Error: Email not found in user info.")
    user_info["email"] = "Not provided"
print(f"User info: {user_info}")


## **Benefits of Exception Handling**

### **1. Structured Error Handling**
#Prevents crashes and provides recovery options.

#```python
def read_user_data(filename):
    try:
        with open(filename, "r") as file:
            return file.read()
    except FileNotFoundError:
        print(f"File {filename} not found. Creating default data...")
        return "default_user_data"
    except PermissionError:
        print("Permission denied. Please check file permissions.")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

# Usage
data = read_user_data("user_data.txt")
print(f"Data: {data}")

### **2. Improved User Experience**
#Provides helpful error messages.

#```python
def validate_email(email):
    try:
        if "@" not in email or "." not in email:
            raise ValueError("Invalid email format")
        return True
    except ValueError as e:
        print(f"Email validation error: {e}")
        print("Please enter a valid email address (e.g., user@example.com)")
        return False

# Usage
email = "invalid_email"
if validate_email(email):
    print("Email is valid!")
else:
    print("Please try again.")

### **3. Debugging Help**
#Exception traceback provides detailed error information.

#```python
def calculate_percentage(total, part):
    try:
        percentage = (part / total) * 100
        return percentage
    except ZeroDivisionError:
        print("Error: Total cannot be zero.")
        print("Debug info: part =", part, ", total =", total)
        return None
    except TypeError:
        print("Error: Both values must be numbers.")
        print("Debug info: part type =", type(part), ", total type =", type(total))
        return None

# Usage
result = calculate_percentage(0, 50)  # Will show debug info

### **4. Code Maintainability**
#Makes code robust and less prone to unexpected failures.

#```python
class UserManager:
    def __init__(self):
        self.users = {}
    
    def add_user(self, user_id, user_data):
        try:
            if user_id in self.users:
                raise ValueError(f"User {user_id} already exists")
            self.users[user_id] = user_data
            print(f"User {user_id} added successfully")
        except ValueError as e:
            print(f"Error adding user: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
    
    def get_user(self, user_id):
        try:
            return self.users[user_id]
        except KeyError:
            print(f"User {user_id} not found")
            return None

# Usage
manager = UserManager()
manager.add_user("001", {"name": "Alice", "age": 30})
manager.add_user("001", {"name": "Bob", "age": 25})  # Will show error
user = manager.get_user("002")  # Will show "not found"

## **Real-World Application Examples**

### **Data Entry Validation**

#```python
def validate_registration_form(name, age, email):
    errors = []
    
    try:
        if not name or len(name.strip()) < 2:
            raise ValueError("Name must be at least 2 characters long")
    except ValueError as e:
        errors.append(str(e))
    
    try:
        age = int(age)
        if age < 0 or age > 120:
            raise ValueError("Age must be between 0 and 120")
    except ValueError as e:
        errors.append("Age must be a valid number")
    
    try:
        if "@" not in email or "." not in email:
            raise ValueError("Invalid email format")
    except ValueError as e:
        errors.append(str(e))
    
    return errors

# Usage
errors = validate_registration_form("A", "abc", "invalid_email")
if errors:
    print("Registration errors:")
    for error in errors:
        print(f"- {error}")
else:
    print("Registration form is valid!")


### **Network Operations**

#```python
import time

def make_api_request(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            # Simulate API request
            if "error" in url:
                raise ConnectionError("Network timeout")
            return f"Success: Data from {url}"
        except ConnectionError as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print("Retrying in 2 seconds...")
                time.sleep(2)
            else:
                print("All retry attempts failed.")
                return None

# Usage
result = make_api_request("https://api.example.com/data")
print(result)


## **Summary Table**
'''
| Exception Type    | When Raised                    | Example Use Case                    |
|-------------------|--------------------------------|-------------------------------------|
| ZeroDivisionError | Division by zero               | Mathematical calculations           |
| FileNotFoundError | File doesn't exist             | File operations                     |
| TypeError         | Incompatible types             | Data type operations                |
| ValueError        | Wrong value for correct type   | Input validation                    |
| IndexError        | List index out of bounds       | Array/list access                   |
| KeyError          | Dictionary key not found       | Dictionary operations               |



**Key Benefits:**
- **Prevents crashes** and provides graceful error handling
- **Improves user experience** with helpful error messages
- **Aids debugging** with detailed traceback information
- **Enhances maintainability** by making code more robust

**Remember:** Always handle exceptions appropriately for your specific use case, and provide meaningful error messages to help users and developers understand what went wrong!

'''

## **Functional Code Challenge: Handling a KeyError**

def get_city_population(populations, city):
    """
    Get the population of a specified city from a dictionary.
    
    Args:
        populations: Dictionary representing city populations
        city: String representing the name of the city
    
    Returns:
        Population of the specified city if found
    
    Raises:
        KeyError: If the city is not found in the dictionary
    """
    try:
        return populations[city]
    except KeyError:
        raise KeyError(f'City "{city}" not found in population data.')

# Example usage and testing
if __name__ == "__main__":
    # Test case 1: City not found (should raise KeyError)
    city_populations = {"New York": 8336817, "Los Angeles": 3979576, "Chicago": 2679044}
    city_name = "Tampa"
    
    try:
        population = get_city_population(city_populations, city_name)
        print(f"Population of {city_name}: {population}")
    except KeyError as e:
        print(f"Error: {e}")
    
    # Test case 2: City found (should return population)
    city_name = "New York"
    
    try:
        population = get_city_population(city_populations, city_name)
        print(f"Population of {city_name}: {population}")
    except KeyError as e:
        print(f"Error: {e}")
    
    # Additional test cases
    print("\n--- Additional Test Cases ---")
    
    # Test with empty dictionary
    empty_populations = {}
    try:
        population = get_city_population(empty_populations, "Any City")
        print(f"Population: {population}")
    except KeyError as e:
        print(f"Error: {e}")
    
    # Test with case sensitivity
    try:
        population = get_city_population(city_populations, "new york")  # lowercase
        print(f"Population: {population}")
    except KeyError as e:
        print(f"Error: {e}")	