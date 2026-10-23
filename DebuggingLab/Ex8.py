def update_extensions_broken(filenames):
    """Original AI solution: attempts to change .doc to .pdf."""
    return [name.replace(".doc", ".pdf") for name in filenames]


def update_extensions(filenames):
    """Change a .doc file extension to .pdf, leaving other names unchanged."""
    return [
        name[:-4] + ".pdf" if name.endswith(".doc") else name
        for name in filenames
    ]


test_cases = [
    ["annual_report.doc"],
    ["document.doc"],
    ["doctor_visit.doc", "doc_holiday.doc"],
]

for filenames in test_cases:
    print(f"{filenames} -> {update_extensions(filenames)}")


# The original cases all happen to work: ".replace()" matches ".doc", not "doc" by itself. It is still unsafe because it replaces ".doc" anywhere, even when it is not the extension; for example, "draft.docx" becomes "draft.pdfx". Checking endswith(".doc") restricts the change to that suffix.
counterexample = ["draft.docx"]
print(
    f"Counterexample: {counterexample} -> "
    f"broken: {update_extensions_broken(counterexample)}, "
    f"fixed: {update_extensions(counterexample)}"
)


# Targeted prompt:The original code is: 
# def update_extensions(filenames):
#     """Changes .doc extensions to .pdf"""
#     return [name.replace(".doc", ".pdf") for name in filenames]
#
# A concrete failing case is ["draft.docx"]: the original returns ["draft.pdfx"] instead of leaving the name unchanged. The .replace() call blindly replaces ".doc" anywhere in a filename, not only when it is the file extension. Please change only filenames that end with ".doc" to ".pdf", preserve other names, and verify these cases:["annual_report.doc"], ["document.doc"],["doctor_visit.doc", "doc_holiday.doc"], and ["draft.docx"].