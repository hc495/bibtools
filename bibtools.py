from src import paper_link, preprocessings, unique, misc
import argparse
import re
try:
    import bibtexparser
except ImportError:
    print("Please install bibtexparser by running 'pip install bibtexparser'.")


def add_url_to_bib(bib_path, output_path = None, semantics_scholar_api_key = None):
    if output_path is None:
        output_path = bib_path
    if preprocessings.is_utf8(bib_path):
        replacement = preprocessings.non_standard_entrance_replacement()
        replacement.encode(bib_path)
        with open(bib_path, 'rb') as bibtex_file:
            library = bibtexparser.load(bibtex_file)
        paper_link.add_url_by_Arxiv_number(library)
        paper_link.add_url_by_doi(library)
        paper_link.add_url_by_scholar_search(library, semantics_scholar_api_key)
        paper_link.final_scan(library)
        with open(output_path, 'w') as bibtex_file:
            bibtexparser.dump(library, bibtex_file)
        replacement.decode(output_path)
    else:
        print(f"{bib_path} is not encoded in UTF-8. Please convert it to UTF-8 and try again.")


def duplicate_remove(bib_path, output_path = None):
    if output_path is None:
        output_path = bib_path
    if preprocessings.is_utf8(bib_path):
        replacement = preprocessings.non_standard_entrance_replacement()
        replacement.encode(bib_path)
        with open(bib_path, 'rb') as bibtex_file:
            library = bibtexparser.load(bibtex_file)
        library, num, instructions = unique.unique(library)
        if num > 0:
            print(f"\033[31m{num} repeated entries are removed.\033[0m")
        else:
            print("\033[32mClean Library.\033[0m")
        if len(instructions) > 0:
            print("\033[31mRequired cite entry replacements:")
            for line in instructions:
                print("\033[31m" + line + "\033[0m")
            with open('replacement.txt', 'w') as instructions_file:
                for line in instructions:
                    instructions_file.write(line + '\n')
            print("\033[31mReplacement instructions are saved to replacement.txt.\033[0m")
        else:
            print("\033[32mNo cite entry replacement required.\033[0m")
        with open(output_path, 'w') as bibtex_file:
            bibtexparser.dump(library, bibtex_file)
        replacement.decode(output_path)
    else:
        print(f"{bib_path} is not encoded in UTF-8. Please convert it to UTF-8 and try again.")

def capitalize_title(bib_path, output_path = None):
    count = 0
    if output_path is None:
        output_path = bib_path
    if preprocessings.is_utf8(bib_path):
        replacement = preprocessings.non_standard_entrance_replacement()
        replacement.encode(bib_path)
        with open(bib_path, 'rb') as bibtex_file:
            library = bibtexparser.load(bibtex_file)
        for paper in library.entries:
            new_title = misc.capitalize_title(paper['title'])
            if new_title != paper['title']:
                print(f"{paper['title']} -> {new_title}.")
                paper['title'] = new_title
                count += 1
        if count > 0:
            print(f"\033[31m{count} titles are capitalized.\033[0m")
        else:
            print("\033[32mAll title is clean, no capitalization needed.\033[0m")
        with open(output_path, 'w') as bibtex_file:
            bibtexparser.dump(library, bibtex_file)
        replacement.decode(output_path)
    else:
        print(f"{bib_path} is not encoded in UTF-8. Please convert it to UTF-8 and try again.")


def lowercase_title(bib_path, output_path = None):
    count = 0
    if output_path is None:
        output_path = bib_path
    if preprocessings.is_utf8(bib_path):
        replacement = preprocessings.non_standard_entrance_replacement()
        replacement.encode(bib_path)
        with open(bib_path, 'rb') as bibtex_file:
            library = bibtexparser.load(bibtex_file)
        for paper in library.entries:
            new_title = misc.lowercase_title(paper['title'])
            if new_title != paper['title']:
                print(f"{paper['title']} -> {new_title}.")
                paper['title'] = new_title
                count += 1
        if count > 0:
            print(f"\033[31m{count} titles are lowercased.\033[0m")
        else:
            print("\033[32mAll title is clean, no lowercasing needed.\033[0m")
        with open(output_path, 'w') as bibtex_file:
            bibtexparser.dump(library, bibtex_file)
        replacement.decode(output_path)
    else:
        print(f"{bib_path} is not encoded in UTF-8. Please convert it to UTF-8 and try again.")


