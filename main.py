import argparse
from cgp import CGP


def main():
    parser = argparse.ArgumentParser(description='Approximate arithmetic circuits using CGP.')
    parser.add_argument('cgpfile', type=str,
                        help='file containing input chromosome')
    parser.add_argument('--error', type=float, required=True,
                        help='sum the integers (default: find the max)')

    args = parser.parse_args()
    cgp = CGP(args.cgpfile, args.error)
    cgp.run()

if __name__ == '__main__':
    main()
