"""
PDF Editor Tool

Usage:
  pdf_editor.py <action> [options]

Available actions:
  merge         Merge multiple PDF files
  smart-merge   Merge PDFs with page selection
  split         Split PDF pages
  encrypt       Encrypt PDF with password
  decrypt       Remove PDF password protection
  reorder       Reorder PDF pages
  compress      Compress PDF file

Examples:

1. Basic merge:
   pdf_editor.py merge -i file1.pdf file2.pdf -o combined.pdf

2. Smart merge with page selection:
   pdf_editor.py smart-merge -i "doc1.pdf:1-3" "doc2.pdf:5" -o merged.pdf

3. Split pages to individual files:
   pdf_editor.py split -i input.pdf -p "1-3,5" -o "page_%d.pdf"

4. Encrypt with password:
   pdf_editor.py encrypt -i sensitive.pdf -o secured.pdf -p "pass123" --allow-printing

5. Decrypt protected PDF:
   pdf_editor.py decrypt -i secured.pdf -o unlocked.pdf -p "pass123"

6. Reorder pages:
   pdf_editor.py reorder -i book.pdf -o new.pdf -r "3,1,2"

Get help for any action:
   pdf_editor.py <action> -h
"""


import argparse
from pathlib import Path
from pypdf import PdfWriter, PdfReader


class BasePDFTool:
    """Base class for PDF operations."""
    @classmethod
    def add_arguments(cls, subparsers):
        raise NotImplementedError

    @classmethod
    def execute(cls, args):
        raise NotImplementedError


class MergeAction(BasePDFTool):
    name = "merge"

    @classmethod
    def add_arguments(cls, subparsers):
        parser = subparsers.add_parser(cls.name, help="Merge multiple PDF files")
        parser.add_argument(
            "-i", "--inputs", 
            nargs="+", 
            type=argparse.FileType('rb'),
            required=True,
            help="Input PDF files to merge"
        )
        parser.add_argument(
            "-o", "--output", 
            type=Path, 
            default="merged.pdf",
            help="Output file name"
        )

    @classmethod
    def execute(cls, args):
        writer = PdfWriter()

        try:
            for f in args.inputs:
                writer.append(f)
                
            with open(args.output, 'wb') as out_file:
                writer.write(out_file)
                
            print(f"Merged {len(args.inputs)} files -> {args.output}")
        finally:
            writer.close()
            for f in args.inputs:
                f.close()


class SmartMergeAction(BasePDFTool):
    name = "smart-merge"

    @classmethod
    def add_arguments(cls, subparsers):
        parser = subparsers.add_parser(cls.name, help="Merge PDFs with page selection")
        parser.add_argument("-i", "--inputs", nargs="+", required=True,
                          help="Input files with optional page ranges (e.g., 'file.pdf:1-3')")
        parser.add_argument("-o", "--output", type=Path, required=True)

    @classmethod
    def _parse_input(cls, input_str):
        if ':' in input_str:
            path, pages = input_str.split(':', 1)
            return Path(path), pages
        return Path(input_str), None

    @classmethod
    def execute(cls, args):
        with PdfWriter() as writer:
            for input_spec in args.inputs:
                path, pages = cls._parse_input(input_spec)
                
                with open(path, 'rb') as f, PdfReader(f) as reader:
                    if pages:
                        pages = SplitAction._parse_page_ranges(
                            pages, len(reader.pages), zero_based=False
                        )
                        for page_num in pages:
                            writer.add_page(reader.pages[page_num])
                    else:
                        writer.append(reader)

            with open(args.output, 'wb') as f:
                writer.write(f)
            print(f"Merged {len(args.inputs)} files -> {args.output}")


class SplitAction(BasePDFTool):
    name = "split"

    @classmethod
    def add_arguments(cls, subparsers):
        parser = subparsers.add_parser(cls.name, help="Split PDF pages")
        parser.add_argument(
            "-i", "--input", 
            type=argparse.FileType('rb'),
            required=True,
            help="Input PDF file to split"
        )
        parser.add_argument(
            "-p", "--pages", 
            required=True,
            help="Page ranges to extract (e.g., '1-3,5,7-9')"
        )
        parser.add_argument(
            "-o", "--output", 
            type=str,
            required=True,
            help="Output file pattern (use %%d for page numbers, e.g., 'output_%%d.pdf')"
        )
        parser.add_argument(
            "--zero-based",
            action="store_true",
            help="Use zero-based page numbering"
        )

    @classmethod
    def _parse_page_ranges(cls, page_str, max_pages, zero_based=False):
        """Parse complex page ranges into list of page indices."""
        pages = []
        for part in page_str.split(','):
            if '-' in part:
                start_end = part.split('-')
                if len(start_end) != 2:
                    raise ValueError(f"Invalid range: {part}")
                start = int(start_end[0]) - (0 if zero_based else 1)
                end = int(start_end[1]) - (0 if zero_based else 1)
                pages.extend(range(start, end + 1))
            else:
                page = int(part) - (0 if zero_based else 1)
                pages.append(page)

        # Validate pages
        for p in pages:
            if p < 0 or p >= max_pages:
                raise ValueError(f"Page {p + (0 if zero_based else 1)} is out of range (1-{max_pages})")

        return sorted(set(pages))  # Remove duplicates and sort

    @classmethod
    def execute(cls, args):
        with PdfReader(args.input) as reader:
            total_pages = len(reader.pages)
            try:
                selected_pages = cls._parse_page_ranges(
                    args.pages, 
                    total_pages,
                    args.zero_based
                )
            except ValueError as e:
                raise SystemExit(f"Error: {e}")

            if "%d" in args.output:
                # Save individual pages
                for page_num in selected_pages:
                    writer = PdfWriter()
                    writer.add_page(reader.pages[page_num])
                    output_path = args.output % (page_num + (0 if args.zero_based else 1))
                    with open(output_path, 'wb') as f:
                        writer.write(f)
                    print(f"Saved page {page_num + (0 if args.zero_based else 1)} -> {output_path}")
            else:
                # Save all selected pages to single file
                writer = PdfWriter()
                for page_num in selected_pages:
                    writer.add_page(reader.pages[page_num])
                with open(args.output, 'wb') as f:
                    writer.write(f)
                print(f"Saved {len(selected_pages)} pages -> {args.output}")


