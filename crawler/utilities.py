import os
absolute_path = os.path.dirname(__file__)

def use_path(path):
    return os.path.join(absolute_path, path)


# Each website is a separate project (folder)
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)
    else:
        print('Directory ' + directory + ' already exists, Continuing to crawl')


# Create queue and crawled files (if not created)
def create_data_files(project_name, base_url):
    queue = os.path.join(project_name, 'queue.txt')
    crawled = os.path.join(project_name, "crawled.txt")
    if not os.path.isfile(use_path(queue)):
        write_file(queue, base_url)
    if not os.path.isfile(use_path(crawled)):
        write_file(crawled, '')


# Create a new file
def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


# Add data onto an existing file
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')


# Delete the contents of a file
def delete_file_contents(path):
    open(path, 'w').close()


# Read a file and convert each line to set items
def file_to_set(file_name):
    results = set()
    with open(use_path(file_name), 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


# Iterate through a set, each item will be a line in a file
def set_to_file(links, file_name):
    with open(use_path(file_name), "w") as f:
        for l in sorted(links):
            f.write(l+"\n")
