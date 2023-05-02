import argparse


def main():
    parser = argparse.ArgumentParser(description='Approximate arithmetic circuits using CGP.')
    parser.add_argument('chromosome', type=str,
                        help='file containing input chromosome')
    parser.add_argument('--error', type=float, required=True,
                        help='sum the integers (default: find the max)')

    args = parser.parse_args()
    print(args)

if __name__ == '__main__':
    main()
