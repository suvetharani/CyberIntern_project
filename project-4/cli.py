import argparse
from analyzer import analyze_password
from wordlist_generator import generate_wordlist, export_wordlist
from utils import clean_input

def main():
    parser = argparse.ArgumentParser(description="Password Strength Analyzer & Wordlist Generator")

    parser.add_argument("password", help="Password to analyze")
    parser.add_argument("--name", help="Your name", default="")
    parser.add_argument("--pet", help="Pet name", default="")
    parser.add_argument("--dob", help="Date of Birth or Year", default="")
    parser.add_argument("--custom", nargs='*', help="Any other words to include", default=[])
    parser.add_argument("--outfile", help="Output wordlist filename", default="wordlist.txt")

    args = parser.parse_args()

    # Clean and collect inputs
    inputs = list(filter(None, [
        clean_input(args.name),
        clean_input(args.pet),
        clean_input(args.dob),
        *args.custom
    ]))

    # Analyze password
    analysis = analyze_password(args.password)
    print("\n🔐 Password Strength Report")
    print("---------------------------")
    print(f"Score: {analysis['score']} / 4")
    print(f"Estimated Crack Time: {analysis['crack_time']}")
    print("Feedback:")
    for tip in analysis['feedback']['suggestions']:
        print(f"- {tip}")
    if not analysis['feedback']['suggestions']:
        print("- Looks good!")

    # Generate and export wordlist
    wordlist = generate_wordlist(inputs)
    export_wordlist(wordlist, args.outfile)
    print(f"\n✅ Wordlist exported to '{args.outfile}' with {len(wordlist)} entries.")

if __name__ == "__main__":
    main()
