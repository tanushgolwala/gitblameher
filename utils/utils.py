def get_flag_based_on_extension(filename: str) -> int:
    if filename.endswith('.pdf'):
        return 1
    elif filename.endswith('.docx'):
        return 2
    elif filename.endswith('.txt'):
        return 3
    else:
        raise ValueError("Unsupported file type")