class CompressAction(BasePDFTool):
    name = "compress"

    @classmethod
    def add_arguments(cls, subparsers):
        parser = subparsers.add_parser(cls.name, help="Compress PDF file")
        parser.add_argument(
            "-i", "--input", 
            type=argparse.FileType('rb'),
            required=True,
            help="Input PDF file to compress"
        )
        parser.add_argument(
            "-o", "--output", 
            type=Path, 
            required=True,
            help="Output compressed PDF file"
        )

    @classmethod
    def execute(cls, args):
        reader = PdfReader(args.input)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        for page in writer.pages:
            page.compress_content_streams()

        with open(args.output, 'wb') as f:
            writer.write(f)

        input_path = Path(args.input.name)
        orig_size = input_path.stat().st_size
        comp_size = args.output.stat().st_size
        ratio = comp_size / orig_size

        print(f"Original Size  : {orig_size:,} bytes")
        print(f"Compressed Size: {comp_size:,} bytes ({ratio:.1%} of original)")


class EncryptAction(BasePDFTool):
    name = "encrypt"

    @classmethod
    def add_arguments(cls, subparsers):
        parser = subparsers.add_parser(cls.name, help="Encrypt PDF with password")
        parser.add_argument("-i", "--input", type=argparse.FileType('rb'), required=True)
        parser.add_argument("-o", "--output", type=Path, required=True)
        parser.add_argument("-p", "--password", required=True, help="Encryption password")
        parser.add_argument("--allow-printing", action="store_true", 
                          help="Allow printing of the PDF")

    @classmethod
    def execute(cls, args):
        with PdfReader(args.input) as reader, PdfWriter() as writer:
            writer.append(reader)

            # Set permissions
            permissions = 0
            if args.allow_printing:
                permissions |= 4

            writer.encrypt(
                user_password=args.password,
                owner_password=None,
                use_128bit=True,
                permissions_flag=permissions
            )

            with open(args.output, 'wb') as f:
                writer.write(f)
            print(f"Encrypted PDF saved to {args.output}")


class DecryptAction(BasePDFTool):
    name = "decrypt"

    @classmethod
    def add_arguments(cls, subparsers):
        parser = subparsers.add_parser(cls.name, help="Remove PDF password protection")
        parser.add_argument("-i", "--input", type=argparse.FileType('rb'), required=True)
        parser.add_argument("-o", "--output", type=Path, required=True)
        parser.add_argument("-p", "--password", required=True, help="Document password")

    @classmethod
    def execute(cls, args):
        with PdfReader(args.input) as reader:
            if not reader.is_encrypted:
                raise SystemExit("Error: File is not encrypted")

            reader.decrypt(args.password)

            with PdfWriter() as writer, open(args.output, 'wb') as f:
                for page in reader.pages:
                    writer.add_page(page)
                writer.write(f)
            print(f"Decrypted PDF saved to {args.output}")


class ReorderAction(BasePDFTool):
    name = "reorder"

    @classmethod
    def add_arguments(cls, subparsers):
        parser = subparsers.add_parser(cls.name, help="Reorder PDF pages")
        parser.add_argument("-i", "--input", type=argparse.FileType('rb'), required=True)
        parser.add_argument("-o", "--output", type=Path, required=True)
        parser.add_argument("-r", "--order", required=True,
                          help="New page order (e.g., '3,1,2')")

    @classmethod
    def execute(cls, args):
        with PdfReader(args.input) as reader:
            try:
                new_order = [int(x) - 1 for x in args.order.split(',')]
                max_page = len(reader.pages) - 1

                for page_num in new_order:
                    if page_num < 0 or page_num > max_page:
                        raise ValueError(f"Invalid page number: {page_num + 1}")

                with PdfWriter() as writer, open(args.output, 'wb') as f:
                    for page_num in new_order:
                        writer.add_page(reader.pages[page_num])
                    writer.write(f)
                    print(f"Reordered PDF saved to {args.output}")

            except ValueError as e:
                raise SystemExit(f"Error: Invalid page order format - {e}")


class PDFEditor:
    def __init__(self):
        self.actions = {}
        self.parser = argparse.ArgumentParser(
            description="PDF Editor Tool",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        self.subparsers = self.parser.add_subparsers(
            title="Available actions",
            dest="action",
            required=True
        )

    def register_action(self, action_cls):
        """Register a new PDF action"""
        self.actions[action_cls.name] = action_cls
        action_cls.add_arguments(self.subparsers)

    def run(self):
        """Run the application"""
        args = self.parser.parse_args()
        self.actions[args.action].execute(args)


def main():
    editor = PDFEditor()
    editor.register_action(MergeAction)
    editor.register_action(SplitAction)
    editor.register_action(CompressAction)
    editor.register_action(EncryptAction)
    editor.register_action(DecryptAction)
    editor.register_action(ReorderAction)
    editor.register_action(SmartMergeAction)
    editor.run()


if __name__ == "__main__":
    main()
