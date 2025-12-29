import argparse
from src.pipeline import train, recognize, add_student


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Smart Attendance System with Incremental Learning')
    parser.add_argument('--train', action='store_true', help='Train embeddings (incremental by default)')
    parser.add_argument('--full-retrain', action='store_true', help='Retrain ALL students from scratch')
    parser.add_argument('--add-student', type=str, metavar='ROLL_NO', help='Add specific student by roll number')
    parser.add_argument('--recognize', action='store_true', help='Run attendance recognition')
    parser.add_argument('--threshold', type=float, default=0.6, help='Recognition threshold (default 0.6)')
    args = parser.parse_args()
    
    if args.full_retrain:
        train(incremental=False)
    elif args.train:
        train(incremental=True)
    elif args.add_student:
        add_student(args.add_student)
    elif args.recognize or (not args.train and not args.add_student and not args.full_retrain):
        recognize(args.threshold)
