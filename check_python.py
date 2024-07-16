import sys
import platform

def main():
    print(sys.version_info)
    if sys.version_info[0] <= 2 or (sys.version_info[0] == 3 and sys.version_info[1] < 8):
        exit(10)
    else:
        exit(5)
    
if __name__ == '__main__':
    main()