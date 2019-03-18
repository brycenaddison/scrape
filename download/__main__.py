import download.data
import os
import sys


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Proper usage: download [name of song]")
    else:
        query = ""
        for word in sys.argv[1:len(sys.argv)]:
            query = query+word+" "
        query = query.rstrip()
        print(f'Searching for: "{query}"')
        path = os.getcwd()
        data.Results(query).get()[0].save(path)


