from multiprocessing import Process, Queue
import os
import time

# Function to search for keywords in a file and count occurrences (multiprocessing version)
def search_keywords_in_file_multiprocess(file_path, keywords, queue):
    results = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            for keyword in keywords:
                count = content.count(keyword)
                if count > 0:
                    if keyword not in results:
                        results[keyword] = []
                    # Append file name and occurrence count as a tuple (file_name, count)
                    results[keyword].append((os.path.basename(file_path), count))
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

    queue.put(results)

# Function to handle multiprocessing search
def multiprocessing_search(files, keywords):
    processes = []
    queue = Queue()
    final_results = {}

    for file_path in files:
        process = Process(target=search_keywords_in_file_multiprocess, args=(file_path, keywords, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    # Collect results from the queue
    while not queue.empty():
        result = queue.get()
        for key, value in result.items():
            if key not in final_results:
                final_results[key] = []
            final_results[key].extend(value)

    return final_results

# Function to print results in a table-like format
def print_results_table(results):
    print(f"{'Keyword':<15} {'File':<25} {'Occurrences':<10}")
    print("-" * 55)
    for keyword, file_list in results.items():
        for file_name, count in file_list:
            print(f"{keyword:<15} {file_name:<25} {count:<10}")

if __name__ == "__main__":
    # Get the current directory (where the script is running from)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the assets directory
    assets_dir = os.path.join(current_dir, "assets")

    # List of files (adjusted to reference the files in the assets folder)
    files = [
        os.path.join(assets_dir, "01-book.txt"),
        os.path.join(assets_dir, "02-book.txt"),
        os.path.join(assets_dir, "03-book.txt")
    ]

    # Define your keywords
    keywords = ["apple", "mountain", "river", "sky", "dream"]

    # Measure execution time
    start_time = time.time()
    result_multiprocessing = multiprocessing_search(files, keywords)
    end_time = time.time()

    # Print results in a table-like format
    print_results_table(result_multiprocessing)

    # Print execution time
    print(f"\nMultiprocessing took {end_time - start_time:.2f} seconds")
