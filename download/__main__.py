import data
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
        print(f"Query: {query}")
        path = os.getcwd()
        song = data.Results(query).get()[0]
        song.save(path)