def booktitle_fix(bib_path, output_path = None):
    count = 0
    if output_path is None:
        output_path = bib_path

    if preprocessings.is_utf8(bib_path):
        replacement = preprocessings.non_standard_entrance_replacement()
        replacement.encode(bib_path)

        with open(bib_path, 'rb') as bibtex_file:
            library = bibtexparser.load(bibtex_file)

        ordinal_map = {
            "first": "1st", "second": "2nd", "third": "3rd", "fourth": "4th", "fifth": "5th",
            "sixth": "6th", "seventh": "7th", "eighth": "8th", "ninth": "9th", "tenth": "10th",
            "eleventh": "11th", "twelfth": "12th", "thirteenth": "13th", "fourteenth": "14th",
            "fifteenth": "15th", "sixteenth": "16th", "seventeenth": "17th", "eighteenth": "18th",
            "nineteenth": "19th", "twentieth": "20th", "twenty-first": "21st", "twenty second": "22nd",
            "twenty-third": "23rd", "twenty-fourth": "24th", "twenty-fifth": "25th", "twenty-sixth": "26th", "twenty-seventh": "27th", "twenty-eighth": "28th",
            "twenty-ninth": "29th", "thirtieth": "30th", "thirty-first": "31st", "thirty second": "32nd", "thirty-third": "33rd", "thirty-fourth": "34th", "thirty-fifth": "35th", "thirty-sixth": "36th", "thirty-seventh": "37th", "thirty-eighth": "38th", "thirty-ninth": "39th", "fortieth": "40th",
            "forty-first": "41st", "forty-second": "42nd", "forty-third": "43rd", "forty-fourth": "44th", "forty-fifth": "45th", "forty-sixth": "46th", "forty-seventh": "47th", "forty-eighth": "48th", "forty-ninth": "49th", "fiftieth": "50th"
        }
        pattern = re.compile(
            r"\b(" + "|".join(sorted(map(re.escape, ordinal_map.keys()), key=len, reverse=True)) + r")\b",
            flags=re.IGNORECASE
        )

        def _replace_ordinal(text: str) -> str:
            return pattern.sub(lambda m: ordinal_map[m.group(0).lower()], text)

        for paper in library.entries:
            if 'booktitle' in paper:
                target = 'booktitle'
            elif 'journal' in paper:
                target = 'journal'
            else:
                continue

            old_booktitle = paper[target]
            new_booktitle = misc.capitalize_title(old_booktitle)
            new_booktitle = re.sub(r'^(\s*)The\b', r'\1the', new_booktitle)
            new_booktitle = _replace_ordinal(new_booktitle)

            if new_booktitle != old_booktitle:
                print(f"{old_booktitle} -> {new_booktitle}.")
                paper[target] = new_booktitle
                count += 1

        if count > 0:
            print(f"\033[31m{count} {target} entries are fixed.\033[0m")
        else:
            print(f"\033[32mAll {target} entries are clean.\033[0m")

        with open(output_path, 'w') as bibtex_file:
            bibtexparser.dump(library, bibtex_file)

        replacement.decode(output_path)
    else:
        print(f"{bib_path} is not encoded in UTF-8. Please convert it to UTF-8 and try again.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='A small tool to process .bib files efficiently. Maybe for your dissertation?',
        epilog='Written by Yufeng Zhao (alias: Hakaze Cho)'
    )
    parser.add_argument(
        'task',
        type=str,
        help='The task to be executed. Options: "url"; "unique"; "cap".'
    )
    parser.add_argument(
        'bib_path',
        type=str,
        help='The path to the .bib file.'
    )
    parser.add_argument(
        '-o',
        '--output_path',
        type=str,
        help='The path to the output .bib file.'
    )
    parser.add_argument(
        '-k',
        '--semantics_scholar_api_key',
        type=str,
        help='The API key for Semantic Scholar.'
    )
    args = parser.parse_args()
    if args.task == "url":
        add_url_to_bib(args.bib_path, args.output_path, args.semantics_scholar_api_key)
    elif args.task == "unique":
        duplicate_remove(args.bib_path, args.output_path)
    elif args.task == "cap":
        capitalize_title(args.bib_path, args.output_path)
    elif args.task == "low":
        lowercase_title(args.bib_path, args.output_path)
    elif args.task == "booktitle_fix":
        booktitle_fix(args.bib_path, args.output_path)
    else:
        print(f"Task {args.task} is not supported. Please choose from 'url' or 'unique'.")