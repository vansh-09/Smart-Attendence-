import argparse
from src.pipeline import train, recognize


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Smart Attendance System')
    parser.add_argument('--train', action='store_true', help='Train embeddings for all students')
    parser.add_argument('--recognize', action='store_true', help='Run attendance recognition')
    parser.add_argument('--threshold', type=float, default=0.6, help='Recognition threshold (default 0.6)')
    args = parser.parse_args()
    
    if args.train:
        train()
    elif args.recognize or (not args.train):
        recognize(args.threshold)
