import argparse

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--name", required=True, help="name of the user")
    args = vars(ap.parse_args())

    print "Hi %s!" % args["name"]
