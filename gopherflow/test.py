import stackexchange
import sys

def main():
    so = stackexchange.Site(stackexchange.StackOverflow)
    q = so.question(9975469)

    for attr in dir(q):
        print("%r -> %r" % (attr, getattr(q, attr)))

if __name__ == "__main__":
    sys.exit(main())
