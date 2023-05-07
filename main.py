import argparse
from cgp import CGP


def main():
    parser = argparse.ArgumentParser(description='Approximate arithmetic circuits using CGP.')
    parser.add_argument('cgpfile', type=str,
                        help='CGP file containing input chromosome')
    parser.add_argument('--error', type=float, required=True,
                        help='allowed error in %')

    args = parser.parse_args()
    with open(args.cgpfile, "r") as f:
        cgp = CGP(f.read(), args.error/100)
        cgp.run()

if __name__ == '__main__':
    main()
